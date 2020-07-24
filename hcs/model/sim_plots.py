import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
import tikzplotlib as tpl
import string

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

alph_list = ['X', 'Y']
alph_dict = {key: alph_list[key] for key in range(len(alph_list))}
alph_lower = list(string.ascii_lowercase)


def course_history_df(sim):
    '''
    Create dataframe from simulation of agents to plot
    '''
    course_history = sim.course_history
    chosen_field = sim.chosen_field
    # For some buggy reason, margins=True doesn't seem to work
    df = (course_history.pivot_table(index='t', columns='subject',
                                     aggfunc='count', margins=False
                                     ).fillna(0))
    # remove extraneous column
    df = df['outcome']

    # counts at each time index
    # Last time period for each student
    graduation = (
        course_history.reset_index()
        .pivot_table('t', index='student', aggfunc='max')
    )
    # by field, when did each group exit
    min_t = graduation.groupby(chosen_field).min()
    # the maximum of these min values determines the end of df
    max_idx = min_t.max()[0]
    # eliminate observations after maximum idx
    df = df.loc[:max_idx]
    # replace with NaN for other values
    # pdb.set_trace()
    for subject in min_t.index.tolist():
        # pdb.set_trace()
        if min_t.loc[subject].item() < max_idx:
            # pdb.set_trace()
            grad_t = min_t.loc[subject][0] + 1
            # pdb.set_trace()
            df[subject].loc[grad_t:] = np.nan

    # temp = np.unique(course_history.index.get_level_values(1),
    #                  return_counts=True)
    # # once students start finishing programs, the count is < sim_num
    # # find first occurance of when that happens
    # idx = np.min(np.argwhere(temp[1] < sim_num)) - 1
    # # eliminate observations after above
    # df = df.loc[:idx]

    # Create the frequency table
    df = df / df.loc[0, :].sum()

    return df


