import py3Dmol
try:
    from ipywidgets import interact, FloatSlider, IntSlider
    HAS_WIDGETS = True
except ImportError:
    HAS_WIDGETS = False

def show_orbital(mol, cube_data, isoval=0.05, width=600, height=400, wand_pos=None, wand_charge=0.0):
    """
    Renders an interactive 3D visualization of a molecular orbital 
    suitable for Jupyter and Google Colab cells.
    """
    xyz_str = mol.tostring(format='xyz')
    
    view = py3Dmol.view(width=width, height=height)
    view.addModel(xyz_str, 'xyz')
    view.setStyle({'stick': {}, 'sphere': {'scale': 0.3}})
    
    # Add labels for atoms
    for i in range(mol.natm):
        symb = mol.atom_symbol(i)
        coord = mol.atom_coord(i) * 0.529177 # Bohr to Angstrom
        view.addLabel(symb, {'position': {'x': coord[0], 'y': coord[1], 'z': coord[2]}, 
                             'backgroundColor': 'gray', 'fontColor': 'white', 'fontSize': 10, 'opacity': 0.6})

    # Add the Stark Wand if present
    if wand_pos is not None:
        wand_color = "#FFD700" if wand_charge > 0 else "#9932CC" # Gold or Dark Orchid
        view.addSphere({'center': {'x': wand_pos[0], 'y': wand_pos[1], 'z': wand_pos[2]}, 
                        'radius': 0.4, 'color': wand_color, 'opacity': 0.8})
        view.addLabel(f"q={wand_charge:+.1f}", {'position': {'x': wand_pos[0], 'y': wand_pos[1], 'z': wand_pos[2]}, 
                                               'backgroundColor': 'white', 'fontColor': 'black', 'fontSize': 12})

    # Add volumetric data (orbitals)
    view.addVolumetricData(cube_data, "cube", {'isoval': isoval, 'color': "blue", 'opacity': 0.6})
    view.addVolumetricData(cube_data, "cube", {'isoval': -isoval, 'color': "red", 'opacity': 0.6})
    
    view.zoomTo()
    return view.show()

def interactive_wand(engine, molecule_type="H2O", mo_index=4):
    """
    Creates an interactive widget for the Stark Wand.
    Requires ipywidgets.
    """
    if not HAS_WIDGETS:
        print("ipywidgets not installed. Dynamic repositioning unavailable.")
        return
    
    def update(x, y, z, charge):
        geo = engine.generate_geometry(molecule_type)
        mol, mf = engine.run_calculation(geo, wand_coords=(x, y, z), wand_charge=charge)
        cube = engine.generate_cube_string(mol, mf, mo_index=mo_index)
        
        # Print energy for the "Challenge"
        print(f"Total Energy: {mf.e_tot:.6f} Ha")
        
        return show_orbital(mol, cube, wand_pos=(x, y, z), wand_charge=charge)
    
    return interact(update, 
             x=FloatSlider(min=-5, max=5, step=0.1, value=2.0, description='Wand X'),
             y=FloatSlider(min=-5, max=5, step=0.1, value=0.0, description='Wand Y'),
             z=FloatSlider(min=-5, max=5, step=0.1, value=0.0, description='Wand Z'),
             charge=FloatSlider(min=-2, max=2, step=0.1, value=1.0, description='Charge'))
