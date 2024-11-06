from ase.io import read, write
from ase.visualize import view
from ase.build.tools import sort
atoms =  read('EDAI.png_slab.vasp')
#atoms = sort(atoms)
#write('POSCAR', atoms, format='vasp')
view(atoms) 
