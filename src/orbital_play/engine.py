import numpy as np
from pyscf import gto, scf
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
    
    else:
        raise ValueError(f"Unsupported molecule type: {molecule_type}")

def run_calculation(geometry_str, basis='sto-3g', spin=0):
    """
    Runs a Restricted or Unrestricted Hartree-Fock calculation.
    spin: 2S = N_alpha - N_beta
    """
    mol = gto.M(atom=geometry_str, basis=basis, unit='Angstrom', spin=spin)
    if spin == 0:
        mf = scf.RHF(mol)
    else:
        mf = scf.UHF(mol)
    mf.kernel()
    return mol, mf

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

def get_molecule_summary(mol, mf):
    """Returns a summary of the calculation results."""
    # Check if RHF or UHF
    # mo_energy: RHF is (n_mo,), UHF is (2, n_mo)
    if mf.mo_energy.ndim == 1:
        # RHF
        mo_energies = mf.mo_energy.tolist()
        mo_occ = mf.mo_occ.tolist()
        n_mo = len(mf.mo_energy)
    else:
        # UHF - Return a dict with alpha and beta
        mo_energies = {
            'alpha': mf.mo_energy[0].tolist(),
            'beta': mf.mo_energy[1].tolist()
        }
        mo_occ = {
            'alpha': mf.mo_occ[0].tolist(),
            'beta': mf.mo_occ[1].tolist()
        }
        n_mo = len(mf.mo_energy[0])

    summary = {
        'energy': mf.e_tot,
        'converged': mf.converged,
        'mo_energies': mo_energies,
        'mo_occ': mo_occ,
        'n_electron': mol.nelectron,
        'n_mo': n_mo
    }
    return summary
