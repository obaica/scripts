import numpy as np
import matplotlib.pylab as plt
import argparse
from matplotlib.ticker import AutoMinorLocator
parser = argparse.ArgumentParser()
parser.add_argument('-legend',nargs='+',help='legen list')
parser.add_argument('-xlim',nargs=2,type=float,help='x limits')
parser.add_argument('-ylim',nargs=2,type=float,help='y limits')
parser.add_argument('-input',dest='f',help='file name')
parser.add_argument('-title',help='plot title')
parser.add_argument('-orbitals',nargs='+',type=int,help='orbitals to be ploted')
args = parser.parse_args()
norb = len(args.orbitals)
data = np.loadtxt(args.f)
ndata = 3000
from matplotlib import rc
rc('text', usetex=True)
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.family'] = 'serif'
fig , ax = plt.subplots()
minorLocator = AutoMinorLocator()
ax.xaxis.set_minor_locator(minorLocator)
plt.tick_params(axis='x',direction='in',length=7,width=2,which='major')
plt.tick_params(axis='x',direction='in',length=4,width=2,which='minor')
plt.tick_params(axis='x',top='on')
plt.tick_params(axis='x',top='on',direction='in',length=4,width=2,which='minor')
plt.tick_params(axis='y',labelleft=0,left=0)
if args.orbitals == None :
    orbitals = range(1,len(data)/ndata)
else :
    orbitals = args.orbitals
if args.legend == None :
    legend = range(len(data)/ndata)
else :
    legend = args.legend
for iorb in orbitals:
    plt.plot(data[iorb*ndata:(iorb+1)*ndata,0],data[iorb*ndata:(iorb+1)*ndata,1],label = legend[iorb-1],linewidth=2)
    print(len(data[iorb*ndata:(iorb+1)*ndata,0]))
if args.xlim != None :
    plt.xlim(args.xlim[0],args.xlim[1])
if args.ylim != None :
    plt.ylim(args.ylim[0],args.ylim[1])
if args.title != None :
    plt.title(args.title,fontsize=12)
#plt.xticks(direction='in')
#plt.get_minor_ticks()
plt.xlabel('Energy (eV)',fontsize=16)
plt.ylabel('Density of States(a.u.)',fontsize=16)
plt.legend(fontsize=12)
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(2)
plt.axvline(x = 0.0 ,linewidth=2,color='#6309bf',linestyle='--')
plt.savefig('DOS.pdf')
plt.show()
