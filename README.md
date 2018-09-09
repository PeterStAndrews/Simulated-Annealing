# Simulated_Annealing

This library contains a detailed simulated annealing algorithim written in python 2.7 that can be readily customised for purpose. The base class, `SimAnn`, contains the structure of the algorithm and it is subclassed by `Details` that houses the experimental parameters and annealing schedule. This is then subclassed further by the `UserSection` which allows the user to write in their own experiment to optimise and returns a cost function for a given set of parameters.  
