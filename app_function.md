i want to build a web app based on plotly dash where i can calculate and visualize deformation of a cantilever beam, in the web page i want to input the size of the beam, only intrested in rectangles, so ask for side view height and top view width, and wall thickness, and give a tick box for solid beam, and then length of the beam, and force applied on the end of the beam in Newtons, want to use SI units every where, here is the math, strictly follow this math
 
Maximum Reaction Force
at the fixed end can be expressed as:
 
RA = F                       
 
where
 
RA = reaction force in A (N, lb)
 
F = single acting force in B (N, lb)
 
Maximum Moment
at the fixed end can be expressed as
 
Mmax = MA = - F L                              
 
where
 
MA = maximum moment in A (Nm, Nmm, lb in)
 
L = length of beam (m, mm, in)
 
Maximum Deflection
at the end of the cantilever beam can be expressed as
 
δB = F L3 / (3 E I)                                   
 
where
 
δB = maximum deflection in B (m, mm, in)
 
E = modulus of elasticity (N/m2 (Pa), N/mm2, lb/in2 (psi))
 
I = moment of Inertia (m4, mm4, in4)
 
b = length between B and C (m, mm, in)    