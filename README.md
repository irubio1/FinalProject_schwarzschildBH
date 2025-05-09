Welcome to my repository! Are you ready to begin simulating the motion of a particle around a Schwarzschild black hole?

Table of Contents
------------------
1. Dependencies
2. Repository Structure
3. How to Run
4. Orbit Types & Physical Conditions

------------------------------------------------------------

1. Dependencies
-----------------
This project uses the following Python libraries:
- numpy
- matplotlib

If you don't have these installed, you can get them via pip:

bash:
pip install numpy
pip install matplotlib

Please also verify that you have a working python and fortran enviroment

Repository Structure:
initial_values.txt           
Automatically written initial parameters

plot_trajectory.py          
Reads simulation output and visualizes the orbit

initial__values.py          
User input and orbit classification logic

SBH_functions.py            
Physics helper functions (e.g., unit conversion)

plot_functions.py           
Effective potential and orbit plotting functions

trajectory.dat              
Output from simulation (r, phi, t, etc.)

./run                         
#Runs every piece of code with the reposity to automatically simulate motion

How to run:
Once your dependencies are installed and you've verified python and fortran, you're ready to run the code. To initalize the simulation 
please run:
./run

You will then be prompted to input the mass of your black hole and choose the type of orbit you wish to see, those choices are documented below. 
Your bounds for Energy E, angular momentum L, and your distance from the black hole r will be given to you afterwards. Please choose your distance
from the black hole from within those bounds to provide numerical stability within your simulation. You will also choose your initial phi (azimuth angle)
for your approach to the black hole.
Once you've chosen the mass of your black hole, your choice of orbit, the distance and the angle phi, sit back and relax and the rest of the program will run smoothly!
  1. Bound (Elliptical-like) Orbit
      Condition:
      0 < E < 1
      L > L_ISCO ≈ 12M
  
      Description:
      The particle oscillates between a minimum and maximum radius (periapsis and aphelion).
      This is equivalent to a stable orbit outside the innermost stable circular orbit (ISCO).
  
  2. Marginally Bound Orbit
      Condition:
      E = 1
      L = L_mb = 4M
  
      Description:
      The particle starts from rest at infinity and barely falls into the black hole.
      This orbit separates bound from unbound trajectories.
  
  3. Unbound (Escape) Orbit
      Condition:
      E > 1
      L > 0
  
      Description:
      The particle comes in from infinity and escapes back to infinity.
      Depending on the potential barrier, it may also fall into the black hole.
  
  4. Capturing Trajectory (Plunging)
      Condition:
      L too small to prevent infall, OR
      r_initial < r_unstable
  
      Description:
      Even if E < 1, the particle spirals into the black hole if its angular momentum is too low.
  
  5. Stable Orbit
     Conditions:
     E = 1e-3 (minimu Energy)
     L = minimum Angular momentum
  
     Description:
     Stable, circular orbit
  
    
