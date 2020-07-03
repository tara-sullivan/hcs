import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
import tikzplotlib as tpl

# Handle file paths; set root directory
import os
import sys
import inspect
try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
rootdir = os.path.dirname(os.path.dirname(currpath))
sys.path.append(rootdir)
# Change to image path
imgpath = rootdir + '/img/'

# from other programs
from model import sim_agents
SimulateAgents = sim_agents.SimulateAgents
from img.code import plot_line_labels
plot_df = plot_line_labels.plot_df
# # get figure heigth and width
from img.code.figsize import ArticleSize
size = ArticleSize()

# useful tools
# import pdb
# from importlib import reload


def course_history_df(course_history):
    '''
    Create dataframe from simulation of agents to plot
    '''
    # For some buggy reason, margins=True doesn't seem to work
    df = (course_history.pivot_table(index='t', columns='subject',
                                     aggfunc='count', margins=False
                                     ).fillna(0))
    # remove extraneous column
    df = df['outcome']

    # keep only simulations where no one has graduated
    sim_num = np.sum(df.loc[0])
    # counts at each time index
    temp = np.unique(course_history.index.get_level_values(1),
                     return_counts=True)
    # once students start finishing programs, the count is < sim_num
    # find first occurance of when that happens
    idx = np.min(np.argwhere(temp[1] < sim_num)) - 1
    # eliminate observations after above
    df = df.loc[:idx]

    # Create the frequency table
    df = df / df.loc[0, :].sum()

    return df


class PlotFuncs:
    '''
    Functions used when plotting figures
    '''
    def __init__(self):
        self.alph_list = ['X', 'Y']
        self.alph_dict = {key: self.alph_list[key]
                          for key in range(len(self.alph_list))}

    def tikz_save(self, figname):
        '''
        Save tikz figure using tikzplotlib
        '''
        # tikzplotlib.clean_figure()
        # default tikz (width, height) = (240pt, 207pt) (manual 4.10.01)
        tpl.save(imgpath + figname + '.tex',
                 axis_height=size.h(), axis_width=size.w())
        print('saved ' + figname)

    def col_dict(self, df):
        '''
        Create dictionary of columns and labels they should have
        '''

        cols = list(df.columns)
        col_dict = {num: 'Field ' + self.alph_dict[num]
                    for num in cols}

        return col_dict

    def print_ab_0(self, ab_0):
        '''
        String for printing ab_0
        '''

        def print_array(ab_0, idx):
            '''
            Print initial beliefs array as (a_0, b_0) = (v1, v2)
            '''
            str1 = r'$(\alpha_0, \beta_0)='
            str2 = r'(' + str(ab_0[idx, 0]) + ', ' + str(ab_0[idx, 1]) + ')$'
            str_all = str1 + str2
            return str_all

        str0 = r'Field ' + self.alph_dict[0] + ': ' + print_array(ab_0, 0)
        str1 = r'Field ' + self.alph_dict[1] + ': ' + print_array(ab_0, 1)
        str_all = str0 + '; ' + str1

        return str_all

    def print_w(self, wage):
        str0 = 'Field ' + self.alph_dict[0] + ': ' + 'w = ' + str(wage[0])
        str1 = 'Field ' + self.alph_dict[1] + ': ' + 'w = ' + str(wage[1])
        str_all = str0 + '; ' + str1
        return str_all

    def print_ability(self, ability):
        str0 = r'Field ' + self.alph_dict[0] \
               + r': $\theta=' + str(np.round(ability[0], 2)) + r'$'
        str1 = r'Field ' + self.alph_dict[1] \
               + r': $\theta=' + str(np.round(ability[1], 2)) + r'$'
        str_all = str0 + '; ' + str1
        return str_all

    def print_v(self, v):
        '''
        Print human capital accumulation
        '''
        str0 = r'Field ' + self.alph_dict[0] \
               + r': $\nu=' + str(np.round(v[0], 2)) + r'$'
        str1 = r'Field ' + self.alph_dict[1] \
               + r': $\nu=' + str(np.round(v[1], 2)) + r'$'
        str_all = str0 + '; ' + str1

        return str_all


