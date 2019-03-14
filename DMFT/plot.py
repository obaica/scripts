#!/usr/bin/env python

import matplotlib.pyplot as plt


#plotting Green's functions
with open('Gf.out.0.29', 'r') as f:
    f.readline()
    lines = f.readlines()
    x = [float(line.split()[0]) for line in lines]
    y1_real = [float(line.split()[1]) for line in lines]  #eg
    y1_imag = [float(line.split()[2]) for line in lines]
    y2_real = [float(line.split()[3]) for line in lines]  #t2g
    y2_imag = [float(line.split()[4]) for line in lines]
    
plt.figure(1)
plt.plot(x,y1_real,label='eg') 
plt.plot(x,y2_real,label='t2g') 
plt.title('Real Green function')  
plt.xlabel('$i{\omega_n}$')
plt.ylabel('Re $G(i{\omega_n})$')
plt.legend()
plt.savefig('Gf_real.png')
plt.show()

plt.figure(2)
plt.plot(x,y1_imag,label='eg')
plt.plot(x,y2_imag,label='t2g')    
plt.title('Imaginary Green function')    
plt.legend() 
plt.xlabel('$i{\omega_n}$')
plt.ylabel('Im $G(i{\omega_n})$')
plt.savefig('Gf_imag.png')
plt.show()
f.close()

#plotting Self-energies
with open('Sig.out.0.29', 'r') as f:
    f.readline()
    lines = f.readlines()
    x = [float(line.split()[0]) for line in lines]
    y1_real = [float(line.split()[1]) for line in lines]  #eg
    y1_imag = [float(line.split()[2]) for line in lines]
    y2_real = [float(line.split()[3]) for line in lines]  #t2g
    y2_imag = [float(line.split()[4]) for line in lines]
    
plt.figure(3)
plt.plot(x,y1_real,label='eg') 
plt.plot(x,y2_real,label='t2g') 
plt.title('Real Self-Energy')  
plt.xlabel('$i{\omega_n}$')
plt.ylabel('Re $\Sigma(i{\omega_n})$')
plt.legend()
plt.savefig('Selfenergy_real.png')
plt.show()

plt.figure(4)
plt.plot(x,y1_imag,label='eg')
plt.plot(x,y2_imag,label='t2g')    
plt.title('Imaginary Self-Energy')     
plt.legend()
plt.xlabel('$i{\omega_n}$')
plt.ylabel('Im $\Sigma(i{\omega_n})$')
plt.savefig('Selfenergy_imaginary.png')
plt.show()
f.close()

#plotting analytically continued Self-energies
with open('Sig1.out', 'r') as f:
    f.readline()
    lines = f.readlines()
    x = [float(line.split()[0]) for line in lines]
    y1_real = [float(line.split()[1]) for line in lines]  #eg
    y1_imag = [float(line.split()[2]) for line in lines]
    y2_real = [float(line.split()[3]) for line in lines]  #t2g
    y2_imag = [float(line.split()[4]) for line in lines]
    
plt.figure(5)
plt.plot(x,y1_real,label='eg') 
plt.plot(x,y2_real,label='t2g') 
plt.title('Real Self-Energy Analytically continued')  
plt.legend()
#plt.ylim(-0.1,0.1)
plt.xlabel('$\omega$')
plt.ylabel('Re $\Sigma(\omega})$')
plt.savefig('RealSelf-EnergyAnalyticallycontinued.png')
plt.show()

plt.figure(6)
plt.plot(x,y1_imag,label='eg')
plt.plot(x,y2_imag,label='t2g')    
plt.title('Imaginary Self-Energy Analytically continued')     
plt.legend()
#plt.ylim(-0.1,0.1)
plt.xlabel('$\omega$')
plt.ylabel('Im $\Sigma(\omega})$')
plt.savefig('Imaginary Self-Energy Analytically continued.png')
plt.show()
f.close()

