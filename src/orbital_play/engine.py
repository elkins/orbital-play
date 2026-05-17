import numpy as np
from pyscf import gto, scf, qmmm, tdscf
from pyscf.tools import cubegen
import io
import tempfile
import os

def generate_geometry(molecule_type, **kwargs):
    """
    Generates an XYZ geometry string for a given molecule type and parameters.
    """
    if molecule_type == "H2":
        dist = kwargs.get('dist', 0.74)
        return f"H 0 0 0; H 0 0 {dist}"
    
    elif molecule_type == "H2O":
        dist = kwargs.get('dist', 0.96)
        angle = kwargs.get('angle', 104.5)
        rad = np.radians(angle)
        x = dist * np.sin(rad/2)
        z = dist * np.cos(rad/2)
        return f"O 0 0 0; H {x} 0 {z}; H {-x} 0 {z}"
    
    elif molecule_type == "CH4":
        dist = kwargs.get('dist', 1.09)
        a = dist / np.sqrt(3)
        return f"""C 0 0 0; 
                   H {a} {a} {a}; 
                   H {a} {-a} {-a}; 
                   H {-a} {a} {-a}; 
                   H {-a} {-a} {a}"""
    
    elif molecule_type == "OH":
        dist = kwargs.get('dist', 0.97)
        return f"O 0 0 0; H 0 0 {dist}"
    
    elif molecule_type == "NH3":
        dist = kwargs.get('dist', 1.01)
        angle = kwargs.get('angle', 106.7)
        # Convert H-N-H angle to angle between N-H and symmetry axis
        # cos(alpha) = 1.5 * cos^2(beta) - 0.5
        rad_alpha = np.radians(angle)
        cos_beta = np.sqrt((np.cos(rad_alpha) + 0.5) / 1.5)
        sin_beta = np.sqrt(1.0 - cos_beta**2)
        
        z = -dist * cos_beta
        r_xy = dist * sin_beta
        
        return (f"N 0 0 0; "
                f"H {r_xy} 0 {z}; "
                f"H {-r_xy*0.5} {r_xy*np.sqrt(3)/2} {z}; "
                f"H {-r_xy*0.5} {-r_xy*np.sqrt(3)/2} {z}")

    elif molecule_type == "CO2":
        dist = kwargs.get('dist', 1.16)
        return f"C 0 0 0; O 0 0 {dist}; O 0 0 {-dist}"

    elif molecule_type == "C2H4":
        dist_cc = kwargs.get('dist_cc', 1.34)
        dist_ch = kwargs.get('dist_ch', 1.08)
        angle = kwargs.get('angle', 121.3) # H-C-H angle
        
        rad = np.radians(angle)
        x = dist_ch * np.sin(rad/2)
        z_h = dist_ch * np.cos(rad/2)
        z_c = dist_cc / 2
        
        return (f"C 0 0 {z_c}; C 0 0 {-z_c}; "
                f"H {x} 0 {z_c + z_h}; H {-x} 0 {z_c + z_h}; "
                f"H {x} 0 {-z_c - z_h}; H {-x} 0 {-z_c - z_h}")

    else:
        raise ValueError(f"Unsupported molecule type: {molecule_type}")

