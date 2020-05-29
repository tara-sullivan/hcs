import numpy as np
import pandas as pd
# import os

# # Plotting
# import matplotlib.pyplot as plt
# import tikzplotlib

# useful tools
from quantecon.util import timing
# import pdb
# from importlib import reload

# from other programs
import AFModel
# import plot_line_labels
AgentHistory = AFModel.AgentHistory
# plot_df = plot_line_labels.plot_df

# imgpath = os.path.join(os.path.dirname(os.getcwd()), 'img/')

sim_num_default = 100
ab_0_default = np.array([[1, 1], [1, 1]])
w_default = np.array([1, 1])
v_default = np.array([1, 1])
ability_default = np.array([0.5, 0.5])

# # This is used for an 0-1, 1-b concordacne, but ill make it general
# # alph_list = list(string.ascii_uppercase)
# alph_list = ['X', 'Y']
# alph_dict = {key: alph_list[key] for key in range(len(alph_list))}


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
                 ab_0_arg=None,     # initial human capital levels
                 w_arg=None,        # default sector-specific wages
                 v_arg=None,        # human capital update amount
                 ability_arg=None,  # true ability
                 sim_num_arg=None   # number of simuations to run
                 ):
        # Use default values if no argument called
        if ab_0_arg is not None:
            self.ab_0 = ab_0_arg
        else:
            self.ab_0 = ab_0_default

        if w_arg is not None:
            self.w = w_arg
        else:
            self.w = w_default

        if v_arg is not None:
            self.v = v_arg
        else:
            self.v = v_default

        if sim_num_arg is not None:
            self.sim_num = sim_num_arg
        else:
            self.sim_num = sim_num_default

        # Ability default takes a couple more arguments
        # Number of courses
        self.N_j = np.size(self.ab_0, axis=0)
        if ability_arg is not None:
            # pass the whole population of abilities
            if ability_arg.shape == (self.sim_num, self.N_j):
                self.ability = ability_arg
            # otherwise you need to broadcast given ability to population
            else:
                self.ability = np.broadcast_to(ability_arg,
                                               (self.sim_num, self.N_j))
        # If no ability arg given, broadcast default ability to population
        else:
            self.ability = np.broadcast_to(ability_default,
                                           (self.sim_num, self.N_j))

        # Call instance of AFModel
        self.afm = AgentHistory(ab_0=self.ab_0,
                                wages=self.w,
                                v=self.v)

        # Run simulatiofn
        outcome = self.run_sim()
        self.course_history = outcome.course_history
        self.chosen_field = outcome.chosen_field
        self.field_state = outcome.field_state

    def run_sim(self):
        '''
        Simulate agents using afm model
        '''
        # simplify notation
        sim_num = self.sim_num
        ability = self.ability
        afm = self.afm
        # initialize arrays
        chosen_field = np.empty(sim_num, dtype=int)
        field_state = np.empty((sim_num, 2))
        course_history_list = []

        print('Running...')
        timing.tic()
        for i in range(sim_num):
            # Create agent's history
            # Optional arguments include fail_first, choose_first
            history = afm.history_i(ability[i])

            # Fill in result arrays
            chosen_field[i] = history.chosen_field
            field_state[i] = history.field_state
            # Create a list of dataframes; quicker to concatenate later
            course_history_list.append(
                pd.DataFrame(list(zip(history.c_t, history.c_outcome)),
                             columns=['subject', 'outcome']))
        timing.toc()
        # concatenate dataframes for full course history
        course_history = pd.concat(course_history_list,
                                   keys=range(sim_num),
                                   names=['student', 't'])
        return self.return_sim(chosen_field, field_state, course_history)

    # return nicely formated results from simulation
    class return_sim:
        def __init__(self, chosen_field, field_state, course_history):
            self.chosen_field = chosen_field
            self.field_state = field_state
            self.course_history = course_history


# def course_history_df(course_history):
#     # For some buggy reason, margins=True doesn't seem to work
#     df = (course_history.pivot_table(index='t', columns='subject',
#                                      aggfunc='count', margins=False
#                                      ).fillna(0))
#     # remove extraneous column
#     df = df['outcome']
#     # Create the frequency table
#     df = df / df.loc[0, :].sum()

#     # Drop rows when people start finishing their education
#     # get counts of the counts of the time index
#     temp = np.unique(sim.course_history.index.get_level_values(1),
#                      return_counts=True)
#     # once students start finishing programs, the count is < sim_num
#     # find first occurance of when that happens
#     idx = np.min(np.argwhere(temp[1] < sim.sim_num)) - 1
#     # eliminate observations after above
#     df = df.loc[:idx]

#     return df


# def col_dict(df):
#     cols = list(df.columns)
#     col_dict = {num: 'Field ' + alph_dict[int(num[-1])] for num in cols}
#     return col_dict


# def tikz_save(figname):
#     # tikzplotlib.clean_figure()
#     # default tikz (width, height) = (240pt, 207pt) (manual 4.10.01)
#     tikzplotlib.save(imgpath + figname + '.tex',
#                      axis_height='207pt', axis_width='240pt')


# def print_ab_0(ab_0):
#     str0 = r'Field ' + alph_dict[0] + ': ' + print_array(ab_0, 0)
#     str1 = r'Field ' + alph_dict[1] + ': ' + print_array(ab_0, 1)
#     str_all = str0 + '; ' + str1
#     return str_all


