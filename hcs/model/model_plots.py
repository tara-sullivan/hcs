import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt

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

# Helpful tools
# import pdb
from importlib import reload

# get figure heigth and width
from img.code.figsize import ArticleSize
size = ArticleSize()
from img.code import tikzplotlib_functions as tplf
reload(tplf)

'''
Beta example plots

    * Beta distribution example - men and women with same mean, different var
    * Beta distribution example - how beta changes (in slides)
    * Beta distribution exampel - B(1, 1) vs B(2, 2)
'''

from model import beta_distribution_example

plt.close('all')
beta_distribution_example.main()
plt.close('all')

print('Saved examples of beta distribution.')

'''
Simulations

    * Baseline simulations - N = 10000
    * Baseline simulations - N = 50
    * Change wages
    * Ability effect
    * Change initial beliefs

Bug: if I call np.random.seed doesn't appear to work with njit class.
Need to comment out decorator in afmodel.py for code to run quickly.
'''

# from other programs
from model import sim_plots
reload(sim_plots)
course_history_df = sim_plots.course_history_df
make_sim_plots = sim_plots.make_sim_plots
fmt_subtitle = sim_plots.fmt_subtitle
from model import sim_agents
SimulateAgents = sim_agents.SimulateAgents

# Initialize figure for paper
fig_all, ax = plt.subplots(3, 2)
# Will add a caption for the whole figure and individual titles at the end.
group_caption = 'Simulations of simple version of model.'
subplot_titles = ''
ref_name = 'fig:sim'
# node code for making subplot titles

#####################################
# Baseline simulation - 10000 times #
#####################################
# Create simulation and dataframe
np.random.seed(125)
sim = SimulateAgents(sim_num=10000)
df = course_history_df(sim)
# arguments for plotting
plt_title = 'Baseline Simulation'
label_edit = {0: -.08, 1: .03}
ax_loc = [0, 0]
subtitle_id = 'a'

make_sim_plots(figname='simulation_1000',
               df=df, ax_loc=ax_loc, group_ax=ax[ax_loc[0], ax_loc[1]],
               subtitle_id=subtitle_id,
               plt_title=plt_title, sim_num=sim.sim_num,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1],
               label_edit=label_edit,
               )
group_caption = group_caption + ' Figure (' + subtitle_id + ')' \
    + ' presents the baseline for ' + r'$N = {:,}$'.format(sim.sim_num) \
    + ' simulations;'
subplot_titles = subplot_titles + tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, subtitle_id=subtitle_id,
    plt_title=plt_title.replace('Field selection and ', '').capitalize(),
)

##################################
# Baseline simulation - 50 times #
##################################
# Create simulation and dataframe
np.random.seed(125)
sim = SimulateAgents(sim_num=50)

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

group_caption = group_caption + ' figure (' + subtitle_id + ')' \
    + ' does the same for the first {:,} simulations.'.format(sim.sim_num)
subplot_titles = subplot_titles + tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, subtitle_id=subtitle_id,
    plt_title=plt_title.replace('Field selection and ', '').capitalize(),
)

################
# Change wages #
################
np.random.seed(29)
wage = np.array([1, 1.5])
sim = SimulateAgents(w=wage)
df = course_history_df(sim)
# arguments for plotting
# plt_title = 'Field selection and wages \\\\ ' + print_w(wage)
plt_title = 'Field selection and wages '
subtitle_dict = {'var_tex': r'w', 'var': wage}
label_edit = {0: .03, 1: .03}
ax_loc = [1, 0]
subtitle_id = 'c'

make_sim_plots('wage_effect',
               df=df, ax_loc=ax_loc, group_ax=ax[ax_loc[0], ax_loc[1]],
               plt_title=plt_title, sim_num=sim.sim_num,
               subtitle_id=subtitle_id,
               plt_subtitle=True, subtitle_dict=subtitle_dict,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
               label_edit=label_edit,
               )

group_caption = group_caption \
    + ' The remaining figures have ' + r'$N = {:,}$'.format(sim.sim_num) \
    + ' simulations.' \
    + ' Figure (' + subtitle_id + ') repeats the simulations' \
    + ' for ' + fmt_subtitle(subtitle_dict, 'short', ' and') + '.'
subplot_titles = subplot_titles + tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, subtitle_id=subtitle_id,
    plt_title=plt_title.replace('Field selection and ', '').capitalize(),
)

