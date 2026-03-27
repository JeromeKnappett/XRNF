import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.rcParams['text.usetex'] = True 

# Function to calculate aerial image contamination (zeta)
def aerial_image_contam(I0,Itot):
    return I0/(Itot)

# Function to calculate transmission from zeta
def transmission_from_zeta(zeta, N=2, eta=0.1):
    T = (zeta*N*eta)/(1-zeta)
    return T

# Grating pair names
names = ['GP1', 'GP2', 'GP3']

# Counts data: left, right, center, total
c_l = [194792,730271, 174874, 709160, 240035, 977297]
c_r = [126640, 318270, 113233, 303949, 167576, 508355]
c_c = [161594, 402885, 156999, 402570, 153840, 407951]
c_t = [521882, 1449428, 468252, 1413442, 608146, 1891319]

# Calculate zeta for original and total
zeta_o = [aerial_image_contam(c_c[i], c_r[i]+c_c[i]+c_l[i]) for i in range(len(c_c))]
zeta_t = [aerial_image_contam(c_c[i], c_t[i]) for i in range(len(c_c))]

# Calculate transmission in percentage
T_o = [transmission_from_zeta(zeta_o[i]) * 100 for i in range(len(c_c))]
T_t = [transmission_from_zeta(zeta_t[i]) * 100 for i in range(len(c_c))]

# Plotting
plt.figure(figsize=(6,5))
plt.plot(names, T_o[::2], 'o:', color='red', mfc='none', label='high coherence - 400 pix', markersize=10)
plt.plot(names, T_o[1::2], 'o:', color='black', mfc='none', label='low coherence - 400 pix', markersize=10)
plt.plot(names, T_t[::2], 'x:', color='red', mfc='none', label='high coherence - full', markersize=10)
plt.plot(names, T_t[1::2], 'x:', color='black', mfc='none', label='low coherence - full', markersize=10)
plt.xlabel('Grating Pair', fontsize=14)
plt.ylabel('$T_{\\mathrm{abs}}\,[\%]$', fontsize=14)
# plt.title('Transmission from Farfield')
plt.legend()
plt.savefig("C:/Users/jknappett/Documents/XRNF/figures/transmission_from_farfield.pdf", bbox_inches='tight')
plt.show()
