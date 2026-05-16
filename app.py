import streamlit as st
from orbital_play import engine
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
    dist = st.sidebar.slider("Bond Distance (Å)", 0.5, 3.0, 0.74, 0.01)
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

@st.cache_resource
def get_calculation(geometry, spin=0):
    mol, mf = engine.run_calculation(geometry, spin=spin)
    return mol, mf

@st.cache_data
def get_cube(geometry, mo_index, spin=0, spin_type='alpha', nx=40, ny=40, nz=40):
    # Reuse the cached calculation from st.cache_resource
    mol, mf = get_calculation(geometry, spin=spin)
    return engine.generate_cube_string(mol, mf, mo_index, spin_type=spin_type, nx=nx, ny=ny, nz=nz)

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
        mol, mf = get_calculation(geometry, spin=spin)
        summary = engine.get_molecule_summary(mol, mf)
        
        n_mo = summary['n_mo']
        
        # Determine current MO energies and occupation based on spin_type
        if spin == 0:
            mo_energies = summary['mo_energies']
            mo_occ = summary['mo_occ']
        else:
            mo_energies = summary['mo_energies'][spin_type]
            mo_occ = summary['mo_occ'][spin_type]

        mo_index = st.sidebar.selectbox("Select Molecular Orbital", 
                                       range(n_mo), 
                                       format_func=lambda i: f"MO {i+1} ({'Occupied' if mo_occ[i]>0 else 'Virtual'})")
        
        cube_data = get_cube(geometry, mo_index, spin=spin, spin_type=spin_type)
        
        # Display summary in columns
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.subheader("Calculation Summary")
            st.write(f"**Total Energy:** {summary['energy']:.6f} Ha")
            st.write(f"**Converged:** {summary['converged']}")
            st.write(f"**Electrons:** {summary['n_electron']}")
            
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
            
            # Add volumetric data (orbitals)
            view.addVolumetricData(cube_data, "cube", {'isoval': iso_val, 'color': "blue", 'opacity': 0.6})
            view.addVolumetricData(cube_data, "cube", {'isoval': -iso_val, 'color': "red", 'opacity': 0.6})
            
            view.zoomTo()
            showmol(view, height=600, width=800)
            
    except Exception as e:
        st.error(f"Error during calculation: {e}")
        st.info("Try adjusting the geometry to more reasonable values.")

st.markdown("---")
st.caption("Developed for OrbitalPlay - Interactive Science Education")
