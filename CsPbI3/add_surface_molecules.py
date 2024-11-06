import matplotlib.pyplot as plt
from ase import io
from ase.visualize import view
from ase.visualize.plot import plot_atoms

def automate_adsorption(slab_file, molecule_file, num_replace_Cs=2, output_file=None):
    """
    Automates the adsorption process by replacing specified number of Cs atoms
    in a slab with a given molecule.
    
    Parameters:
        slab_file (str): Path to the slab VASP file.
        molecule_file (str): Path to the molecule PDB file.
        num_replace_Cs (int): Number of Cs atoms to replace.
        output_file (str): Optional path to save the new slab structure.
    """
    try:
        # Read the slab
        relaxed_slab = io.read(slab_file)
    except Exception as e:
        print(f"Error reading slab file: {e}")
        return

    try:
        # Initialize temporary molecule storage
        tmp_molecule = []

        for j in range(num_replace_Cs):
            num_atoms = len(relaxed_slab.get_chemical_symbols())
            Cs_index = [(relaxed_slab.positions[i, 2], i) 
                         for i in range(num_atoms) 
                         if relaxed_slab.get_chemical_symbols()[i] == 'Cs']

            if not Cs_index:
                print("No Cs atoms found for replacement.")
                break

            # Get the index of the Cs atom with the maximum z value
            max_value_z, idz = max(Cs_index, key=lambda item: item[0])

            # Read the molecule and set its position
            molecule = io.read(molecule_file)
            molecule.set_cell(relaxed_slab.cell)
            molecule.positions += relaxed_slab.positions[idz] - molecule.get_center_of_mass()

            # Store the molecule and remove the replaced Cs atom
            tmp_molecule = molecule if j == 0 else tmp_molecule + molecule
            del relaxed_slab[idz]

        # Combine the relaxed slab and the new molecule
        new_slab = relaxed_slab + tmp_molecule

        # Visualize the structures
        fig, axes = plt.subplots(1, 3, figsize=(20, 10))
        visualize_structure(slab_file, new_slab, axes)

        # Save the final structure to a VASP file if specified
        if output_file:
            io.write(output_file, new_slab, vasp5=True, direct=True)
            print(f"Saved new slab structure to {output_file}")

    except Exception as e:
        print(f"An error occurred during the process: {e}")

def visualize_structure(slab_file, new_slab, axes):
    """
    Visualizes the original and new slab structures.

    Parameters:
        slab_file (str): Path to the slab file.
        new_slab (Atoms): The new slab with adsorbates.
        axes (list): List of axes for plotting.
    """
    # Plot original slab
    slab = io.read(slab_file)
    plot_atoms(slab, axes[0], radii=0.5, rotation=('90x,0y,0z'))
    axes[0].set_xlim(-20, 30)
    axes[0].set_xlabel(r'x[$\AA$]')
    axes[0].set_ylabel(r'z[$\AA$]')
    axes[0].set_title('Original Slab')

    # Plot new slab
    plot_atoms(new_slab, axes[1], radii=0.5, rotation=('90x,0y,0z'))
    axes[1].set_xlim(-20, 30)
    axes[1].set_xlabel(r'x[$\AA$]')
    axes[1].set_ylabel(r'z[$\AA$]')
    axes[1].set_title('New Slab with Adsorbates')

    # Side view of the new slab
    plot_atoms(new_slab, axes[2], radii=0.5, rotation=('0x,0y,0z'))
    axes[2].set_xlabel(r'x[$\AA$]')
    axes[2].set_ylabel(r'y[$\AA$]')
    axes[2].set_title('Side View of New Slab')

    plt.tight_layout()
    plt.show()

# Example usage
automate_adsorption('slab_hexagonal_relaxed.vasp', 'DMA.pdb', num_replace_Cs=2, output_file='delta_001_2DMA_top.vasp')
