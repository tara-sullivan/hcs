import numpy as np
import pandas as pd
# import numba as nb
# import os

# useful tools
from quantecon.util import timing
# import pdb
# from importlib import reload

# from other programs
import AFModel
AgentHistory = AFModel.AgentHistory


sim_num_default = 1000
ab_0_default = np.array([[1, 1], [1, 1]], np.float64)
w_default = np.array([1, 1], np.float64)
v_default = np.array([1, 1], np.float64)
ability_default = np.array([0.5, 0.5], np.float64)


class SimulateAgents:
    '''
    Simulates agent's course history, given prior ab_0

    Optional arguments:
        * ab_0:     Initial human capital levels
        * w:        Wages for each skill
        * v:        Human capital update amount
        * ability:  True ability of agents in population
        * sim_num:  Number of simulations
    '''
    def __init__(self,
                 ab_0=None,     # initial human capital levels
                 w=None,        # default sector-specific wages
                 v=None,        # human capital update amount
                 ability=None,  # true ability
                 sim_num=None   # number of simuations to run
                 ):
        # Use default values if no argument called
        if ab_0 is not None:
            self.ab_0 = ab_0
        else:
            self.ab_0 = ab_0_default

        if w is not None:
            self.w = w
        else:
            self.w = w_default

        if v is not None:
            self.v = v
        else:
            self.v = v_default

        if sim_num is not None:
            self.sim_num = sim_num
        else:
            self.sim_num = sim_num_default

        # Ability default takes a couple more arguments
        # Number of courses
        self.N_j = np.size(self.ab_0, axis=0)
        if ability is not None:
            # pass the whole population of abilities
            if ability.shape == (self.sim_num, self.N_j):
                self.ability = ability
            # otherwise you need to broadcast given ability to population
            else:
                self.ability = np.broadcast_to(ability,
                                               (self.sim_num, self.N_j))
        # If no ability arg given, broadcast default ability to population
        else:
            self.ability = np.broadcast_to(ability_default,
                                           (self.sim_num, self.N_j))

        # Call instance of AFModel
        self.afm = AgentHistory(ab_0=self.ab_0,
                                w=self.w,
                                v=self.v)

        # Run simulation
        self.run_sim()

    def run_sim(self):
        '''
        Simulate agents using afm model
        '''
        # simplify notation
        sim_num = self.sim_num
        ability = self.ability
        afm = self.afm
        # initialize arrays
        chosen_field = np.empty(sim_num)
        field_state = np.empty((sim_num, 2))
        course_history_list = []

        print('Running...')
        timing.tic()
        for i in range(sim_num):
            # Create agent's history
            # Optional arguments include fail_first, choose_first
            afm.find_history_i(ability[i])

            # Fill in result arrays
            chosen_field[i] = afm.chosen_field
            field_state[i] = afm.field_state
            # Create a list of dataframes; quicker to concatenate later
            course_history_list.append(
                pd.DataFrame(list(zip(afm.c_history, afm.c_outcome)),
                             columns=['subject', 'outcome']))
        timing.toc()
        # concatenate dataframes for full course history
        course_history = pd.concat(course_history_list,
                                   keys=range(sim_num),
                                   names=['student', 't'])
        self.chosen_field = chosen_field
        self.field_state = field_state
        self.course_history = course_history


if __name__ == '__main__':

    SimulateAgents()