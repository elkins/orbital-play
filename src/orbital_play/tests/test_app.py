from streamlit.testing.v1 import AppTest
import pytest

def test_app_smoke():
    """Basic smoke test to ensure the app loads."""
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert "OrbitalPlay" in at.title[0].value

def test_molecule_selection_updates_sliders():
    """Verify that changing the molecule type updates the sidebar controls."""
    at = AppTest.from_file("app.py").run()
    
    # Select H2O - the first selectbox is the molecule selector
    at.selectbox[0].select("H2O").run()
    
    # Should have O-H Bond Distance and H-O-H Angle sliders
    slider_labels = [s.label for s in at.slider]
    assert "O-H Bond Distance (Å)" in slider_labels
    assert "H-O-H Angle (degrees)" in slider_labels

def test_calculation_summary_renders():
    """Verify that the calculation summary is displayed."""
    at = AppTest.from_file("app.py").run()
    
    # Check for subheaders in the summary column
    subheaders = [s.value for s in at.subheader]
    assert "Calculation Summary" in subheaders
    assert "MO Energies" in subheaders

def test_spin_toggle_appears_for_radical():
    """Verify that the spin channel radio button appears when OH (Radical) is selected."""
    at = AppTest.from_file("app.py").run()
    
    # Select OH (Radical)
    at.selectbox[0].select("OH (Radical)").run()
    
    # Check for the radio button
    assert len(at.radio) > 0
    assert at.radio[0].label == "Spin Channel"
    assert "Alpha (↑)" in at.radio[0].options
    assert "Beta (↓)" in at.radio[0].options
