from ase.io import read, write
from ase.visualize import view
from ase.build.tools import sort
atoms =  read('slab_HTM/Dimethyl 2,5-dibromoterephthalate_slab.vasp')
atoms = sort(atoms)
view(atoms) 
