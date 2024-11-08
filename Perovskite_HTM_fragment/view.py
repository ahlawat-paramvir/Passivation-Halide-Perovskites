from ase.visualize import view
from ase.io import read, write

atoms = read('slab_HTM/2,7-Dibromophenanthrene-9,10-dione_slab.vasp')

view(atoms)