def run_calculation(geometry_str, basis='sto-3g', spin=0, wand_coords=None, wand_charge=0.0, alchemist_delta=0.0, physics_scale=1.0):
    """
    Runs a Restricted or Unrestricted Hartree-Fock calculation with optional external point charges.
    spin: 2S = N_alpha - N_beta
    wand_coords: (x, y, z) tuple in Angstroms
    wand_charge: float
    alchemist_delta: float - Added charge to the first nucleus in the molecule.
    physics_scale: float - Scaling factor for physical constants (e.g. electron mass).
    """
    # 0. The Multiverse Dial: Scale coordinates by 1/lambda
    # This is equivalent to scaling the electron mass by lambda.
    if abs(physics_scale - 1.0) > 1e-6:
        lines = geometry_str.strip().split(';')
        scaled_lines = []
        for line in lines:
            parts = line.strip().split()
            if not parts: continue
            symbol = parts[0]
            # Scale coordinates by 1/physics_scale
            coords = [float(p) / physics_scale for p in parts[1:]]
            scaled_lines.append(f"{symbol} {' '.join(map(str, coords))}")
        geometry_str = '; '.join(scaled_lines)

    mol = gto.M(atom=geometry_str, basis=basis, unit='Angstrom', spin=spin)
    if spin == 0:
        mf = scf.RHF(mol)
    else:
        mf = scf.UHF(mol)

    # Prepare background charges
    charges = []
    coords_bohr = []

    # 1. The Stark Wand
    if wand_coords is not None and abs(wand_charge) > 1e-6:
        # Convert Angstroms to Bohr (1 Angstrom ≈ 1.88973 Bohr)
        coords_bohr.append(np.array(wand_coords) * 1.88973)
        charges.append(wand_charge)

    # 2. The Alchemist's Dial (Nuclear transmutation)
    if abs(alchemist_delta) > 1e-6:
        # Place the charge exactly on the first atom's nucleus
        # Nudge it by a tiny amount to avoid 1/0 singularies
        offset = 1e-5
        atom_pos = mol.atom_coord(0) # In Bohr
        coords_bohr.append(atom_pos + offset)
        charges.append(alchemist_delta)

    if charges:
        mf = qmmm.add_mm_charges(mf, np.array(coords_bohr), charges)

    mf.kernel()
    return mol, mf

def calculate_dissociation_curve(molecule_type, distances, basis='sto-3g'):
    """
    Calculates RHF and UHF energies for a range of distances.
    Useful for demonstrating the dissociation paradox (static correlation error).
    """
    rhf_energies = []
    uhf_energies = []
    
    for dist in distances:
        geometry = generate_geometry(molecule_type, dist=dist)
        
        # RHF
        mol_rhf = gto.M(atom=geometry, basis=basis, unit='Angstrom', spin=0)
        mf_rhf = scf.RHF(mol_rhf)
        mf_rhf.verbose = 0
        mf_rhf.kernel()
        rhf_energies.append(mf_rhf.e_tot)
        
        # UHF
        mol_uhf = gto.M(atom=geometry, basis=basis, unit='Angstrom', spin=0)
        mf_uhf = scf.UHF(mol_uhf)
        mf_uhf.verbose = 0
        
        if dist > 1.2:
            # Manually nudge UHF to break symmetry (Static Correlation demonstration)
            dm_initial = mf_uhf.get_init_guess()
            # Perturb the beta density matrix to favor localization
            dm_initial[1][0, 0] += 0.1 
            mf_uhf.kernel(dm0=dm_initial)
        else:
            mf_uhf.kernel()
            
        uhf_energies.append(mf_uhf.e_tot)
        
    return rhf_energies, uhf_energies

def get_attosecond_frames(mol, mf, n_frames=10, amplitude=0.5):
    """
    Generates a sequence of total electron density cubes representing 
    the 'sloshing' of electrons in an excited state superposition.
    """
    # 1. Run TDHF for the first excited state
    td = tdscf.rhf.TDHF(mf)
    td.nstates = 1
    td.kernel()
    
    # 2. Extract transition density matrix in AO basis
    # T = C_occ * X * C_virt.T + C_virt * Y * C_occ.T
    mo_coeff = mf.mo_coeff
    nocc = mol.nelectron // 2
    
    x, y = td.xy[0] # Amplitudes for first state
    # x and y are (nocc, nvir)
    
    c_occ = mo_coeff[:, :nocc]
    c_vir = mo_coeff[:, nocc:]
    
    # Transition density matrix (AO basis)
    t_dm = (c_occ @ x @ c_vir.T) + (c_vir @ y @ c_occ.T)
    # Ensure it's symmetric for cubegen (approximating real part)
    t_dm = t_dm + t_dm.T
    
    # Ground state density
    gs_dm = mf.make_rdm1()
    
    frames = []
    # Create temporal sequence (one full cycle)
    for i in range(n_frames):
        phase = 2 * np.pi * i / n_frames
        # Superposition density: rho_gs + amp * cos(theta) * rho_trans
        current_dm = gs_dm + amplitude * np.cos(phase) * t_dm
        
        # Generate cube string for total density
        fd, path = tempfile.mkstemp(suffix='.cube')
        try:
            cubegen.density(mol, path, current_dm, nx=30, ny=30, nz=30)
            with open(path, 'r') as f:
                frames.append(f.read())
        finally:
            os.close(fd)
            if os.path.exists(path):
                os.remove(path)
                
    return frames

