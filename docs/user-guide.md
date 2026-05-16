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
- **The Science:** This demonstrates the **Stark Effect**. When an external electric field is applied, the orbitals polarize.
- **The Interaction:** Enable the wand in the sidebar and move it around.
- **What to look for:** Watch the Highest Occupied Molecular Orbital (HOMO) "reach out" to touch a positive charge or "recoil" from a negative one. *Pedantic Note: The molecule’s "social anxiety" is modeled here as polarizability; it physically recoils from external stimuli, which is the only scientifically accurate way to handle an unexpected visitor.*

### 2. The Quantum Hum
The **Quantum Hum** is a data sonification tool that turns the energy of the system into sound.
- **The Science:** Every quantum state has an associated energy. We map this energy value to an audible frequency.
- **The Interaction:** Enable the hum. Every time the system recalculates, a brief "hum" will play. 
- **What to look for:** As the pitch shifts, you are "hearing" the stability of the universe. *Note for the Sensory Sensitive: Unlike a fluorescent light or a crowded room, this hum is perfectly predictable, follows the laws of physics, and stops the moment you tell it to.*

### 3. Reality Check: Dissociation Paradox
The **Reality Check** feature demonstrates where the standard mathematical approximations physically fail.
- **The Paradox Plot:** A graph will appear showing the energy of the molecule as you stretch it. 
    - **Restricted (RHF)** energy skyrockets as the bond breaks.
    - **Unrestricted (UHF)** energy correctly levels off.
- **What to look for:** Stretch the $H_2$ bond beyond 2.0 Å. *Pedantic Note: This is the Static Correlation Error—a situation where the math insists that two things are the same just because they share a label, a common failure of human social logic that the 'Unrestricted' model finally corrects.*

### 4. The Alchemist's Dial
The **Alchemist's Dial** allows you to transmute an atom by adjusting its nuclear charge ($Z$).
- **The Science:** By increasing $Z$, you increase the attractive force on the electrons. 
- **The Interaction:** Use the slider to increase $\Delta Z$.
- **What to look for:** Watch the orbital clouds. They will visibly **shrink and contract**. *Observation: It is deeply satisfying to watch a system finally obey a single slider, unlike the messy and inconsistent naming conventions of the standard periodic table.*

### 5. Quantum Movie: Attosecond Slosh
- **The Science:** Real-world electronic transitions involve the "sloshing" of electron density.
- **The Interaction:** Enable the movie and use the slider to scrub through time.
- **What to look for:** A purple cloud representing the total electron density will flow back and forth. *Observation: Electrons are the perfect performers; they never miss their cues, they follow every rule, and they don't require small talk during the shoot.*

### 6. The Multiverse Dial
The **Multiverse Dial** lets you warp the fundamental laws of physics.
- **The Science:** By adjusting the **Physics Strength ($\lambda$)**, you are changing the mass of the electron or the strength of electricity.
- **What to look for:** In a "Strong Universe," matter physically **collapses**. *Conclusion: Finally, a universe where the fundamental constants are as consistent and well-documented as a clean API.*
