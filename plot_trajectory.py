#!/bin/usr/python3.12

import matplotlib.pyplot as plt
import SBH_functions as functions
import plot_functions as SBH_PLOT 
import numpy as np

# Load data from trajectory.dat assuming columns: tau, r_geom, phi, pr, pphi
data = np.loadtxt("trajectory.dat", skiprows=2)  # Skip the first row if it's a header
n, r_geom, tau_geom, L_geom, E_geom, M_BH, phi, time_step = np.loadtxt("initial_values.txt", delimiter='\t')


# Extract relevant columns
r_geom = data[:, 1]  # r in geometrized units
phi = data[:, 2]     # angular position in radians

# Constants
G = 6.67430e-11        # m^3 / (kg s^2)
c = 2.99792458e8       # m/s
M_sun = 1.98847e30     # kg
M_BH = M_BH              # example black hole mass in solar masses
M_kg = M_BH * M_sun
M_geom = G * M_kg / c**2  # conversion factor to meters

# Convert r from geometrized units to meters
r_meters = r_geom * M_geom
r_s = 2 * M_BH * M_geom  # Schwarzschild radius in meters

# Create polar plot
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
ax.plot(phi, r_meters, label='Trajectory', lw=1.5)
ax.set_title(f"Orbit Around Schwarzschild BH (M = {M_BH} $M_\\odot$)", va='bottom')

# Plot Schwarzschild radius
ax.plot(np.linspace(0, 2*np.pi, 500), np.full(500, r_s), 'r--', label='Schwarzschild Radius')

ax.set_rlabel_position(135)
ax.grid(True)
ax.legend(loc='upper right')
plt.show()

