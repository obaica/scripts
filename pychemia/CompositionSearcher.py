#!/usr/bin/env python

from __future__ import print_function
import pychemia
import os


def searcher_n(pcdb, entry_id, entries_dict, formula_name, prescription):
    """
    Search for incremental values on n if the formula can match with the prescription given
    by the numerator and denominators

    Example:

    You have a formula such as La4Ti4O14, and we are searching for An Bn X3n+1

    The prescription is a string with the list of values, ie  '[n, n, 3*n+1]'
    The formula_name is just the label used to store the values into the dictionary entries_dict
    The variable entries_dict stores all the entry_id for the cases that match the search

    """
    # Get the structure from the Mongo ID value
    st=pcdb.get_structure(entry_id)
    # Get the composition object from the structure
    comp=st.get_composition()
    # Number of atoms of each specie
    n_atoms_specie = sorted([ int(x) for x in comp.values])
 
    n=1
    while True:
        sum_prescription = sum(eval(prescription))
        # The evaluation with natom makes calculations faster
        if comp.natom == sum_prescription and n_atoms_specie == sorted(eval(prescription)):
            if formula_name not in entries_dict:
                entries_dict[formula_name]=[]
            entries_dict[formula_name].append(entry_id)
            print("%-20s Formula: %20s    N=%3d    N_atoms_specie: %s" % (formula_name, st.formula, n, n_atoms_specie))
            break
        # As n increases the value of sum_prescrition does too. 
        # We stop when the value of n is such that sum_prescription is larger than the number of atoms.
        if comp.natom < sum_prescription:
            break
        n+=1



db_settings={'name': 'PyChemiaMasterDB', 'host': 'mongo01.systems.wvu.edu', 'user':'guilleaf', 'passwd': 'zxcvbnm', 'ssl': True}
pcdb=pychemia.db.get_database(db_settings)

entries_dict={}

# Binary
print('Binary search')
#for entry in  pcdb.entries.find({'structure.nspecies':2, 'properties.oqmd.energy': {'$lt': 0}},{'_id':1}):
for entry in  pcdb.entries.find({'structure.nspecies':2},{'_id':1}):
    entry_id = entry['_id']

    searcher_n(pcdb, entry_id, entries_dict, 'BnX3n', '[n, 3*n]')
    
print('')

# Ternary
print('Ternary search')
#for entry in  pcdb.entries.find({'structure.nspecies':3, 'properties.oqmd.energy': {'$lt': 0}},{'_id':1}):
for entry in  pcdb.entries.find({'structure.nspecies':3},{'_id':1}, no_cursor_timeout=True):
    entry_id = entry['_id']

    searcher_n(pcdb, entry_id, entries_dict, 'AnBnX3n', '[n, n, 3*n]')
    searcher_n(pcdb, entry_id, entries_dict, 'AnBnX4n', '[n, n, 4*n]')
    searcher_n(pcdb, entry_id, entries_dict, 'AnBnX3n+1', '[n, n, 3*n+1]')
    searcher_n(pcdb, entry_id, entries_dict, 'An+1BnX3n+1', '[n+1, n, 3*n+1]')

    # This formulas speficially target O in the formula, we will get all and after remove the false positives
    searcher_n(pcdb, entry_id, entries_dict, 'AnBnX3n+2', '[n, n, 3*n+2]')
    searcher_n(pcdb, entry_id, entries_dict, 'AnBn-1X3n', '[n, n-1, 3*n]')

entries_dict['AnBn-1O3n'] = list(entries_dict['AnBn-1X3n'])
entries_dict['AnBnO3n+2'] = list(entries_dict['AnBnX3n+2'])

# Removing false positivies from the previous step
to_remove=[]
for entry_id in entries_dict['AnBnO3n+2']:
    # Get the structure from the Mongo ID value
    st=pcdb.get_structure(entry_id)
    # Get the composition object from the structure
    comp=st.get_composition()
    n_atoms_specie = sorted([ int(x) for x in comp.values])
    # The value of n comes from the lowest number of atoms in the formula
    n = n_atoms_specie[0]
    if 'O' in comp and comp['0'] == 3*n+2:
        print("This formula is accepted:     %s" % st.formula)
    else:
        print("This formula is not accepted: %s" % st.formula)
        to_remove.append(entry_id)

for i in to_remove:
    entries_dict['AnBnO3n+2'].remove(i)

to_remove=[]
for entry_id in entries_dict['AnBn-1O3n']:
    # Get the structure from the Mongo ID value
    st=pcdb.get_structure(entry_id)
    # Get the composition object from the structure
    comp=st.get_composition()
    n_atoms_specie = sorted([ int(x) for x in comp.values])
    # The value of n comes from the second number of atoms in the formula, the lowest is n-1
    n = n_atoms_specie[1]
    if 'O' in comp and comp['0'] == 3*n:
        print("This formula is accepted:     %s" % st.formula)
    else:
        print("This formula is not accepted: %s" % st.formula)
        to_remove.append(entry_id)

for i in to_remove:
    entries_dict['AnBn-1O3n'].remove(i)


print("Number of cases found for each formula")
for icase in entries_dict:
    print("%20s : %d" % (icase, len(entries_dict[icase])))

for icase in entries_dict:
    if not os.path.isdir(icase):
        os.mkdir(icase)
    if not os.path.isdir(icase+'_NE'):
        os.mkdir(icase+'_NE')
    for j in entries_dict[icase]:
        entry=pcdb.entries.find_one({'_id':j},{'properties.oqmd':1})
        st=pcdb.get_structure(j)
        sym=pychemia.crystal.CrystalSymmetry(st)

        if 'properties' not in entry or 'oqmd' not in entry['properties'] or 'energy' not in entry['properties']['oqmd']:
            print('ERROR: Bad DataBase Fields on %s' % j)
            print(entry)
        else:
            if entry['properties']['oqmd']['energy'] is not None and entry['properties']['oqmd']['energy'] < 0:
                comment='Energy: %f Energy_pa: %f SpaceGroup: %d' % (entry['properties']['oqmd']['energy'], entry['properties']['oqmd']['energy_pa'], sym.number())
                pychemia.code.vasp.write_poscar(st,"%s/%s_SPG%03d" % (icase,str(j),sym.number()), comment=comment)
            else:
                pychemia.code.vasp.write_poscar(st,"%s_NE/%s_SPG%03d" % (icase,str(j),sym.number()))