def make_sim_plots(figname, ax_loc=None, group_ax=None, plt_title='',
                   plt_subtitle=False, subtitle_dict=None, subtitle_id=None,
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
    * subtitle_id: ID for each subtitle (i.e. '(a)')
    * (*args, **kwargs) wraps plot_df signature

    '''

    # Create the standalone version of the figure
    # Shared characteristics
    kwargs['x_title'] = 't'
    kwargs['y_title'] = 'Fraction students enrolled in field'
    kwargs['x_lim'] = 30
    kwargs['col_labels'] = col_dict(kwargs['df'])

    # create the text to add
    if sim_num is not None:
        if sim_num < 999:
            loc_num = 18
        else:
            loc_num = 16
        kwargs['add_text'] = {'add_loc': (loc_num, .03),
                              'add_str': 'N simulations = '
                              + '{:,}'.format(sim_num)}

    # Create the title for the standalone version
    if plt_subtitle is False:
        kwargs['title'] = plt_title
    else:
        kwargs['title'] = plt_title + ' \\\\ ' \
            + fmt_subtitle(subtitle_dict=subtitle_dict, length='long')

    # Initialize standalone figure
    fig_standalone, ax_standalone = plt.subplots()
    # Create standalone figure
    plot_df(ax=ax_standalone, *args, **kwargs)
    # Change some properties after plotting
    for line in ax_standalone.lines:
        # Change line width
        line.set_linewidth(2.0)
        # Add marker
        line.set_marker('x')

    # Save standalone version of the graph
    # pdb.set_trace()
    # tpl.clean_figure(fig_standalone)
    tpl.save(figure=fig_standalone, filepath=imgpath + figname + '.tex',
             axis_height=size.h(1.2), axis_width=size.w(1.3),)
    # print('saved ' + figname)
    plt.close(fig_standalone)

    if group_ax is not None and ax_loc is not None:
        if ax_loc[1] == 0:
            kwargs['y_title'] = 'Fraction enrolled in field'
        else:
            kwargs['y_title'] = ''

        kwargs['x_title'] = r'$t$'

        # Create the title for the grouped version
        if subtitle_id is not None:
            # title_str = plt_title.replace('Field selection and ', '')
            # title_str = title_str.capitalize()
            # kwargs['title'] = '(' + subtitle_id + ') ' + title_str
            kwargs['title'] = ''
        elif subtitle_dict is not None:
            kwargs['title'] = fmt_subtitle(subtitle_dict=subtitle_dict,
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
        # Casuallly undoing the previous three lines of code because i'm hungry
        kwargs['add_text'] = None
        # Move x axis to the inside
        group_ax.tick_params(axis='x', direction='in')

        plot_df(ax=group_ax, *args, **kwargs)

        # Change some properties after plotting
        for line in group_ax.lines:
            # Change line width
            line.set_linewidth(2.0)
            # Add marker
            line.set_marker('x')


def col_dict(df):
    '''
    Create dictionary of columns and labels they should have
    '''
    cols = list(df.columns)
    col_dict = {num: 'Field ' + alph_dict[num]
                for num in cols}

    return col_dict


def fmt_subtitle(subtitle_dict, length, sep=';'):
    '''
    Format subtitle strings for plots. Creates two versions:

    long length: 'Field X: w = 1; Field Y: w = 1.5'
    short length: w_X = 1; w_Y = 1.5

    subtitle dict is a dictionary with the format:
        {
            'var_tex': xx,
            'var': yy
        }
    where xx is the LaTeX name for a variable (i.e. \theta or w) and yy is
    variable name in this program.

    Separately calculated for ab_0.
    '''
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
        str0 = r'${0}_{{{1}}}'.format(subtitle_dict['var_tex'], alph_dict[0])
        str1 = r'${0}_{{{1}}}'.format(subtitle_dict['var_tex'], alph_dict[1])
        # Exception for ab_0
        if subtitle_dict['var_tex'] == 'ab_0':
            str0 = r'$(\alpha_{{{x}0}}, \beta_{{{x}0}})'.format(x=alph_dict[0])
            str1 = r'$(\alpha_{{{y}0}}, \beta_{{{y}0}})'.format(y=alph_dict[1])
    # Add 'Field j: ' to long version
    if length == 'long':
        str0 = r'Field {j}: {exp}'.format(j=alph_dict[0], exp=str0)
        str1 = r'Field {j}: {exp}'.format(j=alph_dict[1], exp=str1)
    # Find value for j = 0 and j = 1
    if subtitle_dict['var_tex'] == 'ab_0':
        val0 = '({0[0]:g}, {0[1]:g})'.format(subtitle_dict['var'][0, :])
        val1 = '({0[0]:g}, {0[1]:g})'.format(subtitle_dict['var'][1, :])
    else:
        val0 = '{0:g}'.format(subtitle_dict['var'][0])
        val1 = '{0:g}'.format(subtitle_dict['var'][1])
    str0 = str0 + ' = ' + val0 + r'$'
    str1 = str1 + ' = ' + val1 + r'$'
    str_all = str0 + sep + ' ' + str1
    return str_all

#     def print_v(self, v, length):
#         '''
#         Print human capital accumulation
#         '''
#         if length == 'long':
#             str0 = r'Field ' + self.alph_dict[0] + r': $\nu'
#             str1 = r'Field ' + self.alph_dict[1] + r': $\nu'
#         if length == 'short':
#             str0 = r'$\theta_{' + self.alph_dict[0] + '}'
#             str1 = r'$\theta_{' + self.alph_dict[1] + '}'
#         str0 = str0 + ' = {0:g}'.format(np.round(v[0], 2)) + r'$'
#         str1 = str1 + ' = {0:g}'.format(np.round(v[1], 2)) + r'$'
#         # str0 = r'Field ' + self.alph_dict[0] \
#         #        + r': $\nu=' + str(np.round(v[0], 2)) + r'$'
#         # str1 = r'Field ' + self.alph_dict[1] \
#         #        + r': $\nu=' + str(np.round(v[1], 2)) + r'$'
#         str_all = str0 + '; ' + str1

#         return str_all


if __name__ == '__main__':
    plt.close('all')

    fig_all, ax = plt.subplots(3, 2)

    ##################################
    # Baseline simulation - 50 times #
    ##################################
    # Create simulation and dataframe
    np.random.seed(125)
    ab_0 = np.array([[1., 1.], [2., 2.]])
    sim = SimulateAgents(ab_0=ab_0, sim_num=50)
    # sim = SimulateAgents(sim_num=50)

    df = course_history_df(sim)
    # arguments for plotting
    plt_title = 'Baseline Simulation (zoomed in)'
    label_edit = {0: -.08, 1: .03}
    ax_loc = [0, 1]
    subtitle_id = 'b'

    make_sim_plots('simulation_50',
                   df=df, ax_loc=ax_loc, group_ax=ax[ax_loc[0], ax_loc[1]],
                   plt_title=plt_title, sim_num=sim.sim_num,
                   subtitle_id=subtitle_id,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1],
                   label_edit=label_edit,
                   )
    plt.show()

    # ability = np.array([.25, .75])
    # subtitle_dict = {'var_tex': r'\theta', 'var': ability}
    # print(fmt_subtitle(subtitle_dict, 'short'))
    # print(fmt_subtitle(subtitle_dict, 'long'))

    # ab_0 = np.array([[1., 1.], [2., 2.]])
    # subtitle_dict = {'var_tex': 'ab_0', 'var': ab_0}
    # print(fmt_subtitle(subtitle_dict, 'short'))
    # print(fmt_subtitle(subtitle_dict, 'long'))
