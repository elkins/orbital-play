# Developer Guide

Welcome to the internal workings of OrbitalPlay. This guide explains the architecture and how to extend the tool.

## Architecture Overview

OrbitalPlay is split into two primary layers:

### 1. The Quantum Engine (`quantum_engine.py`)
This is a clean wrapper around the **PySCF** library. Its responsibilities are:
- **Geometry Generation:** Calculating XYZ coordinate strings for molecules based on physical parameters (dist, angle).
- **SCF Execution:** Executing the `scf.RHF` calculation.
- **Cube Generation:** Generating Gaussian Cube files using `cubegen.orbital`.
- **Metadata:** Extracting calculation summaries.

### 2. The Interactive Frontend (`app.py`)
Built with **Streamlit**, this layer handles:
- User interaction via sidebar widgets.
- Triggering the engine and retrieving results.
- Rendering the 3D visual using `py3Dmol`.
- **Caching:** Optimized caching reuses the SCF resource for cube generation, significantly improving responsiveness when adjusting visual settings.

## Testing

OrbitalPlay includes a comprehensive test suite using `pytest`.

### Running Tests
To run all tests (unit and UI):
```bash
pytest tests/
```

> **Note:** We have explicitly suppressed several `RuntimeWarning` messages (divide by zero, overflow) that occur within the PySCF `cubegen` module. These are known numerical artifacts in the underlying library's coordinate transformation logic and do not affect the accuracy of the generated orbital visualizations.

### Test Structure
- `tests/test_engine.py`: Unit tests for molecular geometry formulas and Hartree-Fock convergence.
- `tests/test_app.py`: UI and integration tests using Streamlit's `AppTest` to verify widget behavior and rendering.

## Adding a New Molecule
...
2. Add the molecule's coordinate logic to the `generate_geometry` function in `quantum_engine.py`.
3. Update the `molecule_type` selectbox and slider logic in `app.py`.
4. Add a corresponding test case in `tests/test_engine.py`.

## Extending the Engine

The engine currently uses the **STO-3G** basis set for speed. If you want to add support for more accurate basis sets (like `6-31G*`), you can modify the `run_calculation` function in `quantum_engine.py`. Note that larger basis sets will increase the calculation time and might affect the "real-time" feel of the app.

## Development Setup

To contribute to the documentation:
1. Install doc dependencies: `pip install -r docs-requirements.txt`
2. Start the live preview: `mkdocs serve`
3. Edit files in the `docs/` directory.
