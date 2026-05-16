import py3Dmol

def show_orbital(mol, cube_data, isoval=0.05, width=600, height=400):
    """
    Renders an interactive 3D visualization of a molecular orbital 
    suitable for Jupyter and Google Colab cells.
    """
    xyz_str = mol.tostring(format='xyz')
    
    view = py3Dmol.view(width=width, height=height)
    view.addModel(xyz_str, 'xyz')
    view.setStyle({'stick': {}, 'sphere': {'scale': 0.3}})
    
    # Add volumetric data (orbitals)
    view.addVolumetricData(cube_data, "cube", {'isoval': isoval, 'color': "blue", 'opacity': 0.6})
    view.addVolumetricData(cube_data, "cube", {'isoval': -isoval, 'color': "red", 'opacity': 0.6})
    
    view.zoomTo()
    return view.show()
