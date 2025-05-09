#!/bin/usr/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from IPython.display import display

def choose_phi_plot():
    # Initialize variables for storing the confirmed point
    r_confirmed = None
    phi_confirmed = None
    return_value = {'phi': None}  # Dictionary to hold the result
    
    # Set up the polar plot
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)
    point, = ax.plot([], [], 'ro')  # red dot for selected point
    ax.set_yticklabels([])  # Remove the radial ticks
    ax.set_title(r"Please choose a value for your initial $\phi$", fontsize=14)

    # Click event handler
    def on_click(event):
        nonlocal r_confirmed, phi_confirmed
        if event.inaxes == ax:  # Only register clicks inside the plot
            r = event.ydata
            phi = event.xdata
            point.set_data([phi], [r])  # Update the plot with the selected point
            fig.canvas.draw()
            print(f"Clicked point: phi = {phi:.2f} rad ({np.degrees(phi):.1f}°)")
            
            # Store the selected point
            r_confirmed = r
            phi_confirmed = phi
            

    # Confirm button handler
    def on_confirm(event):
        nonlocal r_confirmed, phi_confirmed
        if r_confirmed is not None and phi_confirmed is not None:
            print(f"Selection confirmed: phi = {phi_confirmed:.2f} rad")
            return_value['phi'] = phi_confirmed  # Store phi in return_value dictionary
            plt.close(fig)  # Close the plot after confirmation
        else:
            print("No point selected yet!")

    # Connect the click event
    fig.canvas.mpl_connect('button_press_event', on_click)

    # Add a confirm button to finalize the selection
    ax_confirm = plt.axes([0.7, 0.02, 0.2, 0.05])
    confirm_button = Button(ax_confirm, 'Confirm Selection')
    confirm_button.on_clicked(on_confirm)

    # Display the button and show the plot
    plt.title("Click to select a point, then confirm")
    plt.show()

    # Wait for the user to confirm the selection
    while return_value['phi'] is None:
        plt.pause(0.1)  # This allows the event loop to run and handle user input

    return return_value['phi']  # Return the selected phi

def plot_effective_potential(M_BH, L_geom, E_geom, r_init):
    r_vals = np.linspace(2.05 * M_BH, 20 * M_BH, 1000)
    Veff = (1 - 2 * M_BH / r_vals) * (1 + (L_geom ** 2) / (r_vals ** 2))
    
    plt.figure(figsize=(8, 5))
    plt.plot(r_vals, Veff, label=r"$V_{\mathrm{eff}}(r)$")
    plt.axhline(y=E_geom**2, color='r', linestyle='--', label=r"$E^2$")
    plt.axvline(x=r_init, color='g', linestyle='--', label=r"$r_0$ (start)")
    
    plt.xlabel("r (geom units)")
    plt.ylabel(r"$V_{\mathrm{eff}}, E^2$")
    plt.title("Effective Potential vs Radius")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
