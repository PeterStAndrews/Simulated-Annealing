# Simulated_Annealing

This library contains a detailed [simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing) algorithim written in python 2.7 that can be readily customised for purpose. The base class, `SimAnn`, contains the structure of the algorithm and it is subclassed by `Details` that houses the experimental parameters and annealing schedule. This is then subclassed further by the `UserSection` which allows the user to write in their own experiment to optimise and returns a cost function for a given set of parameters.  

## Author & license 
Copyright (c) 2016, Peter Mann 
Licensed under the GNU General Public Licence v.2.0 <https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html>.