# def print_array(ab_0, idx):
#     str1 = r'$(\alpha_0, \beta_0)='
#     str2 = r'(' + str(ab_0[idx, 0]) + ', ' + str(ab_0[idx, 1]) + ')$'
#     str_all = str1 + str2
#     return str_all

# def print_v(v):
#     str0 = r'Field ' + alph_dict[0] \
#            + r': $\nu=' + str(np.round(v[0], 2)) + r'$'
#     str1 = r'Field ' + alph_dict[1] \
#            + r': $\nu=' + str(np.round(v[1], 2)) + r'$'
#     str_all = str0 + '; ' + str1
#     return str_all


if __name__ == '__main__':

    # # Simulate agent behavior - 100 times
    # np.random.seed(125)
    # sim = SimulateAgents(sim_num_arg=10000)
    # # Plot course history
    # title_str = 'Baseline Simulation'
    # label_edit = {'j0': -.08, 'j1': .03}
    # add_text = {'add_loc': (13, .03),
    #             'add_str': 'N simulations = ' + f'{sim.sim_num:,}'}
    # plot_course_history(course_history=sim.course_history,
    #                     title_str=title_str,
    #                     label_edit=label_edit,
    #                     add_text=add_text)

    # # Save figure using tikzplotlib
    # tikz_save('simulation_1000')

    # Simulation with fewer obs
    # np.random.seed(125)
    # sim = SimulateAgents(sim_num_arg=50)
    # # Plot course history
    # title_str = 'Baseline Simulation'
    # label_edit = {'j0': -.08, 'j1': .03}
    # add_text = {'add_loc': (15, .03),
    #             'add_str': 'N simulations = ' + str(sim.sim_num)}
    # plot_course_history(course_history=sim.course_history,
    #                     title_str=title_str,
    #                     label_edit=label_edit,
    #                     add_text=add_text)

    # # Save figure using tikzplotlib
    # tikz_save('simulation_50')

    # plt.show()

    # Simulate agent behavior
    # np.random.seed(519)
    # ab_0 = np.array([[1, 1], [2, 2]])
    # sim = SimulateAgents(ab_0_arg=ab_0)
    # # Plot course history
    # title_str = 'Field selection and initial beliefs \\\\ ' \
    #             + print_ab_0(ab_0)
    # label_edit = {}
    # add_text = {'add_loc': (15, .03),
    #             'add_str': 'N simulations = ' + str(sim.sim_num)}
    # plot_course_history(course_history=sim.course_history,
    #                     title_str=title_str,
    #                     label_edit=label_edit,
    #                     add_text=add_text)

    # # Save figure using tikzplotlib
    # tikz_save('belief_effect')

    # # Simulate agent behavior
    # np.random.seed(29)
    # wage = np.array([1, 1.5])
    # sim = SimulateAgents(w_arg=wage)
    # # Plot course history
    # title_str = 'Field selection and wages \\\\ ' \
    #             'Field ' + alph_dict[0] + ': ' + 'w = ' + str(wage[0]) + '; ' \
    #             + 'Field ' + alph_dict[1] + ': ' + 'w = ' + str(wage[1])
    # label_edit = {'j0': .03, 'j1': .03}
    # add_text = {'add_loc': (15, .03),
    #             'add_str': 'N simulations = ' + str(sim.sim_num)}
    # plot_course_history(course_history=sim.course_history,
    #                     title_str=title_str,
    #                     label_edit=label_edit,
    #                     add_text=add_text)

    # # plt.show()
    # # Save figure using tikzplotlib
    # tikz_save('wage_effect')

    # # Underlying abiltiy 
    # # Simulate agent behavior
    # np.random.seed(29)
    # ability = np.array([.25, .75])
    # sim = SimulateAgents(ability_arg=ability)
    # # Plot course history
    # title_str = 'Field selection and ability to succeed \\\\ ' \
    #             'Field ' + alph_dict[0] + ': ' + 'ability = ' + str(ability[0]) + '; ' \
    #             + 'Field ' + alph_dict[1] + ': ' + 'ability = ' + str(ability[1])
    # label_edit = {'j0': .03, 'j1': .03}
    # add_text = {'add_loc': (15, .03),
    #             'add_str': 'N simulations = ' + str(sim.sim_num)}
    # plot_course_history(course_history=sim.course_history,
    #                     title_str=title_str,
    #                     label_edit=label_edit,
    #                     add_text=add_text)

    # # Save figure using tikzplotlib
    # tikz_save('ability_effect')

    # (r'$' + str(xtick) + r'$' for xtick in xticks)



    # Initial human capital
    # Create simulation and dataframe
    np.random.seed(29)
    sim = SimulateAgents(v_arg=v)
    df = course_history_df(sim.course_history)
    # arguments for plotting
    title_str = 'Field selection and human capital updating \\\\ ' \
                + print_v(v)
    label_edit = {'j0': .03, 'j1': .03}
    add_text = {'add_loc': (15, .03),
                'add_str': 'N simulations = ' + str(sim.sim_num)}
    plot_df(df=df,
            cols=list(df.columns), col_labels=col_dict(df),
            title=title_str,
            label_edit=label_edit,
            add_text=add_text)
    # Save figure using tikzplotlib
    tikz_save('v_effect')

    plt.show()
