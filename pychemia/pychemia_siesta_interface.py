import pychemia

#create siesta interface object
si = pychemia.code.siesta.SiestaInput('/shared/atomistic/siesta/siesta-4.0.1/Tests/h2o/h2o.fdf')

#display the object contents
si.variables

#write a fdf file
si.write('h2o.fdf')

#create siesta run object DOES NOT WORK!
sr=pychemia.code.siesta.SiestaRun(workdir='.', input_path='h2o.fdf', pseudo_path='/shared/atomistic/siesta/siesta-4.0.1/Tests/Pseudos/', pseudo_list=['H', 'O'])

#or
sr=pychemia.code.siesta.SiestaRun(workdir='.', input_path='h2o.fdf', pseudo_path='/shared/atomistic/siesta/siesta-4.0.1/Tests/Pseudos/', pseudo_file='/shared/atomistic/siesta/siesta-4.0.1/Tests/h2o/h2o.pseudos')

sr.set_inputs()
sr.run()
