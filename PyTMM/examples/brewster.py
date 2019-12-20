"""Calculates angle dependent reflectivity for two polarizations.
"""
import numpy as np
import matplotlib.pyplot as plt

from PyTMM.transferMatrix import TransferMatrix, Polarization

ref_index = 2
thickness = 600  # slab thickness, nm
wavelength = 500  # wavelength, nm
angles_rad = np.linspace(0, np.pi / 2, 1000)

r_for_te_polarization = np.zeros(angles_rad.shape)
r_for_tm_polarization = np.zeros(angles_rad.shape)

for i, angle in enumerate(angles_rad):
    # TE
    a = TransferMatrix.layer(ref_index, thickness,
                             wavelength, angle, Polarization.s)
    R, T = a.solvePropagation()
    r_for_te_polarization[i] = np.abs(R**2)

    # TM
    a = TransferMatrix.layer(ref_index, thickness,
                             wavelength, angle, Polarization.p)
    R, T = a.solvePropagation()
    r_for_tm_polarization[i] = np.abs(R**2)

#%% unfortunately this is not working, maybe transfer matrices could be admjusted so it will work:
# # TE
# a = TransferMatrix.layer(ref_index, thickness,
#                          wavelength, angles_rad, Polarization.s)
# R, T = solvePropagation(a)
# r_for_te_polarization = np.abs(R**2)

# # TM
# a = TransferMatrix.layer(ref_index, thickness,
#                          wavelength, angles_rad, Polarization.p)
# R, T = solvePropagation(a)
# r_for_tm_polarization = np.abs(R**2)


plt.plot(angles_rad, r_for_te_polarization)
plt.plot(angles_rad, r_for_tm_polarization)
plt.xlabel("Angle, rad")
plt.ylabel("Reflectance")
plt.title("Angle dependence of reflectivity")
plt.legend(['TE', 'TM'], loc='best')
plt.show(block=True)
