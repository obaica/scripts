# INCAR Change
import pychemia

vi=pychemia.code.vasp.VaspInput('INCAR.inp')
nspecies=st.nspecies
arr=nspecies*[0]
arr[0] = params['U']
vi['LDAUU']=arr
arr=nspecies*[0]
arr[0] = params['J']
vi['LDAUJ']=arr
vi.write('INCAR')