##################
# Ability effect #
##################
# Create simulation and dataframe
np.random.seed(29)
ability = np.array([.4, .6])
sim = SimulateAgents(ability=ability)
df = course_history_df(sim)
# arguments for plotting
plt_title = 'Field selection and ability to succeed'
subtitle_dict = {'var_tex': r'\theta', 'var': ability}
label_edit = {0: .03, 1: .03}
ax_loc = [1, 1]
subtitle_id = 'd'

make_sim_plots('ability_effect',
               df=df, ax_loc=ax_loc, group_ax=ax[ax_loc[0], ax_loc[1]],
               plt_title=plt_title, sim_num=sim.sim_num,
               subtitle_id=subtitle_id,
               plt_subtitle=True, subtitle_dict=subtitle_dict,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
               label_edit=label_edit,
               )

group_caption = group_caption \
    + ' Figure (' + subtitle_id + ') repeats the simulations when ' \
    + fmt_subtitle(subtitle_dict, 'short', ' and') + '.'
subplot_titles = subplot_titles + tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, subtitle_id=subtitle_id,
    plt_title=plt_title.replace('Field selection and ', '').capitalize(),
)

##########################
# Change initial beliefs #
##########################
np.random.seed(519)
ab_0 = np.array([[1., 1.], [2., 2.]])
sim = SimulateAgents(ab_0=ab_0)
df = course_history_df(sim)
# arguments for plotting
plt_title = 'Field selection and initial beliefs'
subtitle_dict = {'var_tex': 'ab_0', 'var': ab_0}
label_edit = {}
ax_loc = [2, 0]
subtitle_id = 'e'

make_sim_plots('belief_effect',
               df=df, ax_loc=ax_loc, group_ax=ax[ax_loc[0], ax_loc[1]],
               plt_title=plt_title, sim_num=sim.sim_num,
               subtitle_id=subtitle_id,
               plt_subtitle=True, subtitle_dict=subtitle_dict,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
               label_edit=label_edit,
               )

group_caption = group_caption \
    + ' Figure (' + subtitle_id + ') repeats the simulations when ' \
    + fmt_subtitle(subtitle_dict, 'short', ' and') + '.'
subplot_titles = subplot_titles + tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, subtitle_id=subtitle_id,
    plt_title=plt_title.replace('Field selection and ', '').capitalize(),
)

###################
# Save group plot #
###################

ax[2, 1].axis('off')

tplf.save_subplots(
    filepath=imgpath + 'sim_plots.tex',
    figure=fig_all, xlabel_loc='right',
    node_code=subplot_titles, caption=group_caption,
)

plt.close('all')

##########################
# Make equal first round #
##########################
# Create simulation and dataframe
np.random.seed(629)
delta = sim.afm.delta
ab_0 = np.array([[1., 1.], [2., 2.]])
nx, ny = np.sum(ab_0, axis=1)
v = np.array([
    (delta**(nx - ny) * (nx / ny) * (ab_0[1, 0] / ab_0[0, 0])),
    1])
sim = SimulateAgents(ab_0=ab_0, v=v)
df = course_history_df(sim)
# arguments for plotting
subtitle_dict = {'var_tex': r'\nu', 'var': np.round(v, 2)}
plt_title = fmt_subtitle(subtitle_dict, 'long')
subtitle_dict = {'var_tex': 'ab_0', 'var': ab_0}
label_edit = {}

make_sim_plots('belief_adj_effect',
               df=df,
               plt_title=plt_title, sim_num=sim.sim_num,
               plt_subtitle=True, subtitle_dict=subtitle_dict,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
               label_edit=label_edit,
               )

#########################
# Initial human capital #
#########################
# Create simulation and dataframe
np.random.seed(29)
sim = SimulateAgents(v=v)
df = course_history_df(sim)
# arguments for plotting
subtitle_dict = {'var_tex': r'\nu', 'var': np.round(v, 2)}
plt_title = fmt_subtitle(subtitle_dict, 'long')
label_edit = {0: .03, 1: .03}

make_sim_plots('v_effect',
               df=df,
               plt_title='', sim_num=sim.sim_num,
               plt_subtitle=False, subtitle_dict=subtitle_dict,
               xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
               label_edit=label_edit,
               )

# plot_df(df=df,
#         cols=list(df.columns), col_labels=col_dict(df),
#         title=title_str,
#         xticks=[0, 5, 10, 15, 20], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
#         label_edit=label_edit,
#         add_text=add_text)
# tikz_save('v_effect')
