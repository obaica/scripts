import numpy as np
import matplotlib.pylab as plt
import argparse
from matplotlib.ticker import AutoMinorLocator
import re
from matplotlib import rc
import pychemia


def get_procar(file_name,ret_type='matrix'):
    st = pychemia.code.vasp.read_poscar('POSCAR')
    cell_cv = st.cell
    rf = open(file_name)
    PROCAR = rf.read()
    rf.close()
    
    data = {}
    raw_kpoints = re.findall('k-point\s*([0-9]*)\s*:\s*([\s-][0-9]*[.][0-9]*)\s*([\s-][0-9]*[.][0-9]*)\s*([\s-][0-9]*[.][0-9]*)\s*weight\s*=\s*([\s-][0-9]*[.][0-9]*)',PROCAR)
    for x in raw_kpoints:
        data[int(x[0])] = {}
        data[int(x[0])]['kpoints'] = [float(x[1]),float(x[2]),float(x[3])]
    for x in data :
        raw_kpoints_bands = re.findall('k-point\s*'+str(x)+'\s:[a-z0-9\n\s\t.=#+-]*',PROCAR)[0]
        kpoints_bands = re.findall('band\s*([0-9]*)\s*#\senergy\s*([0-9.+-]*)',raw_kpoints_bands)
        data[x]['bands'] = {}
        for y in kpoints_bands :
            data[x]['bands'][int(y[0])] = float(y[1])
    if ret_type == 'dictionary':
        return data
    elif ret_type == 'matrix':
        nkpoints = len(data)
        nbands   =len(data[1]['bands'])
        ########################################################
        #  data_matrix shape :                                 #
        #  --------------------------------------------------- #
        #  | ikpoint | kx | ky | kz | iband | energy of band | #
        #  --------------------------------------------------- #
        ########################################################
        data_matrix = np.zeros(shape=(nkpoints*nbands,1+3+1+1))
        irow = 0
        for ikpoint in data:
            for iband in range(0,nbands) :
                data_matrix[irow,0] = ikpoint
                kx = data[ikpoint]['kpoints'][0]
                ky = data[ikpoint]['kpoints'][1]
                kz = data[ikpoint]['kpoints'][2]
                data_matrix[irow,1] = kx
                data_matrix[irow,2] = ky
                data_matrix[irow,3] = kz
                data_matrix[irow,4] = iband
                data_matrix[irow,5] = data[ikpoint]['bands'  ][iband+1]
                irow += 1
        return data_matrix
        
def get_fermi(file_name):
    rf = open(file_name,'r')
    data = rf.read()
    rf.close()
    e_fermi = float(re.findall('E-fermi\s*:\s*([0-9.+-]*)',data)[0])
    return e_fermi
        


parser = argparse.ArgumentParser()
parser.add_argument('-legend',nargs='+',help='legen list')
parser.add_argument('-xlim',nargs=2,type=int,help='x limits')
parser.add_argument('-ylim',nargs=2,type=float,help='y limits')
parser.add_argument('-title',help='plot title')

rc('text', usetex=True)
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.family'] = 'serif'
args = parser.parse_args()


try :
    f = open('KPOINTS')
    lines = f.readlines()
    f.close()
    f = open('KPOINTS')
    KP = f.read()
    f.close()
except :
    print("There is no file named KPOINTS")
KP1 = re.findall('reciprocal[\s\S]*',KP)
tick_labels_raw = np.array(re.findall('!\s(.*)',KP1[0]))
nkpoint = int(lines[1].split()[0])

high_symm_kpoints = np.array([x.split() for x in re.findall("(.*)!\s.*",KP)[1:]]).astype(np.float)
high_symm_distances = []
for ix in range(1,len(high_symm_kpoints),2):
    high_symm_distances.append(np.linalg.norm(high_symm_kpoints[ix]-high_symm_kpoints[ix-1]))
high_symm_distances = np.array(high_symm_distances)/sum(high_symm_distances)

fig , ax = plt.subplots(figsize=(11,8))

data = get_procar("PROCAR")
data[:,5] += -1*get_fermi("OUTCAR")
bands = np.unique(data[:,4]).astype(int)
nkp_total = len(np.unique(data[:,0]))

x_range = np.linspace(0,nkp_total-1,nkp_total)
tick_pos = []
for band in bands :
    idx = data[:,4] == band
    x_place_holder = 0
    for isym_point in range(len(high_symm_distances)):
        if band == 1 : 
            tick_pos.append(x_place_holder)
        x = np.linspace(x_place_holder,x_place_holder+high_symm_distances[isym_point],nkpoint)
        x_place_holder += high_symm_distances[isym_point]
        y = data[idx,5][isym_point*nkpoint:(isym_point+1)*nkpoint]     
        plt.plot(x,y,color='b',linewidth=2)
tick_pos.append(1)


minorLocator = AutoMinorLocator()
ax.yaxis.set_minor_locator(minorLocator)
plt.tick_params(axis='y',direction='in',length=7,width=2,which='major')
plt.tick_params(axis='y',direction='in',length=4,width=2,which='minor')
plt.tick_params(axis='y',right='on',direction='in',length=7,width=2,which='major')
plt.tick_params(axis='y',right='on',direction='in',length=4,width=2,which='minor')
plt.tick_params(axis='y',top='on',direction='in',length=4,width=2,which='minor')
plt.tick_params(axis='x',bottom='off')



if args.ylim != None :
    plt.ylim(args.ylim[0],args.ylim[1])
    for x in tick_pos :
        plt.axvline(x = x,ymin=args.ylim[0],ymax=args.ylim[1],linewidth=2,color='black')
    plt.axvline(x = tick_pos[0],ymin=args.ylim[0],ymax=args.ylim[1],linewidth=2,color='black')

else :
    ymin, ymax = ax.get_ylim()
    plt.ylim(ymin,ymax)
    print(ymin,ymax)
    for x in tick_pos :
        plt.axvline(x = x,ymin=ymin,ymax=ymax,linewidth=2,color='black')
    plt.axvline(x = tick_pos[0],ymin=ymin,ymax=ymax,linewidth=2,color='black')
    
tick_labels = np.empty(len(tick_pos),dtype='|S16')
for ilabel in range(0,len(tick_labels_raw),2):
    if ilabel == 0 :
        continue
    if tick_labels_raw[ilabel-1] == tick_labels_raw[ilabel]:
        tick_labels[ilabel/2] = tick_labels_raw[ilabel]
    else :
        tick_labels[ilabel/2] = tick_labels_raw[ilabel-1] +' '+ tick_labels_raw[ilabel]
tick_labels[0] = tick_labels_raw[0]
tick_labels[-1] = tick_labels_raw[-1]
print(tick_labels)


for ilabel in range(len(tick_labels)):
   tick_labels[ilabel] =  '$'+tick_labels[ilabel]+'$'
plt.xticks(tick_pos,tick_labels, fontsize=24,fontweight='bold')
plt.yticks(fontsize=20)
if args.xlim != None :
    xmin = tick_pos[args.xlim[0]]
    xmax = tick_pos[args.xlim[1]]
    plt.xlim(xmin,xmax)
else :
    plt.xlim(0,1)

if args.title != None :
    plt.title(args.title,fontsize=20)
plt.ylabel('Energy (eV)',fontsize=24)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(2)

plt.axhline(y = 0.0 ,linewidth=2,color='#bf2909',linestyle='--')

plt.savefig('BANDS.pdf')
plt.show()
