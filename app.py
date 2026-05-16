import streamlit as st
from orbital_play import engine, sonify
from stmol import showmol
import py3Dmol
import numpy as np

st.set_page_config(page_title="OrbitalPlay", layout="wide")

st.title("🧪 OrbitalPlay: Molecular Orbital Playground")
st.markdown("""
Explore how molecular orbitals change as you adjust molecular geometry.
Calculations are performed in real-time using Hartree-Fock theory (STO-3G basis).
""")

# Sidebar for controls
st.sidebar.header("Molecular Geometry")

molecule_type = st.sidebar.selectbox("Select Molecule", ["H2", "H2O", "CH4", "OH (Radical)"])
spin = 0

if molecule_type == "H2":
    dist = st.sidebar.slider("Bond Distance (Å)", 0.5, 5.0, 0.74, 0.01)
    geometry = engine.generate_geometry("H2", dist=dist)
    
elif molecule_type == "H2O":
    dist = st.sidebar.slider("O-H Bond Distance (Å)", 0.8, 1.5, 0.96, 0.01)
    angle = st.sidebar.slider("H-O-H Angle (degrees)", 80.0, 120.0, 104.5, 0.5)
    geometry = engine.generate_geometry("H2O", dist=dist, angle=angle)

elif molecule_type == "CH4":
    dist = st.sidebar.slider("C-H Bond Distance (Å)", 0.8, 1.5, 1.09, 0.01)
    geometry = engine.generate_geometry("CH4", dist=dist)

elif molecule_type == "OH (Radical)":
    dist = st.sidebar.slider("O-H Bond Distance (Å)", 0.5, 2.0, 0.97, 0.01)
    geometry = engine.generate_geometry("OH", dist=dist)
    spin = 1

# Experimental section
st.sidebar.header("Experimental Features")
use_wand = st.sidebar.checkbox("The Stark Wand", value=False, help="Interact with the molecule using an external point charge.")
wand_pos = None
wand_charge = 0.0
if use_wand:
    wx = st.sidebar.slider("Wand X (Å)", -5.0, 5.0, 2.0, 0.1)
    wy = st.sidebar.slider("Wand Y (Å)", -5.0, 5.0, 0.0, 0.1)
    wz = st.sidebar.slider("Wand Z (Å)", -5.0, 5.0, 0.0, 0.1)
    wand_pos = (wx, wy, wz)
    wand_charge = st.sidebar.slider("Wand Charge (q)", -2.0, 2.0, 1.0, 0.1)

use_audio = st.sidebar.checkbox("The Quantum Hum", value=False, help="Hear the energy state of the molecule.")
use_reality = st.sidebar.checkbox("Reality Check", value=False, help="Visualize the dissociation paradox where the math breaks.")
use_alchemist = st.sidebar.checkbox("The Alchemist's Dial", value=False, help="Transmute the atom by continuously changing its nuclear charge.")
use_movie = st.sidebar.checkbox("Quantum Movie: Attosecond Slosh", value=False, help="Visualize real-time electron sloshing (TDHF).")

alchemist_delta = 0.0
if use_alchemist:
    alchemist_delta = st.sidebar.slider("Nuclear Charge Delta (ΔZ)", -0.5, 1.0, 0.0, 0.05)

@st.cache_resource
def get_calculation(geometry, spin=0, wand_pos=None, wand_charge=0.0, alchemist_delta=0.0):
    mol, mf = engine.run_calculation(geometry, spin=spin, wand_coords=wand_pos, wand_charge=wand_charge, alchemist_delta=alchemist_delta)
    return mol, mf

@st.cache_data
def get_cube(geometry, mo_index, spin=0, spin_type='alpha', wand_pos=None, wand_charge=0.0, alchemist_delta=0.0, nx=40, ny=40, nz=40):
    # Reuse the cached calculation from st.cache_resource
    mol, mf = get_calculation(geometry, spin=spin, wand_pos=wand_pos, wand_charge=wand_charge, alchemist_delta=alchemist_delta)
    return engine.generate_cube_string(mol, mf, mo_index, spin_type=spin_type, nx=nx, ny=ny, nz=nz)

@st.cache_data
def get_dissociation_data(molecule_type):
    distances = np.linspace(0.5, 5.0, 40)
    rhf, uhf = engine.calculate_dissociation_curve(molecule_type, distances)
    return distances, rhf, uhf

@st.cache_data
def get_movie_frames(geometry, spin=0, wand_pos=None, wand_charge=0.0, alchemist_delta=0.0):
    mol, mf = get_calculation(geometry, spin=spin, wand_pos=wand_pos, wand_charge=wand_charge, alchemist_delta=alchemist_delta)
    return engine.get_attosecond_frames(mol, mf)

# Orbital selection
st.sidebar.header("Orbital Visualization")
spin_type = 'alpha'
if spin > 0:
    spin_type = st.sidebar.radio("Spin Channel", ["Alpha (↑)", "Beta (↓)"]).split(" ")[0].lower()

iso_val = st.sidebar.slider("Isosurface Value", 0.01, 0.2, 0.05, 0.01)

st.sidebar.header("About OrbitalPlay")
st.sidebar.info(r"""
This tool uses the **PySCF** library to solve the 
Schrödinger equation via the Hartree-Fock method. 
Orbitals are visualized by calculating the wavefunction 
$\psi$ on a 3D grid and rendering isosurfaces where 
$|\psi|$ is constant.

Blue: Positive phase (+)
Red: Negative phase (-)
""")

