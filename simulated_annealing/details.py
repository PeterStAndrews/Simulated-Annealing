# Sub-class of `SimAnn` that includes details of annealing schedule
#
# Copyright (C) 2016 Peter Mann
# 
# This file is part of `simulated annealing`, for optimisation using Python.
#
# `simulated annealing` is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# `simulated annealing` is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with `simulated annealing`. If not, see <http://www.gnu.org/licenses/gpl.html>.

import numpy

class details( SimAnn ):
    '''This sub-class specifies the details of the MCMC experiment'''
    
    def __init__(self, parameters):
        super(details, self).__init__(parameters)
        
        self._initial_temperature = parameters['initial_temperature'] 
        self._final_temperature = parameters['final_temperature'] 
        self._alpha = parameters['alpha'] #schedule parameter
        
    def schedule( self ):
        '''function decreases temperature to reduce acceptance frequency according to user schedule.
        This localises the exploration to the global minimum.'''
        self.temperature *= self._alpha
        
    def convergence( self ):
        '''function returns True if the convergence criteria for the experiment is met'''
        if self.temperature < self._final_temperature:
            return True    
        
    def criterion( self ):
        '''The acceptance function to be used, pass if greedy search. '''
        
        #Boltzmann distribution
        Boltzmann = numpy.exp( - (1 / self.temperature) * abs((self.NEW_COST - self.CURRENT_COST)) )
        
        #Barker distribution
        Barker = 1/ (1 + numpy.exp( (1 / self.temperature) * abs((self.NEW_COST - self.CURRENT_COST)) ))
        
        #update proposal list
        self.criterion_list.append( Boltzmann )
        
        return Boltzmann