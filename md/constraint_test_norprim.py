#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import re
import sys

#number of abinit iterations
iterations=int(sys.argv[1])

#name of system
name=sys.argv[2]

######################################

#creating zero matrices
xcart = np.zeros(iterations)
r12_mag = np.zeros(iterations)
cos_alpha = np.zeros(iterations)
acell1=np.zeros(iterations)
acell2=np.zeros(iterations)
acell3=np.zeros(iterations)
cos_beta=np.zeros(iterations)
etot=np.zeros(iterations)
volume=np.zeros(iterations)
pressure=np.zeros(iterations)

rp1_mod = np.zeros(iterations)
rp2_mod = np.zeros(iterations)
rp3_mod = np.zeros(iterations)


for i in range(iterations):
    #open .out file
    fileop = open("./"+name+str(i)+"/"+name+str(i)+".out","r")
    read = fileop.read()
    fileop.close()
    
    #open .mdout file
    fileopmdout = open("./"+name+str(i)+"/"+name+str(i)+".mdout","r")
    readmd = fileopmdout.read()
    fileopmdout.close()
    
    #constraint values
    acell_init = re.findall('acell([0-9E+.\s]*)Bohr',read)[0].split()
    #rprim_init = re.findall('rprim([0-9E+-.\s]*)shiftk',read)[0].split()
    xcart_init = re.findall('xcart([0-9E+-.\s]*)xred',read)[0].split()
    tot_energy = re.findall('etotal([0-9E+-.\s]*)fcart',read)[0].split()
    volume_init = re.findall('volume\(Bohr\^3\)([0-9E+-.\s]*)md_step',readmd)[0].split()[1:][::2]
    pressure_init = re.findall('pressure\(hartree/Bohr\^3\)([0-9E+-.\s]*)bond\sconstraints',readmd)[0].split()[1:][::2]
    
    #atom constraint
    xcart[i]=xcart_init[0] #atom 1
    
    #bond constraint
    r1=np.array(xcart_init[0:3],float)
    r2=np.array(xcart_init[3:6],float)
    r3=np.array(xcart_init[6:9],float)
    r4=np.array(xcart_init[9:12],float)
    r5=np.array(xcart_init[12:15],float)
    r6=np.array(xcart_init[15:18],float)
    r7=np.array(xcart_init[18:21],float)
    r8=np.array(xcart_init[21:24],float)
    r9=np.array(xcart_init[24:27],float)
    r10=np.array(xcart_init[27:30],float)
    r11=np.array(xcart_init[30:33],float)

    r19_mag[i]=np.linalg.norm(r9-r1) #9th atom and 1st atom bond
    
    #atom angle contraint
    r3=np.array(xcart_init[6:9],float)
    r4=np.array(xcart_init[9:12],float)
    r5=np.array(xcart_init[12:15],float)
    r34=r4-r3
    r35=r5-r3
    cos_alpha[i] = (np.dot(r34,r35))/((np.linalg.norm(r34))*(np.linalg.norm(r35)))
    
    #cell parameter constraint
    acell1[i]=acell_init[0]
    acell2[i]=acell_init[1]
    acell3[i]=acell_init[2]

    #rprim vectors
    # rp1 = np.array([rprim_init[0],rprim_init[3],rprim_init[6]],float)
    # rp2 = np.array([rprim_init[1],rprim_init[4],rprim_init[7]],float)
    # rp3 = np.array([rprim_init[2],rprim_init[5],rprim_init[8]],float)

    rp1 = np.array([1,0,0])
    rp2 = np.array([0,1,0])
    rp3 = np.array([0,0,1])


    #modulus of rprim vectors
    rp1_mod[i] = np.linalg.norm(rp1)
    rp2_mod[i] = np.linalg.norm(rp2)
    rp3_mod[i] = np.linalg.norm(rp3)

    
    #cell angle constraint
    a =float(acell_init[0])*rp1
    b =float(acell_init[1])*rp2
    c =float(acell_init[2])*rp3.
    cos_beta[i] = (np.dot(a,b))/((np.linalg.norm(a))*(np.linalg.norm(b)))
    
    #total energy
    etot[i] = tot_energy[0]
    
    #volume
    volume[i] = volume_init[-1]
    
    #pressure
    pressure[i] = pressure_init[-1]
    
# plt.figure(1)

# plt.subplot(121)
# plt.plot(acell1)
# plt.plot(acell2)
# plt.plot(acell3)
# plt.title('acell')
# plt.xlabel('Iteration')
# plt.ylabel('Bohr')
# plt.legend(['acell1','acell2','acell3'])


# plt.subplot(122)
# plt.plot(rp1_mod)
# plt.plot(rp2_mod)
# plt.plot(rp3_mod)
# plt.title('rprim')
# plt.xlabel('Iteration')
# plt.ylabel('magnitude')
# plt.legend(['rp1_mod','rp2_mod','rp3_mod'])
# plt.tight_layout()
# ax = plt.gca()
# ax.ticklabel_format(useOffset=False)
# plt.savefig('acell_rprim.pdf')
# plt.show()

    
####PLOTTING########
plt.figure(1)

plt.subplot(421)
plt.plot(xcart)
plt.title('Atomic position of Fe1 atom')
plt.xlabel('Iteration')
plt.ylabel('Bohr')


plt.subplot(422)
plt.plot(r12_mag)
ax = plt.gca()
ax.ticklabel_format(useOffset=False)
plt.title('Bond Length')
plt.xlabel('Iteration')
plt.ylabel('Bohr')

plt.subplot(423)
plt.plot(cos_alpha)
plt.title('Atom angle')
plt.xlabel('Iteration')
plt.ylabel('cosine')

plt.subplot(424)
plt.plot(acell1)
plt.title('Cell Parameter')
plt.xlabel('Iteration')
plt.ylabel('Bohr')

plt.subplot(425)
plt.plot(cos_beta)
plt.title('Cell vector angle')
plt.xlabel('Iteration')
plt.ylabel('cosine')

plt.subplot(426)
plt.plot(etot)
plt.title('Total Energy')
plt.xlabel('Iteration')
plt.ylabel('Hartree')

plt.subplot(427)
plt.plot(volume)
plt.title('Volume')
plt.xlabel('Iteration')
plt.ylabel('Bohr^3')

plt.subplot(428)
plt.plot(pressure)
plt.title('Pressure')
plt.xlabel('Iteration')
plt.ylabel('Hartree/Bohr^3')



plt.tight_layout()
plt.savefig('constraints.pdf')



plt.show()    
