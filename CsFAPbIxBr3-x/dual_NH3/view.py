from ase.io import read, write
from ase.visualize import view
from ase.build.tools import sort
atoms =  read('BDAI.vasp')
atoms = sort(atoms)
view(atoms) 
