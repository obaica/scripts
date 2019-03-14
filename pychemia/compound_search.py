import pychemia

#setup database connection
dbsettings={'host': 'mongo01.systems.wvu.edu', 'name': 'PyChemiaMasterDB', 'user':'guest', 'passwd': 'aldo', 'ssl': True}
pcdb=pychemia.db.get_database(dbsettings)

for i in pcdb.entries.find({'$and': [{'structure.symbols': {'$in': ['N']}},{'structure.symbols': {'$in': ['O']} }], 'structure.nspecies': 4},{'_id':1}):
	st = pcdb.get_structure(i['_id'])
	composition = st.get_composition() #Composition({u'H': 16, u'V': 4, u'O': 12, u'N': 4})
	stoch = [composition[x] for x in composition] #[16, 4, 12, 4]
	other_two_species = [x for x in composition if x != 'O' and x!= 'N'] #[u'H', u'V']
	gcd = stoch[0]
	for i in stoch: #[16, 4, 12, 4]
		gcd = fractions.gcd(gcd,i) #4
	if composition['O']/gcd == 2 and composition['N']/gcd == 1 and composition[other_two_species[0]]/gcd == 1 and composition[other_two_species[1]]/gcd == 1:
		print(st.formula)