# IPython log file

import pychemia

dbsettings={'host': 'mongo01.systems.wvu.edu', 'name': 'PyChemiaMasterDB', 'user': 'guilleaf', 'passwd': 'zxcvbnm', 'ssl': True}

pcdb=pychemia.db.get_database(dbsettings)
selection={ '$and': [ {'properties.blocks': { '$in': ['d']}}, 
                      {'structure.symbols': {'$in': ['F']}},   
                      {'structure.nspecies': 3},                              ##  Three species only
                      {'structure.natom': { '$gt': 4}},                       ## find all structures having more than 4 atoms
                      {'properties.oqmd.energy_pa': { '$lt': 0}}]}            ### Find all structures with formation energy per atom less than 0

print('Number of Structures: %d' % pcdb.entries.find(selection, no_cursor_timeout=True).count())

cursor=pcdb.entries.find(selection, no_cursor_timeout=True)
for entry in cursor:
    # Identifier
    entry_id = entry['_id']
    st=pcdb.get_structure(entry['_id'])
    sym=pychemia.crystal.symmetry.CrystalSymmetry(st)
    pg=sym.get_symmetry_dataset()['pointgroup']
#    bandgap=entry['properties']['oqmd']['band_gap']

## filter structures having 3 or 4 (or integer multiple) of 'F' atoms. 
    comp = st.composition
    if comp['F']%3.0 == 0 or comp['F']%4 ==0:

#    print(entry['properties']['oqmd'])

## print  BANDGAP
#        print('%10s       natoms: %3d       SpaceGroup: %5d     %14s      PointGroup: %5s      BandGap(eV): %6.3f' % (entry['structure']['formula'], 
#                                                                                      entry['structure']['natom'], 
#                                                                                      entry['properties']['spacegroup']['number'], 
#                                                                                      entry['properties']['spacegroup']['crystal_system'], 
#                                                                                      pg, bandgap))

      print('%10s       natoms: %3d       SpaceGroup: %5d     %14s      PointGroup: %5s ' % (entry['structure']['formula'], 
                                                                                      entry['structure']['natom'],
                                                                                      entry['properties']['spacegroup']['number'],
                                                                                      entry['properties']['spacegroup']['crystal_system'],
                                                                                      pg))

## print POSCAR for each obtained structure
#       pychemia.code.vasp.write_poscar(st,'%s_%s_%03d_POSCAR' % (entry_id, st.formula,sym.number()))
