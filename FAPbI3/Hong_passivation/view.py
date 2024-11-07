from ase.io import read, write
from ase.visualize import view
from ase.build.tools import sort
atoms =  read('DMePDAI.png_slab.vasp')
atoms = sort(atoms)
#write('PDAI.pdb', atoms, format='proteindatabank')
view(atoms) 
