# Base class for `simulated annealing`.
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

import random
import numpy
import time 

class SimAnn( object ):
    ''' This class is an abstract Markov Chain Monte Carlo algorithm to obtain the global minimum of a cost function. 
    Each new update generates a cost for the new state, this is compared against the current minimum cost for
    the currently minimal state. The class takes a dict 'parameters' as it's argument. This contains key 
    information for the algorithm including modulations to the convergence, acceptance and initialisation criteria.
    
    The user must define the methods for the class using sub-classes. '''
    
    def __init__( self, parameters ):
        '''creates instance of the class and initialises class parameters'''
        
        self.NEW_STATE = None
        self.NEW_COST = None 
        self.NEW_INSTANCE = None
        
        self.CURRENT_STATE = None
        self.CURRENT_INSTANCE = None
        self.CURRENT_COST = parameters['initial_cost']
        
        self.BEST_STATE = None
        self.BEST_COST = parameters['initial_cost'] 
        self.BEST_INSTANCE = None
        
    def before( self ):
        '''initialisation function to be run before the experiment'''
        
        self.moves = 0
        self.accepted = 0
        self.rejected = 0     
        self.start_time = time.clock()
        self.temperature = self._initial_temperature
        self.criterion_list = list()
        self.list_of_proposals = list()
        self.acceptance = list()
        
    def null_update( self, parameters ):
        '''placeholder function returns parameters without modification'''
        raise NotImplementedError
    
    def updates( self, parameters ):
        '''placeholder function performs the updates in the parameter space. Returns dict of variables
        over which the new cost function will be evaluated'''
        raise NotImplementedError
               
    def costfunction( self, variables ): 
        '''placeholder function generates the cost function for a particular parameter set (variables) and returns its value. 
        The new state is then created as a particular realisation of the underlying experiment. Must set 
        self.NEW_STATE and return the value of self.NEW_COST '''
        raise NotImplementedError
        
    def lowest_ever( self ):
        '''function checks if newly accepted move is the lowest ever recorded'''
        if self.CURRENT_COST < self.BEST_COST:
            
            self.BEST_COST = self.CURRENT_COST
            self.BEST_STATE = self.CURRENT_STATE
            self.BEST_INSTANCE = self.CURRENT_INSTANCE
        
    def criteria( self ):
        '''function evaluates the Metropolis-Hastings criteria for the cost function. Stores previously held
        value of cost function and compares against the updated value. If new is accepted then the previous 
        value is replaced and the details of the new value are returned, else the details of the old state are 
        returned. '''
        
        #increase number of moves by one
        self.moves += 1
        
        #move is accepted
        if (self.NEW_COST < self.CURRENT_COST) or ( numpy.random.uniform(0,1) < self.criterion() ):
            
            self.accepted += 1
            
            #update current leading minimum
            self.CURRENT_COST = self.NEW_COST 
            self.CURRENT_STATE = self.NEW_STATE
            self.CURRENT_INSTANCE = self.NEW_INSTANCE
            
            self.list_of_proposals.append( self.NEW_COST )
            
            #check if proposal is best on record
            self.lowest_ever()
            
        #move is rejected
        else:
            self.rejected += 1
            
    def criterion( self ):
        '''placeholder for the acceptance function to be used'''
        raise NotImplementedError
        
    def acceptance_ratio( self ):
        '''function computes the acceptance ratio over the course of the experiment'''
        self.acceptance.append( (self.accepted + 0.0) / (self.accepted + self.rejected) )
                    
    def convergence( self ):
        '''function returns True if the convergence criteria for the experiment is met'''
        raise NotImplementedError        
        
    def schedule( self ):
        '''function increases beta to reduce acceptance frequency according to user schedule'''
        raise NotImplementedError        
        
    def after( self, rc ):
        '''function to be run after experiment. It records: the instance of the underlying experiment, 
        the minimum cost, the minimum state (or rather the experimental parameters that minimised the 
        cost function, provided they are returned from the user-defined experiment) and the algorithm metadata. '''
        
        self.total_time = time.clock() - self.start_time
        
        rc['Instance'] = self.CURRENT_INSTANCE
        rc['Algorithm'] = {'Moves': self.moves, 'Accepted': self.accepted, 'Rejected': self.rejected, 'time': self.total_time}
        rc['Cost'] = self.CURRENT_COST
        rc['State'] = self.CURRENT_STATE      
        rc['Proposal_History'] = self.list_of_proposals
        rc['criterion_list'] = self.criterion_list
        rc['Ratio'] = self.acceptance
        rc['Lowest'] = {'Cost': self.BEST_COST, 'State': self.BEST_STATE, 'Instance': self.BEST_INSTANCE }
        
    def experiment( self ): 
        '''This function performs the MCMC algorithm. The current experiment with the lowest cost function is
        saved into a dict which is reported upon convergence by calling self.after() '''

        rc = dict()
        self.before()
        
        while not self.convergence(): 
            
            #update parameters
            variables = self.updates( parameters )
            
            #generate new cost function
            self.costfunction( variables )
            
            #evaluate Metropolis criteria and record current best state
            self.criteria()
            
            #compute acceptance ratio
            self.acceptance_ratio()
            
            #update schedule 
            self.schedule()
            
        self.after( rc )
            
        return rc