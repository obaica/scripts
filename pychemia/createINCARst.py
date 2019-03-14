#!/usr/bin/env python

# Reading PyChemia database entries

import pychemia

#setup database connection
dbsettings={'host': 'mongo01.systems.wvu.edu', 'name': 'PyChemiaMasterDB', 'user':'guest', 'passwd': 'aldo', 'ssl': True}
pcdb=pychemia.db.get_database(dbsettings)

#Get structure information for a certain ID    
st=pcdb.get_structure('3_La2NiO4_000000000000010137')
print(st)

#Generate a POSCAR file for the structure
pychemia.code.vasp.write_poscar(st)

#Generate INCAR for the structure
vi=pychemia.code.vasp.VaspInput('INCAR.inp')
nspecies=st.nspecies
arr=nspecies*[0]
arr[0] = params['U']
vi['LDAUU']=arr
arr=nspecies*[0]
arr[0] = params['J']
vi['LDAUJ']=arr
vi.write('INCAR')
