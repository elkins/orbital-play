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

## Experimental Features

OrbitalPlay includes highly experimental features to explore the "weirdness" of quantum chemistry.

### 1. The Stark Wand
The **Stark Wand** allows you to interact with the molecule using an external point charge (an "Ion"). 
- **The Science:** This demonstrates the **Stark Effect**. When an external electric field (from your Wand) is applied, the molecular orbitals polarize.
- **The Interaction:** Enable the wand in the sidebar and use the X, Y, Z sliders to move it around the molecule. Use the **Charge ($q$)** slider to change its intensity.
- **What to look for:** Watch the Highest Occupied Molecular Orbital (HOMO) of Water "reach out" to touch a positive charge or "recoil" from a negative one.

### 2. The Quantum Hum
The **Quantum Hum** is a data sonification tool that turns the energy of the system into sound.
- **The Science:** Every quantum state has an associated energy. We map this energy value to an audible frequency.
- **The Interaction:** Enable the hum in the sidebar. Every time the system recalculates, a brief "hum" will play. 
- **What to look for:** As you move the Stark Wand or change the bond distance, notice how the **pitch** of the hum shifts. This provides an auditory "feel" for the stability of the quantum system.

### 3. Reality Check: Dissociation Paradox
The **Reality Check** feature demonstrates where the standard mathematical approximations in quantum chemistry physically fail.
- **The Pathological Case:** Select **$H_2$** and enable **Reality Check**.
- **The Paradox Plot:** A graph will appear showing the energy of the molecule as you stretch it. 
    - **Restricted (RHF)** energy (our default) skyrockets as the bond breaks. This is impossible!
    - **Unrestricted (UHF)** energy correctly levels off.
- **What to look for:** Stretch the $H_2$ bond distance beyond 2.0 Å. In the 3D view, you will see a warning. In the **Restricted** state, the math is forcing the two electrons to stay "smeared out" across both atoms even when they are miles apart. This is a purely mathematical artifact called **Static Correlation Error**.

### 4. The Alchemist's Dial
The **Alchemist's Dial** allows you to continuously transmute an atom by adjusting its nuclear charge ($Z$).
- **The Science:** The "gravity" of an atom comes from the positive charge of its nucleus. By increasing $Z$, you increase the attractive force on the electrons. This is the concept of **Effective Nuclear Charge**.
- **The Interaction:** Enable the dial in the sidebar and use the **Nuclear Charge Delta ($\Delta Z$)** slider.
- **What to look for:** Watch the orbital clouds. As you increase $\Delta Z$, the orbitals will visibly **shrink and contract** toward the nucleus. This demonstrates why atoms get smaller as you move from left to right across the periodic table!
