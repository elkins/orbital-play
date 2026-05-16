# User Guide

The OrbitalPlay interface is designed for exploration. Here is how to navigate the "Quantum Playground".

## The Dashboard

When you launch the app, you will see a 3D visualization area on the left and a calculation summary on the right.

### 1. Molecular Geometry (Sidebar)
Use the sliders in the sidebar to modify the structure of the molecule:
- **Select Molecule:** Choose between $H_2$, $H_2O$, $CH_4$, and the $OH$ Radical.
- **Bond Distance:** Adjust the distance between atoms in Angstroms (Å).
- **Bond Angle:** (For $H_2O$) Adjust the angle between the Oxygen and Hydrogen atoms.

As you move the sliders, the underlying quantum engine recalculates the orbitals in real-time.

### 2. Orbital Visualization (Sidebar)
- **Select Molecular Orbital:** Choose which orbital to visualize. They are sorted by energy level.
- **Spin Channel:** (Only for radicals) Toggle between **Alpha (↑)** and **Beta (↓)** orbitals. In open-shell systems, these spatial distributions are not identical!
- **Isosurface Value:** Adjust the "transparency" or threshold of the orbital cloud. A lower value shows more of the diffuse electron cloud, while a higher value focuses on the dense regions of probability.

### 3. Interpreting the 3D View
- **Stick & Sphere:** Atoms are shown as spheres, and bonds as sticks.
- **Blue Surfaces:** Represent the positive phase ($+$) of the wavefunction.
- **Red Surfaces:** Represent the negative phase ($-$) of the wavefunction.

### 4. Calculation Summary
The right panel provides the technical data behind the visual:
- **Total Energy:** The ground state energy of the molecule.
- **MO Energies:** A list of the energies for each calculated molecular orbital. The orbital currently selected in the sidebar is highlighted in bold.

## Tips for Educators
- **Bonding vs. Anti-bonding:** Show students the $H_2$ molecule. MO 1 (bonding) has a continuous cloud between nuclei, while MO 2 (anti-bonding) has a distinct node (gap) in the middle.
- **Geometric Influence:** Watch how the HOMO (Highest Occupied Molecular Orbital) of Water changes its shape as you vary the bond angle from 90° to 120°.
- **Spin Polarization:** Select the **OH Radical**. Toggle between Alpha and Beta spin channels for the same MO index (e.g., MO 5). Notice how the "Alpha" orbital (which contains the unpaired electron) has a different shape and energy than its "Beta" counterpart. This is a direct visualization of the Pauli Exclusion Principle and exchange interaction in action.
