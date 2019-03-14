import pychemia

dbsettings={'host': 'mongo01.systems.wvu.edu', 'name': 'PyChemiaMasterDB', 'user':'guest', 'passwd': 'aldo', 'ssl': True}
pcdb=pychemia.db.get_database(dbsettings)

st=pcdb.get_structure('6_BaC2H6N2O3S2_0000000006180')
print(st)

abi=pychemia.code.abinit.AbinitInput()
abi.from_structure(st)
print(abi)

abi.set_variable('ecut',15)
abi.write('abinit.in')
