# Reading PyChemia database entries

import pychemia

#setup database connection
dbsettings={'host': 'mongo01.systems.wvu.edu', 'name': 'PyChemiaMasterDB', 'user':'guest', 'passwd': 'aldo', 'ssl': True}
pcdb=pychemia.db.get_database(dbsettings)

#total number of entries
pcdb.entries.count()

#returns one entry from the database
pcdb.entries.find_one()

#a structure with 6 atoms and 3 species (ex: 2Cl, 2In, 2O)
pcdb.entries.find_one({'structure.natom': 6, 'structure.nspecies': 3})

#return a structure with La in it
pcdb.entries.find_one({'structure.symbols': {'$in': ['La']} })

#count how many structures like that there are
pcdb.entries.count({'structure.symbols': {'$in': ['La']} }) 


#Count the number of structures with La, Ni and O (May contain other species too)
pcdb.entries.count({'$and': [ {'structure.symbols': {'$in': ['La']}}, {'structure.symbols': {'$in': ['Ni']}},{'structure.symbols': {'$in': ['O']} }]})

#Count the number of structures with La,Ni and O which only have 3 species
pcdb.entries.count({'$and': [ {'structure.symbols': {'$in': ['La']}}, {'structure.symbols': {'$in': ['Ni']}},{'structure.symbols': {'$in': ['O']} }], 'structure.nspecies': 3})

#Find an entry with La,Ni and O with only 3 species
pcdb.entries.find_one({'$and': [ {'structure.symbols': {'$in': ['La']}}, {'structure.symbols': {'$in': ['Ni']}},{'structure.symbols': {'$in': ['O']} }], 'structure.nspecies': 3})

#Return the ID of the queried entry
pcdb.entries.find_one({'$and': [ {'structure.symbols': {'$in': ['La']}}, {'structure.symbols': {'$in': ['Ni']}},{'structure.symbols': {'$in': ['O']} }], 'structure.nspecies': 3},{'_id':1})

#Print ID's of all searches with a specific criteria
for i in pcdb.entries.find({'$and': [ {'structure.symbols': {'$in': ['La']}}, {'structure.symbols': {'$in': ['Ni']}},{'structure.symbols': {'$in': ['O']} }], 'structure.nspecies': 3},{'_id':1}):
    print(i)

#Get structure information for a certain ID    
st=pcdb.get_structure('3_La2NiO4_000000000000010137')
print(st)

#Generate a POSCAR file for the structure
pychemia.code.vasp.write_poscar(st)


get_ipython().run_line_magic('cat', 'POSCAR')
get_ipython().run_line_magic('pinfo', 'pcdb.find_AnBm')
pychemia.runner.get_jobs('gufranco')
pychemia.runner.PBSRunner()
job=pychemia.runner.PBSRunner()
job.set_pbs_params(nodes=1,ppn=4, walltime=[4,0,0] )
print(job)
pychemia.utils.periodic.atomic_symbols
pychemia.utils.periodic.groups
pychemia.utils.periodic.group('O')
pychemia.utils.periodic.covalent_radius('La')
pychemia.utils.periodic.covalent_radius(['La','O', 'In'])
pychemia.utils.periodic.atomic_number(['La','O', 'In'])
get_ipython().run_line_magic('pinfo', 'pychemia.utils.computing.convert_color')
pychemia.utils.serializer(3.4)
pychemia.utils.serializer.generic_serializer(342434.3)
import numpy as np
np.random.rand(10)
a=np.random.rand(10)
a
pychemia.utils.serializer.generic_serializer(a)