def generate_cube_string(mol, mf, mo_index, spin_type='alpha', nx=40, ny=40, nz=40):
    """
    Generates a Gaussian Cube file as a string for a specific molecular orbital.
    mo_index: 0-indexed index of the molecular orbital.
    spin_type: 'alpha' or 'beta' (only for UHF)
    """
    # Create a temporary file to store the cube data
    fd, path = tempfile.mkstemp(suffix='.cube')
    try:
        # Determine the correct MO coefficients
        # mf.mo_coeff for RHF is (n_ao, n_mo) - ndim=2
        # mf.mo_coeff for UHF is (2, n_ao, n_mo) - ndim=3
        if mf.mo_coeff.ndim == 2:
            # RHF
            mo_coeff = mf.mo_coeff[:, mo_index]
        else:
            # UHF
            if spin_type == 'alpha':
                mo_coeff = mf.mo_coeff[0][:, mo_index]
            else:
                mo_coeff = mf.mo_coeff[1][:, mo_index]

        cubegen.orbital(mol, path, mo_coeff, nx=nx, ny=ny, nz=nz)
        
        with open(path, 'r') as f:
            cube_data = f.read()
    finally:
        os.close(fd)
        if os.path.exists(path):
            os.remove(path)
            
    return cube_data

def get_molecule_summary(mol, mf, alchemist_delta=0.0, physics_scale=1.0):
    """Returns a summary of the calculation results."""
    # Check if RHF or UHF
    # mo_energy: RHF is (n_mo,), UHF is (2, n_mo)
    if mf.mo_energy.ndim == 1:
        # RHF
        mo_energies = (mf.mo_energy * physics_scale).tolist()
        mo_occ = mf.mo_occ.tolist()
        n_mo = len(mf.mo_energy)
    else:
        # UHF - Return a dict with alpha and beta
        mo_energies = {
            'alpha': (mf.mo_energy[0] * physics_scale).tolist(),
            'beta': (mf.mo_energy[1] * physics_scale).tolist()
        }
        mo_occ = {
            'alpha': mf.mo_occ[0].tolist(),
            'beta': mf.mo_occ[1].tolist()
        }
        n_mo = len(mf.mo_energy[0])

    energy = mf.e_tot * physics_scale
    
    # Energy Correction for Alchemist's Dial
    # We must subtract the unphysical repulsion between the host nucleus 
    # and the delta-charge we placed on top of it.
    if abs(alchemist_delta) > 1e-6:
        offset_bohr = (1e-5) * 1.88973 # 1e-5 Angstrom in Bohr
        z_host = mol.atom_charge(0)
        # Using simple Coulomb repulsion between point charges at this distance
        repulsion_correction = (z_host * alchemist_delta) / offset_bohr
        energy -= repulsion_correction

    summary = {
        'energy': energy,
        'converged': mf.converged,
        'mo_energies': mo_energies,
        'mo_occ': mo_occ,
        'n_electron': mol.nelectron,
        'n_mo': n_mo
    }
    return summary
