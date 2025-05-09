#!/bin/usr/python3

import numpy as np
import plot_functions as SBH_PLOT
import SBH_functions as functions

outf_name = "initial_values.txt"
with open(outf_name, "w") as IV_outf:
    # User input for black hole mass and geometrized space flag
    M_BH = float(input("Mass of Black Hole (in solar masses): "))
        # Ask user what type of orbit they want
    print("\nSelect the type of orbit you'd like to simulate:")
    print("1. Bound (Elliptical-like)")
    print("2. Marginally bound (E = 1)")
    print("3. Unbound (Escape)")
    print("4. Plunge (Capturing)")
    orbit_choice = input("Enter number (1-4): ")
    print(f"\nGiven the mass {M_BH} of your black hole, please adhere to these following bounds to maintain numerical stability for your simulated model:")
    bounds = functions.calculate_bounds(M_BH)
    # Print bounds in scientific notation
    for key, value in bounds.items():
        print(f"{key}: {value[0]:.3e} to {value[1]:.3e}")


    geometrized_space = False  ### DO NOT CHANGE THIS FLAG UNLESS YOU COMPLETELY UNDERSTAND GEOMETRIZED UNITS --- (the geometrized space section is also still underdeveloped and may explode if you try so don't please)

    # Define constants for limits
    r_min_factor = 2.1
    L_max_factor = np.sqrt(12)

    # Geometrized units branch
    if geometrized_space:
        r_geom, tau_end, L_geom, E_geom, phi, time_step = functions.GEOM_space()

        
    # SI units branch
    else:
        def SI_activation():
            r_m, phi = functions.SI_space()  # now SI_space() only returns 2 values
            if r_m < bounds["radius_SI_m"][0] or r_m > bounds["radius_SI_m"][1]:
                print(f"[Error] Radius r = {r_m} m is out of bounds.")


            # Only converting r_m to r_geom
            r_geom, _, _, _ = functions.si_to_geom(M_BH, r_m)

            # Use preset values for the rest
            tau_geom = 999.99 # a few orbital periods
            time_step = 0.01
            E_geom, L_geom = functions.orbit_choice(M_BH, orbit_choice)

            return r_geom, tau_geom, L_geom, E_geom, time_step, phi


    # Constants for validation
    r_min_factor = 2.1
    L_max_factor = np.sqrt(12)

    # Try until valid inputs are provided
    while True:
        print("")
        r_geom, tau_geom, L_geom, E_geom, time_step, phi = SI_activation()
        
        n = int(tau_geom/time_step)
        print("")
        print(f"Initial radius r = {r_geom:.3e} geom units")
        print(f"Schwarzschild radius r_s = {2 * M_BH:.3e}")

        SBH_PLOT.plot_effective_potential(M_BH, L_geom, E_geom, r_geom)


        # Validate radius using the bounds
        if r_geom < bounds["radius_geom"][0] or r_geom > bounds["radius_geom"][1]:
            print(f"[Error] Radius r = {r_geom:.3e} is out of bounds.")
            print(f"        Must be within bounds: {bounds['radius_geom'][0]:.3e} to {bounds['radius_geom'][1]:.3e}")
            continue
       # Write the parameters to the output file
        writestr = f"{n}\t{r_geom}\t{tau_geom}\t{L_geom}\t{E_geom}\t{M_BH}\t{phi}\t{time_step}"
        print(f"Writing to file: {writestr}")  # Debug print
        try:
            with open('initial_values.txt', 'w') as IV_outf:
                IV_outf.write(writestr + "\n")
        except Exception as e:
            print(f"Error writing to file: {e}")

        # All checks passed, break out of the loop
        break  # This will exit the loop after writing to the file
print("Initial values written to initial_values.txt.")

