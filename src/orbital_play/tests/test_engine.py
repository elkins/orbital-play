import pytest
from orbital_play import engine
import os

def test_generate_geometry_h2():
    geo = engine.generate_geometry("H2", dist=0.74)
    assert "H 0 0 0" in geo
    assert "H 0 0 0.74" in geo

def test_generate_geometry_h2o():
    geo = engine.generate_geometry("H2O", dist=1.0, angle=90.0)
    assert "O 0 0 0" in geo
    # For 90 deg, x = 1 * sin(45) = 0.707, z = 1 * cos(45) = 0.707
    assert "0.707" in geo

def test_generate_geometry_ch4():
    geo = engine.generate_geometry("CH4", dist=1.09)
    assert "C 0 0 0" in geo
    assert "H" in geo
    assert geo.count("H") == 4

def test_generate_geometry_invalid():
    with pytest.raises(ValueError):
        engine.generate_geometry("Unknown")

def test_run_calculation():
    geometry = "H 0 0 0; H 0 0 0.74"
    mol, mf = engine.run_calculation(geometry)
    assert mf.converged
    assert mol.nelectron == 2
    summary = engine.get_molecule_summary(mol, mf)
    assert summary['converged']
    assert len(summary['mo_energies']) > 0

def test_generate_cube_string():
    geometry = "H 0 0 0; H 0 0 0.74"
    mol, mf = engine.run_calculation(geometry)
    cube_data = engine.generate_cube_string(mol, mf, 0, nx=10, ny=10, nz=10)
    assert "PySCF" in cube_data
    assert "Orbital" in cube_data
    assert len(cube_data) > 0

def test_generate_geometry_oh():
    geo = engine.generate_geometry("OH", dist=0.97)
    assert "O 0 0 0" in geo
    assert "H 0 0 0.97" in geo

def test_run_calculation_uhf():
    # OH radical, spin=1
    geometry = "O 0 0 0; H 0 0 0.97"
    mol, mf = engine.run_calculation(geometry, spin=1)
    assert mf.converged
    assert mol.nelectron == 9
    summary = engine.get_molecule_summary(mol, mf)
    assert summary['converged']
    # Check that energies are separated into alpha and beta
    assert 'alpha' in summary['mo_energies']
    assert 'beta' in summary['mo_energies']
    assert len(summary['mo_energies']['alpha']) == len(summary['mo_energies']['beta'])

def test_generate_cube_string_uhf():
    geometry = "O 0 0 0; H 0 0 0.97"
    mol, mf = engine.run_calculation(geometry, spin=1)
    # Test alpha
    cube_alpha = engine.generate_cube_string(mol, mf, 0, spin_type='alpha', nx=10, ny=10, nz=10)
    assert "PySCF" in cube_alpha
    # Test beta
    cube_beta = engine.generate_cube_string(mol, mf, 0, spin_type='beta', nx=10, ny=10, nz=10)
    assert "PySCF" in cube_beta

def test_calculate_dissociation_curve():
    distances = [0.74, 1.5, 3.0]
    rhf, uhf = engine.calculate_dissociation_curve("H2", distances)
    assert len(rhf) == len(distances)
    assert len(uhf) == len(distances)
    # At large distance, UHF should be lower than RHF (symmetry breaking)
    assert uhf[2] < rhf[2]

def test_get_attosecond_frames():
    geometry = "H 0 0 0; H 0 0 0.74"
    mol, mf = engine.run_calculation(geometry)
    frames = engine.get_attosecond_frames(mol, mf, n_frames=3)
    assert len(frames) == 3
    assert "PySCF" in frames[0]
    assert "density" in frames[0]
