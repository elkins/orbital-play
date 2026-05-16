# Theoretical Background

OrbitalPlay uses established principles of computational chemistry to visualize the invisible.

## The Schrödinger Equation

At the heart of the engine is the time-independent Schrödinger Equation:

$$ \hat{H}\Psi = E\Psi $$

Where:
- $\hat{H}$ is the Hamiltonian operator representing the total energy.
- $\Psi$ is the wavefunction.
- $E$ is the energy of the system.

## Hartree-Fock Method

Since the exact Schrödinger equation cannot be solved for systems with more than one electron, we use the **Hartree-Fock (HF)** method. This is an approximation that assumes each electron moves in an average field created by the other electrons and the nuclei.

OrbitalPlay implements **Restricted Hartree-Fock (RHF)**, which is suitable for the closed-shell molecules ($H_2$, $H_2O$, $CH_4$) featured in the playground.

## Basis Sets (STO-3G)

To solve the HF equations on a computer, we represent the wavefunction as a combination of simple functions called a **Basis Set**. 

We use the **STO-3G** basis set. It is a "minimal basis set," meaning it uses the minimum number of functions required to describe the occupied orbitals. This makes calculations extremely fast—ideal for real-time interaction—while still providing qualitatively correct orbital shapes for educational purposes.

## Restricted vs. Unrestricted Hartree-Fock

In most introductory chemistry, we assume that every molecular orbital is occupied by two electrons with opposite spins (Alpha ↑ and Beta ↓). This is known as **Restricted Hartree-Fock (RHF)**.

However, in **Open-Shell Systems** (like radicals), there are unpaired electrons. In these cases, we use **Unrestricted Hartree-Fock (UHF)**.

### Spin Polarization
In UHF, Alpha and Beta electrons are allowed to occupy different spatial orbitals. An unpaired Alpha electron will interact differently with other Alpha electrons than with Beta electrons. This "polarizes" the core electrons, causing the Alpha and Beta spatial wavefunctions to diverge. 

OrbitalPlay allows you to toggle between these two sets of orbitals for the **Hydroxyl radical (·OH)**, making this subtle quantum effect visible.

## Advanced Experimental Phenomena

OrbitalPlay extends beyond basic Hartree-Fock to showcase complex physical interactions.

### 1. The Stark Effect & Polarizability
When an external electric field is applied (via the **Stark Wand**), the molecular Hamiltonian is perturbed:

\\[ \hat{H} = \hat{H}_0 - \vec{\mu} \cdot \vec{E} \\]

Where \\(\vec{\mu}\\) is the molecular dipole operator and \\(\vec{E}\\) is the external field. This interaction causes the electron density to shift, or **polarize**. You can observe the orbitals physically "stretching" toward or "recoiling" from your external point charge, demonstrating the molecule's response to its environment.

### 2. Atomic Contraction (The Alchemist's Dial)
The size of an orbital is dictated by the balance between the kinetic energy of the electron and the electrostatic attraction of the nucleus. For a hydrogen-like atom, the radial part of the wavefunction scales with the nuclear charge \\(Z\\):

$$ \psi(r) \sim e^{-Zr/n a_0} $$

As you increase $Z$ using the **Alchemist's Dial**, the exponent grows larger, causing the wavefunction to decay much faster with distance. Visually, this results in the orbital "contracting" or shrinking toward the nucleus, a fundamental demonstration of why atoms become smaller as you move right across a period in the Periodic Table.

### 3. Data Sonification (The Quantum Hum)
Molecular orbitals are fundamentally three-dimensional probability waves. In **The Quantum Hum**, we map the total energy of a specific quantum state to an acoustic frequency. This allows us to "hear" the stability of a system:

- **Lower Frequency:** Lower energy (more stable state).
- **Higher Frequency:** Higher energy (less stable or "tense" state).

By sonifying the data, we provide a multi-sensory bridge to understanding the "tension" in a chemical bond as it is stretched or polarized.

### 4. Attosecond Science & Dynamic Density
Traditionally, chemistry is taught using stationary orbitals (the time-independent Schrödinger equation). However, the **2023 Nobel Prize in Physics** was awarded for **Attosecond Pulses**, which allow us to observe electrons as they move in real-time.

In **The Attosecond Movie**, we visualize the **Total Electron Density** $\rho(r, t)$. This is done by simulating a coherent superposition of the ground state and the first excited state (calculated via Time-Dependent Hartree-Fock, or TDHF). As the phase of the excited state changes over time, the electron density physically "sloshes" back and forth across the molecule, demonstrating the dynamic nature of chemical transitions.

## Molecular Orbitals (MOs)

Molecular orbitals (MOs) are mathematical functions that describe the location and wave-like behavior of an electron in a molecule. 

### Probability Density
The physical interpretation of the wavefunction is that its square, $|\Psi|^2$, represents the **probability density** of finding an electron at a specific point in space.

### Phases
The colors you see in the visualization (Blue and Red) represent the **phase** (sign) of the wavefunction $\Psi$. Phase is crucial for understanding how orbitals overlap to form bonds (constructive interference) or create nodes (destructive interference).