if __name__ == '__main__':

    plt.close('all')

    # simplify notation
    pf = PlotFuncs()
    tikz_save = pf.tikz_save
    col_dict = pf.col_dict
    print_ab_0 = pf.print_ab_0
    print_v = pf.print_v
    print_w = pf.print_w
    print_ability = pf.print_ability

    # Bug: if I call np.random.seed doesn't appear to work with njit class.

    ##################################
    # Baseline simulation - 50 times #
    ##################################
    # Create simulation and dataframe
    np.random.seed(125)
    sim = SimulateAgents(sim_num=50)

    df = course_history_df(sim.course_history)
    # arguments for plotting
    title_str = 'Baseline Simulation'
    label_edit = {0: -.08, 1: .03}
    add_text = {'add_loc': (14, .03),
                'add_str': 'N simulations = ' + str(sim.sim_num)}
    plot_df(df=df, col_labels=col_dict(df),
            title=title_str,
            xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1],
            label_edit=label_edit,
            add_text=add_text)
    tikz_save('simulation_50')

    #####################################
    # Baseline simulation - 10000 times #
    #####################################
    # Create simulation and dataframe
    np.random.seed(125)
    sim = SimulateAgents(sim_num=10000)
    df = course_history_df(sim.course_history)
    # arguments for plotting
    title_str = 'Baseline Simulation'
    label_edit = {0: -.08, 1: .03}
    add_text = {'add_loc': (13, .03),
                'add_str': 'N simulations = ' + f'{sim.sim_num:,}'}
    plot_df(df=df, col_labels=col_dict(df),
            title=title_str,
            xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1],
            label_edit=label_edit,
            add_text=add_text)
    tikz_save('simulation_1000')

    ################
    # Change wages #
    ################
    np.random.seed(29)
    wage = np.array([1, 1.5])
    sim = SimulateAgents(w=wage)
    df = course_history_df(sim.course_history)
    # arguments for plotting
    title_str = 'Field selection and wages \\\\ ' + print_w(wage)
    label_edit = {0: .03, 1: .03}
    add_text = {'add_loc': (14, .03),
                'add_str': 'N simulations = ' + str(sim.sim_num)}
    plot_df(df=df, col_labels=col_dict(df),
            title=title_str,
            xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
            label_edit=label_edit,
            add_text=add_text)
    tikz_save('wage_effect')

    ##########################
    # Change initial beliefs #
    ##########################
    np.random.seed(519)
    ab_0 = np.array([[1, 1], [2, 2]])
    sim = SimulateAgents(ab_0=ab_0)
    df = course_history_df(sim.course_history)
    # arguments for plotting
    title_str = 'Field selection and initial beliefs \\\\ ' \
                + print_ab_0(ab_0)
    label_edit = {}
    add_text = {'add_loc': (14, .03),
                'add_str': 'N simulations = ' + str(sim.sim_num)}
    plot_df(df=df, col_labels=col_dict(df),
            title=title_str,
            xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
            label_edit=label_edit,
            add_text=add_text)
    tikz_save('belief_effect')

    ##########################
    # Make equal first round #
    ##########################
    # Create simulation and dataframe
    np.random.seed(629)
    delta = sim.afm.delta
    ab_0 = np.array([[1, 1], [2, 2]])
    nx, ny = np.sum(ab_0, axis=1)
    v = np.array([
        (delta**(nx - ny) * (nx / ny) * (ab_0[1, 0] / ab_0[0, 0])),
        1])
    sim = SimulateAgents(ab_0=ab_0, v=v)
    df = course_history_df(sim.course_history)
    # arguments for plotting
    title_str = print_v(v) + ' \\\\ ' + print_ab_0(ab_0)
    add_text = {'add_loc': (13, .03),
                'add_str': 'N simulations = ' + str(sim.sim_num)}
    plot_df(df=df,
            cols=list(df.columns), col_labels=col_dict(df),
            title=title_str,
            xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
            add_text=add_text)
    tpl.save(imgpath + 'belief_adj_effect.tex',
             axis_height=size.h(), axis_width=size.w())

    #########################
    # Initial human capital #
    #########################
    # Create simulation and dataframe
    np.random.seed(29)
    sim = SimulateAgents(v=v)
    df = course_history_df(sim.course_history)
    # arguments for plotting
    title_str = 'Field selection and human capital updating \\\\ ' \
                + print_v(v)
    label_edit = {0: .03, 1: .03}
    add_text = {'add_loc': (14, .03),
                'add_str': 'N simulations = ' + str(sim.sim_num)}
    plot_df(df=df,
            cols=list(df.columns), col_labels=col_dict(df),
            title=title_str,
            xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
            label_edit=label_edit,
            add_text=add_text)
    tikz_save('v_effect')

    ##################
    # Ability effect #
    ##################
    # Create simulation and dataframe
    np.random.seed(29)
    ability = np.array([.25, .75])
    sim = SimulateAgents(ability=ability)
    df = course_history_df(sim.course_history)
    # arguments for plotting
    title_str = 'Field selection and ability to succeed \\\\ ' + print_ability(ability)
    label_edit = {0: .03, 1: .03}
    add_text = {'add_loc': (14, .03),
                'add_str': 'N simulations = ' + str(sim.sim_num)}
    plot_df(df=df,
            cols=list(df.columns), col_labels=col_dict(df),
            title=title_str,
            xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
            label_edit=label_edit,
            add_text=add_text)
    tikz_save('ability_effect')

    plt.show()
