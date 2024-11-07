from ase.io import read, write
from ase.visualize import view
from ase.build.tools import sort
atoms =  read('PDAI_only.pdb')
atoms = sort(atoms)
write('PDAI_only.vasp', atoms, format='vasp')
view(atoms) 
