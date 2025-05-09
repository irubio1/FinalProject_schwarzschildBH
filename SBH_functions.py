#!/bin/usr/python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import plot_functions as SBH_PLOT

#Conversion Functions 
def si_to_geom(M_BH, r_m=None, tau_s=None, L_m2ps=None, E_jpkg=None): 
    """
    Converts SI quantities to geometrized units (in terms of M) where G = c = 1.
    Each input can be optional (None); only the provided values will be converted.
    """
    G = 6.67430e-11  # m^3 / (kg s^2)
    c = 2.99792458e8  # m/s
    M_sun = 1.98847e30  # kg
    M_kg = M_BH * M_sun

    M_geom = G * M_kg / c**2  # meters
    Tau_geom = G * M_kg / c**3  # seconds
    L_geom_factor = G * M_kg / c  # for angular momentum

    # Conversion from SI to Geometrized
    r_geom = r_m / (2 * G * M_kg / c**2) if r_m is not None else None
    tau_geom = tau_s / Tau_geom if tau_s is not None else None
    L_geom = L_m2ps / L_geom_factor if L_m2ps is not None else None
    E_geom = E_jpkg / c**2 if E_jpkg is not None else None

    return r_geom, tau_geom, L_geom, E_geom

def geom_to_si(M_BH, r_geom=None, tau_geom=None, L_geom=None, E_geom=None):
    """
    Converts geometrized units back to SI units (meters, seconds, etc.).
    """
    G = 6.67430e-11  # m^3 / (kg s^2)
    c = 2.99792458e8  # m/s
    M_sun = 1.98847e30  # kg
    M_kg = M_BH * M_sun

    # Conversion factor
    conversion_factor = 2 * G * M_kg / c**2  # for radius, meters

    r_m = r_geom * conversion_factor if r_geom is not None else None
    tau_s = tau_geom * G * M_kg / c**3 if tau_geom is not None else None
    L_m2ps = L_geom * G * M_kg / c if L_geom is not None else None
    E_jpkg = E_geom * c**2 if E_geom is not None else None

    return r_m, tau_s, L_m2ps, E_jpkg

def SI_space():
    r_m = float(input("Distance from black hole (m): "))  
    phi = SBH_PLOT.choose_phi_plot()

    # Convert SI units to geometrized units

    return r_m, phi

def GEOM_space():
    E_geom = float(input("Energy E (geometrized): "))
    L_geom = float(input("Angular Momentum L (geometrized): "))
    r_geom = float(input("Distance from black hole (in geometrized units): ")) * M_BH
    phi = SBH_PLOT.choose_phi_plot()
    tau_end = 100  # Default tau_end for the simulation
    time_step = 0.01  # Default time step

    return r_geom, tau_end, L_geom, E_geom, phi, time_step


def calculate_bounds(M_BH):
    # Adjusted lower bounds for stability
    r_min_geom = 2.5 * M_BH  # Slightly higher lower bound for radius in geometrized units
    r_max_geom = 20* M_BH  # Example for upper bound of radius in geometrized units
    
    # Convert radius bounds from geometrized units to SI meters
    r_min_SI, _, _, _ = geom_to_si(M_BH, r_min_geom)  # Convert only the radius (r_geom)
    r_max_SI, _, _, _ = geom_to_si(M_BH, r_max_geom)  # Convert only the radius (r_geom)
    
    # Adjusted bounds for angular momentum (in geometrized units)
    L_min_geom = 1.2 * M_BH  # Slightly higher lower bound for angular momentum
    L_max_geom = 12 * M_BH  # Example upper bound for angular momentum
    
    # Convert angular momentum bounds to SI units (multiplying by 1e3 for conversion)
    L_min_SI = L_min_geom * 1e3  # Convert to m^2/s
    L_max_SI = L_max_geom * 1e3  # Convert to m^2/s
    
    # Adjusted bounds for energy in geometrized units
    E_min_geom = 0.05  # Slightly higher minimum energy in geometrized units
    E_max_geom = 1.0  # Example maximum energy in geometrized units
    
    # Convert energy bounds to SI units (using J/kg as the unit)
    E_min_SI = E_min_geom * 1e-3  # Convert to J/kg (example)
    E_max_SI = E_max_geom * 1e-3  # Convert to J/kg (example)

    # Return the bounds as a dictionary
    bounds = {
        "energy_geom": (E_min_geom, E_max_geom),
        "energy_SI_Jpkg": (E_min_SI, E_max_SI),
        "angular_momentum_geom": (L_min_geom, L_max_geom),
        "angular_momentum_SI_m2ps": (L_min_SI, L_max_SI),
        "radius_geom": (r_min_geom, r_max_geom),
        "radius_SI_m": (r_min_SI, r_max_SI),
    }
    
    return bounds

def orbit_choice(M_BH, orbit_choice):

    # Constants for orbit classification
    L_ISCO = np.sqrt(12) * M_BH
    L_mb = 4 * M_BH

    if orbit_choice == "1":  # Bound
        E_geom = 0.95  # must be < 1
        L_geom = L_ISCO + 1
    elif orbit_choice == "2":  # Marginally bound
        E_geom = 1.0
        L_geom = L_mb
    elif orbit_choice == "3":  # Unbound
        E_geom = 1.05  # must be > 1
        L_geom = L_ISCO + 5
    elif orbit_choice == "4":  # Plunge
        E_geom = 0.95
        L_geom = 2.0 * M_BH  # below ISCO

    return E_geom, L_geom