# Sub-class of `details` that includes users experiment for optimisation
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


class user_section( details ):
    '''The sub-class tailors the algorithm to the user's experiment we wish to minimise. This section is highly 
    user-defined and creates the random walk through the parameter space as well as the generation of the 
    cost function'''
    
    def __init__(self, parameters):
        super(user_section, self).__init__(parameters) 
        
    def null_updates( self, parameters ):
        '''function returns parameters without modification'''
        raise NotImplementedError   
        
    def updates( self, parameters ):
        '''function performs the updates in the parameter space. Returns dict of variables
        over which the new cost function will be evaluated. It is important to constrain the 
        search to physically meaningful submanifolds of the parameter space.'''
        raise NotImplementedError   
            
    def costfunction( self, variables ): 
        '''function generates the cost function for a particular parameter set (variables) and returns it's value. 
        The new state is then created as a particular realisation of the underlying experiment. Must set:
        
        self.NEW_INSTANCE 
        self.NEW_STATE 
        self.NEW_COST 
        
        If using epyc, will only have one 'new cost' line to update. '''
        raise NotImplementedError   
        
    def create_model( self ):
        '''function produces the model that we evaluate the parameters over.  '''
        raise NotImplementedError






        