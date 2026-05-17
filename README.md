# OrbitalPlay

Interactive Molecular Orbital Education. Solve the Schrödinger equation for simple molecules in real-time and visualize the resulting orbitals.

📚 **[Full Documentation](https://elkins.github.io/orbital-play/)**

## Interactive Tutorials

Explore the quantum world through guided Jupyter notebooks.

| Tutorial | Description | Link |
| :--- | :--- | :--- |
| **01: The Hydrogen Bond** | Discover the simplest chemical bond and the nature of bonding/anti-bonding orbitals. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/elkins/orbital-play/blob/main/notebooks/01_The_Hydrogen_Bond.ipynb) |
| **02: VSEPR and Hybridization** | Visualize why molecules have specific shapes and how lone pairs "push" other orbitals. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/elkins/orbital-play/blob/main/notebooks/02_VSEPR_and_Hybridization.ipynb) |

## What is OrbitalPlay?

OrbitalPlay is a "Visual Orbital Engine" designed to bridge the gap between abstract quantum mechanics and physical chemical intuition. It transforms complex mathematical wavefunctions into interactive 3D visualizations that students can manipulate in real-time.

### Core Features
- **Interactive Playground:** Move atoms and watch bonding/anti-bonding orbitals "warp" on the fly.
- **Scientific Rigor:** Powered by **PySCF**, using the Hartree-Fock method and STO-3G basis sets to ensure accuracy.
- **Spin Visualization:** Explore open-shell systems (like the ·OH radical) and see how Alpha and Beta electrons occupy different spatial regions.
- **Notebook Ready:** Full integration with Jupyter and Google Colab for guided classroom discovery.

## Why it Matters
Most introductory chemistry students only see static, 2D representations of orbitals in textbooks. OrbitalPlay provides a dynamic environment where the connection between molecular geometry and electronic structure becomes tangible.

---

## Installation

```bash
pip install orbital-play
```

## Usage

### Streamlit App
Launch the main interactive dashboard:
```bash
streamlit run app.py
```

### Python Library
Integrate the engine into your own research or educational notebooks:
```python
from orbital_play import engine, show_orbital

# Define and calculate
geo = engine.generate_geometry("H2O", dist=0.96, angle=104.5)
mol, mf = engine.run_calculation(geo)

# Visualize the HOMO
cube = engine.generate_cube_string(mol, mf, mo_index=4)
show_orbital(mol, cube)
```

