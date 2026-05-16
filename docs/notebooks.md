# Interactive Notebooks

While the Streamlit app provides a fast, playground-style experience, our **Guided Discovery Notebooks** are designed for deeper educational exploration. 

These notebooks interleave theoretical narrative with executable code, allowing students to "look under the hood" of the quantum engine.

## Google Colab Integration

Every notebook in our library includes a **"Open in Colab"** badge. This allows students to run full quantum chemistry simulations directly in their browser without any local setup.

### Available Notebooks

1. **[01: The Hydrogen Bond](https://colab.research.google.com/github/elkins/orbital-play/blob/main/notebooks/01_The_Hydrogen_Bond.ipynb)**
   - Learn about constructive and destructive interference.
   - Visualize bonding and anti-bonding orbitals in $H_2$.

## Using the Library in Your Own Notebooks

You can use the `orbital-play` engine and visualizer in any Jupyter environment:

```python
!pip install orbital-play pyscf py3Dmol

from orbital_play import engine, show_orbital

# 1. Define geometry
geo = engine.generate_geometry("H2O", dist=0.96, angle=104.5)

# 2. Run calculation
mol, mf = engine.run_calculation(geo)

# 3. Visualize HOMO
cube = engine.generate_cube_string(mol, mf, mo_index=4)
show_orbital(mol, cube)
```
)
```