st.sidebar.caption("OrbitalPlay v0.1")

# Run calculation
with st.spinner("Calculating orbitals..."):
    try:
        mol, mf = get_calculation(geometry, spin=spin, wand_pos=wand_pos, wand_charge=wand_charge, alchemist_delta=alchemist_delta)
        summary = engine.get_molecule_summary(mol, mf, alchemist_delta=alchemist_delta)
        
        n_mo = summary['n_mo']
        
        # Determine current MO energies and occupation based on spin_type
        if spin == 0:
            mo_energies = summary['mo_energies']
            mo_occ = summary['mo_occ']
        else:
            mo_energies = summary['mo_energies'][spin_type]
            mo_occ = summary['mo_occ'][spin_type]

        if not use_movie:
            mo_index = st.sidebar.selectbox("Select Molecular Orbital", 
                                           range(n_mo), 
                                           format_func=lambda i: f"MO {i+1} ({'Occupied' if mo_occ[i]>0 else 'Virtual'})")
            
            cube_data = get_cube(geometry, mo_index, spin=spin, spin_type=spin_type, wand_pos=wand_pos, wand_charge=wand_charge, alchemist_delta=alchemist_delta)
        else:
            # Movie mode
            frames = get_movie_frames(geometry, spin=spin, wand_pos=wand_pos, wand_charge=wand_charge, alchemist_delta=alchemist_delta)
            frame_idx = st.sidebar.slider("Movie Frame (Time)", 0, len(frames)-1, 0)
            cube_data = frames[frame_idx]
        
        # Display summary in columns
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.subheader("Calculation Summary")
            st.write(f"**Total Energy:** {summary['energy']:.6f} Ha")
            st.write(f"**Converged:** {summary['converged']}")
            st.write(f"**Electrons:** {summary['n_electron']}")
            
            if use_audio:
                hum_wav = sonify.generate_hum(summary['energy'])
                st.audio(hum_wav, format="audio/wav")

            if use_reality and molecule_type == "H2":
                st.markdown("---")
                st.subheader("The Dissociation Paradox")
                dists, rhf, uhf = get_dissociation_data("H2")
                
                import pandas as pd
                chart_data = pd.DataFrame({
                    'Distance (Å)': dists,
                    'Restricted (RHF)': rhf,
                    'Unrestricted (UHF)': uhf
                }).set_index('Distance (Å)')
                
                st.line_chart(chart_data)
                st.info("The **Restricted (RHF)** energy fails to level off, diverging from reality. This is the **Static Correlation Error**.")

            spin_label = f" ({spin_type.capitalize()})" if spin > 0 else ""
            st.subheader(f"MO Energies{spin_label}")
            for i, energy in enumerate(mo_energies):
                label = f"MO {i+1}"
                if i == mo_index:
                    label = f"**{label}**"
                st.write(f"{label}: {energy:.4f} Ha")

        with col1:
            # Visualization
            xyz_str = mol.tostring(format='xyz')
            
            view = py3Dmol.view(width=800, height=600)
            view.addModel(xyz_str, 'xyz')
            view.setStyle({'stick': {}, 'sphere': {'scale': 0.3}})
            
            # Label atoms with effective charge
            for i in range(mol.natm):
                symb = mol.atom_symbol(i)
                coord = mol.atom_coord(i) * 0.529177 # Bohr to Angstrom
                # First atom gets the delta
                z_eff = mol.atom_charge(i) + (alchemist_delta if i == 0 else 0)
                label = f"{symb} (Z={z_eff:.2f})"
                
                view.addLabel(label, {'position': {'x': coord[0], 'y': coord[1], 'z': coord[2]}, 
                                      'backgroundColor': 'gray', 'fontColor': 'white', 'fontSize': 10, 'opacity': 0.6})

            # Render the Stark Wand if active
            if use_wand:
                wand_color = "#FFD700" if wand_charge > 0 else "#9932CC" # Gold or Dark Orchid
                view.addSphere({'center': {'x': wand_pos[0], 'y': wand_pos[1], 'z': wand_pos[2]}, 
                                'radius': 0.4, 'color': wand_color, 'opacity': 0.8})
                # Add a label for the charge
                view.addLabel(f"q={wand_charge:+.1f}", {'position': {'x': wand_pos[0], 'y': wand_pos[1], 'z': wand_pos[2]}, 
                                                       'backgroundColor': 'white', 'fontColor': 'black', 'fontSize': 12})

            # Add volumetric data (orbitals or total density)
            if not use_movie:
                view.addVolumetricData(cube_data, "cube", {'isoval': iso_val, 'color': "blue", 'opacity': 0.6})
                view.addVolumetricData(cube_data, "cube", {'isoval': -iso_val, 'color': "red", 'opacity': 0.6})
            else:
                # Total Density is always positive
                # We use a higher isoval for total density visibility
                view.addVolumetricData(cube_data, "cube", {'isoval': iso_val * 2, 'color': "purple", 'opacity': 0.6})
            
            view.zoomTo()
            showmol(view, height=600, width=800)

            if use_reality and molecule_type == "H2" and dist > 1.8 and spin == 0:
                st.warning("⚠️ **Unphysical State:** In this 'Restricted' mode, electrons are forced into a mathematical 'ghost' state where they are delocalized across both atoms, even at 5 Å.")
            
    except Exception as e:
        st.error(f"Error during calculation: {e}")
        st.info("Try adjusting the geometry to more reasonable values.")

st.markdown("---")
st.caption("Developed for OrbitalPlay - Interactive Science Education")
