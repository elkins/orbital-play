# Theoretical Background

OrbitalPlay uses established principles of computational chemistry to visualize the invisible.

## The Schrödinger Equation

At the heart of the engine is the time-independent Schrödinger Equation:

\\[ \hat{H}\Psi = E\Psi \\]

Where:
- \\(\hat{H}\\) is the Hamiltonian operator representing the total energy.
- \\(\Psi\\) is the wavefunction.
- \\(E\\) is the energy of the system.

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

## Molecular Orbitals (MOs)
...

Molecular orbitals are mathematical functions that describe the location and wave-like behavior of an electron in a molecule. 

### Probability Density
The physical interpretation of the wavefunction is that its square, \\(|\Psi|^2\\), represents the **probability density** of finding an electron at a specific point in space.

### Phases
The colors you see in the visualization (Blue and Red) represent the **phase** (sign) of the wavefunction \\(\Psi\\). Phase is crucial for understanding how orbitals overlap to form bonds (constructive interference) or create nodes (destructive interference).
