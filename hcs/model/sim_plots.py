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
import pdb
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

    def make_sim_plots(self, figname, ax_loc=None, plt_title='',
                       plt_subtitle=False, subtitle_dict=None,
                       sim_num=None,
                       *args, **kwargs):
        '''
        Run the plotting code twice; once to save a standalone figure that can
        be used in a presentation, and once to save a combined figure for the
        paper.

        * figname: string to name the figure
        * ax_loc: axes for the subplot
        * plt_title: title of plot
        * plt_subtitle: optional subtitle of plot
        * (*args, **kwargs) wraps plot_df signature

        '''

        # Create the standalone version of the figure
        # Shared characteristics
        kwargs['x_title'] = 't'
        kwargs['y_title'] = 'Fraction students enrolled in field'
        kwargs['x_lim'] = 27
        kwargs['col_labels'] = self.col_dict(df)

        # create the text to add
        if sim_num is not None:
            if sim_num < 999:
                loc_num = 18
            else:
                loc_num = 17
            kwargs['add_text'] = {'add_loc': (loc_num, .03),
                                  'add_str': 'N simulations = '
                                  + '{:,}'.format(sim.sim_num)}

        # Create the title for the standalone version
        if plt_subtitle is False:
            kwargs['title'] = plt_title
        else:
            kwargs['title'] = plt_title + ' \\\\ ' \
                + self.fmt_subtitle(subtitle_dict=subtitle_dict, length='long')

        # Initialize standalone figure
        fig_standalone, ax_standalone = plt.subplots()
        # Create standalone figure
        plot_df(ax=ax_standalone, *args, **kwargs)
        # Save standalone version of the graph
        tpl.clean_figure(fig_standalone)
        tpl.save(figure=fig_standalone, filepath=imgpath + figname + '.tex',
                 axis_height=size.h(1.3), axis_width=size.w(1.2))
        # print('saved ' + figname)
        plt.close(fig_standalone)

        if ax_loc is not None:
            if ax_loc[1] == 0:
                kwargs['y_title'] = 'Fraction enrolled in field'
            else:
                kwargs['y_title'] = ''

            if ax_loc[0] == 2:
                kwargs['x_title'] = 't'
            else:
                kwargs['x_title'] = ''

            # Create the title for the grouped version
            if plt_subtitle is False:
                kwargs['title'] = plt_title
            else:
                kwargs['title'] = self.fmt_subtitle(subtitle_dict=subtitle_dict,
                                        length='short')

            # Remove labels
            # kwargs['col_labels'] = {k: '' for k, v in
            #                         kwargs['col_labels'].items()}
            # Remove the text 'simulation'
            if sim_num is not None:
                kwargs['add_text']['add_str'] = (kwargs['add_text']['add_str']
                                                 .replace('simulations ', ''))
                # Change location of the simulation number
                kwargs['add_text']['add_loc'] = \
                    (3, kwargs['add_text']['add_loc'][1])

            plot_df(ax=ax[ax_loc[0], ax_loc[1]], *args, **kwargs)

    def col_dict(self, df):
        '''
        Create dictionary of columns and labels they should have
        '''

        cols = list(df.columns)
        col_dict = {num: 'Field ' + self.alph_dict[num]
                    for num in cols}

        return col_dict

    def fmt_subtitle(self, subtitle_dict, length):
        # String for the variable name ; i.e. '\theta' or '\theta_x'
        if length == 'long':
            var_str = subtitle_dict['var_tex']
            # Exception for ab_0
            if subtitle_dict['var_tex'] == 'ab_0':
                var_str = r'(\alpha_{0}, \beta_{0})'
            # One version for j=0, one version for j=1
            str0 = r'$' + var_str
            str1 = r'$' + var_str
        if length == 'short':
            # a string for j=0 and j=1
            str0 = r'$' + subtitle_dict['var_tex'] \
                   + r'_{' + self.alph_dict[0] + '}'
            str1 = r'$' + subtitle_dict['var_tex'] \
                   + r'_{' + self.alph_dict[1] + '}'
            # Exception for ab_0
            if subtitle_dict['var_tex'] == 'ab_0':
                str0 = r'$' + r'(\alpha_{' + self.alph_dict[0] + r', 0}, ' \
                       r'\beta_{' + self.alph_dict[0] + r', 0})'
                str1 = r'$' + r'(\alpha_{' + self.alph_dict[1] + r', 0}, ' \
                       r'\beta_{' + self.alph_dict[1] + r', 0})'
        # Add 'Field j: ' for long version
        if length == 'long':
            str0 = r'Field ' + self.alph_dict[0] + ': ' + str0
            str1 = r'Field ' + self.alph_dict[1] + ': ' + str1
        # Find value for j = 0 and j = 1
        if subtitle_dict['var_tex'] == 'ab_0':
            val0 = '({0[0]:g}, {0[1]:g})'.format(subtitle_dict['var'][0, :])
            val1 = '({0[0]:g}, {0[1]:g})'.format(subtitle_dict['var'][0, :])
        else:
            val0 = '{0:g}'.format(subtitle_dict['var'][0])
            val1 = '{0:g}'.format(subtitle_dict['var'][1])
        str0 = str0 + ' = ' + val0 + r'$'
        str1 = str1 + ' = ' + val1 + r'$'
        str_all = str0 + '; ' + str1
        return str_all

    def print_v(self, v, length):
        '''
        Print human capital accumulation
        '''
        if length == 'long':
            str0 = r'Field ' + self.alph_dict[0] + r': $\nu'
            str1 = r'Field ' + self.alph_dict[1] + r': $\nu'
        if length == 'short':
            str0 = r'$\theta_{' + self.alph_dict[0] + '}'
            str1 = r'$\theta_{' + self.alph_dict[1] + '}'
        str0 = str0 + ' = {0:g}'.format(np.round(v[0], 2)) + r'$'
        str1 = str1 + ' = {0:g}'.format(np.round(v[1], 2)) + r'$'
        # str0 = r'Field ' + self.alph_dict[0] \
        #        + r': $\nu=' + str(np.round(v[0], 2)) + r'$'
        # str1 = r'Field ' + self.alph_dict[1] \
        #        + r': $\nu=' + str(np.round(v[1], 2)) + r'$'
        str_all = str0 + '; ' + str1

        return str_all


# if __name__ == '__main__':

plt.close('all')

# # simplify notation
pf = PlotFuncs()
# # tikz_save = pf.tikz_save
# col_dict = pf.col_dict
# print_ab_0 = pf.print_ab_0
# print_v = pf.print_v
# print_w = pf.print_w
# print_ability = pf.print_ability
make_sim_plots = pf.make_sim_plots

# Bug: if I call np.random.seed doesn't appear to work with njit class.

# Initialize figure for paper

fig_all, ax = plt.subplots(3, 2)

#####################################
# Baseline simulation - 10000 times #
#####################################
# Create simulation and dataframe
np.random.seed(125)
sim = SimulateAgents(sim_num=10000)
df = course_history_df(sim.course_history)
# arguments for plotting
plt_title = 'Baseline Simulation'
label_edit = {0: -.08, 1: .03}

# pdb.set_trace()
make_sim_plots('simulation_1000', ax_loc=(0, 0),
               df=df,
               plt_title=plt_title, sim_num=sim.sim_num,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1],
               label_edit=label_edit,
               )

##################################
# Baseline simulation - 50 times #
##################################
# Create simulation and dataframe
np.random.seed(125)
sim = SimulateAgents(sim_num=50)

df = course_history_df(sim.course_history)
# arguments for plotting
plt_title = 'Baseline Simulation (zoomed in)'
label_edit = {0: -.08, 1: .03}

make_sim_plots('simulation_50', ax_loc=(0, 1),
               df=df,
               plt_title=plt_title, sim_num=sim.sim_num,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1],
               label_edit=label_edit,
               )

################
# Change wages #
################
np.random.seed(29)
wage = np.array([1, 1.5])
sim = SimulateAgents(w=wage)
df = course_history_df(sim.course_history)
# arguments for plotting
# plt_title = 'Field selection and wages \\\\ ' + print_w(wage)
plt_title = 'Field selection and wages '
subtitle_dict = {'var_tex': r'w', 'var': wage}
label_edit = {0: .03, 1: .03}

make_sim_plots('wage_effect', ax_loc=(1, 0),
               df=df,
               plt_title=plt_title, sim_num=sim.sim_num,
               plt_subtitle=True, subtitle_dict=subtitle_dict,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
               label_edit=label_edit,
               )

##########################
# Change initial beliefs #
##########################
np.random.seed(519)
ab_0 = np.array([[1., 1.], [2., 2.]])
sim = SimulateAgents(ab_0=ab_0)
df = course_history_df(sim.course_history)
# arguments for plotting
plt_title = 'Field selection and initial beliefs'
subtitle_dict = {'var_tex': 'ab_0', 'var': ab_0}
label_edit = {}

make_sim_plots('belief_effect', ax_loc=(1, 1),
               df=df,
               plt_title=plt_title, sim_num=sim.sim_num,
               plt_subtitle=True, subtitle_dict=subtitle_dict,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
               label_edit=label_edit,
               )

##################
# Ability effect #
##################
# Create simulation and dataframe
np.random.seed(29)
ability = np.array([.25, .75])
sim = SimulateAgents(ability=ability)
df = course_history_df(sim.course_history)
# arguments for plotting
plt_title = 'Field selection and ability to succeed'
subtitle_dict = {'var_tex': r'\theta', 'var': ability}
label_edit = {0: .03, 1: .03}

make_sim_plots('ability_effect', ax_loc=(2, 0),
               df=df,
               plt_title=plt_title, sim_num=sim.sim_num,
               plt_subtitle=True, subtitle_dict=subtitle_dict,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
               label_edit=label_edit,
               )

# ##########################
# # Make equal first round #
# ##########################
# # Create simulation and dataframe
# np.random.seed(629)
# delta = sim.afm.delta
# ab_0 = np.array([[1., 1.], [2., 2.]])
# nx, ny = np.sum(ab_0, axis=1)
# v = np.array([
#     (delta**(nx - ny) * (nx / ny) * (ab_0[1, 0] / ab_0[0, 0])),
#     1])
# sim = SimulateAgents(ab_0=ab_0, v=v)
# df = course_history_df(sim.course_history)
# # arguments for plotting
# plt_title = print_v(v) #+ ' \\\\ ' + print_ab_0(ab_0, length=long)
# add_text = {'add_loc': (18, .03),
#             'add_str': 'N simulations = ' + '{:,}'.format(sim.sim_num)}

# make_sim_plots('belief_adj_effect',
#                df=df, col_labels=col_dict(df),
#                # cols=list(df.columns),
#                plt_title=plt_title,
#                xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
#                add_text=add_text)
# # tpl.save(imgpath + 'belief_adj_effect.tex',
# #          axis_height=size.h(), axis_width=size.w())

# #########################
# # Initial human capital #
# #########################
# # Create simulation and dataframe
# np.random.seed(29)
# sim = SimulateAgents(v=v)
# df = course_history_df(sim.course_history)
# # arguments for plotting
# title_str = 'Field selection and human capital updating \\\\ ' \
#             + print_v(v)
# label_edit = {0: .03, 1: .03}
# add_text = {'add_loc': (14, .03),
#             'add_str': 'N simulations = ' + str(sim.sim_num)}
# plot_df(df=df,
#         cols=list(df.columns), col_labels=col_dict(df),
#         title=title_str,
#         xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
#         label_edit=label_edit,
#         add_text=add_text)
# tikz_save('v_effect')

ax[2, 1].axis('off')

tpl.clean_figure(fig_all)
tpl.save(imgpath + 'sim_plots.tex',
         axis_height=size.h(), axis_width=size.w(),
         extra_groupstyle_parameters={'horizontal sep=1.2cm',
                                      'vertical sep=1.8cm'})
