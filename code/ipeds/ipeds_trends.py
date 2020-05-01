# import numpy as np
# import pandas as pd
# import math
import os
from sys import platform, path

import matplotlib.pyplot as plt
import tikzplotlib

import json

# Handle file paths (this is something I should change in the future!)
my_os = platform
if my_os == 'darwin':
    home = ('/Users/tarasullivan/Google Drive File Stream/'
            'My Drive/research/hcs/')
elif my_os == 'win32':
    home = 'Z:/hcs/'
# os.chdir(home + '/code/ipeds/')
os.chdir(home)
path.append(home + '/code/ipeds/')

imgpath = home + 'img/'

# Create dataset (may want to comment this out)
from ipeds_df import df, df2, df4

# function for creating cip graph
from cip_graph import cipgraph

# Create dicitonaries
from ipeds_dict import cip2labels_short, cip2labels, cip4labels_df
label_dict = {'ctotalm': 'Men', 'ctotalw': 'Women'}


def dprint(dict):
    '''Nicely print dictionaries'''
    print(json.dumps(dict, indent=4))


# # figure size shit
# textwidth = 6.50127
# fig_width = textwidth / 2
# golden_mean = (math.sqrt(5) - 1.0) / 2.0
# fig_height = fig_width * golden_mean


#################################################
# Number of bachelor's degrees by men and women #
#################################################

def save_fig(fig, name):
    tikzplotlib.clean_figure(fig)
    tikzplotlib.save(imgpath + name + '.tex')


def plot_n_degrees(df, figname='n_degrees'):
    '''
    Plots the total number of bachelor's degrees awarded each year in millions

     * df: dataframe of total bachelor's degrees completed
     * figname: name to call figure. default is n_degrees.tex
    '''
    fig, ax = plt.subplots()

    df.groupby(['year']).aggregate('sum').transform(
        lambda x: x / 1e6).plot(ax=ax)

    handles, labels_list = ax.get_legend_handles_labels()
    ax.legend(list(map(label_dict.get, labels_list)))

    # remove label from x axis
    ax.set_xlabel('')

    ax.set_title('Number of Bachelors Degrees awarded (millions)')

    save_fig(fig, figname)


# Create n_degrees graph
# plot_n_degrees(df)

# Create lists of top CIP codes for men and women
# list of top 20 2-digit cip codes
cip2_2018 = df2.groupby(['year', 'cip2']).aggregate('sum').loc[2018]

# save values of top 20 index
top20 = cip2_2018.sum(axis=1).sort_values(
    ascending=False).iloc[:20].index.values
top12 = cip2_2018.sum(axis=1).sort_values(
    ascending=False).iloc[:12].index.values

# top 12 cip codes, aggregated
cip2df = df2[
    df2['cip2'].isin(top12)].groupby(
    ['year', 'cip2']).aggregate('sum').unstack()

# switch order of columns
cip2df.columns = cip2df.columns.swaplevel(0, 1)
cip2df.sort_index(axis=1, level=0, inplace=True)

#################################
# Top 12 - number men and women #
#################################


def n_top12(cip2df):

    fig, ax = plt.subplots(3, 4, sharex='col')

    # Figure size shit
    # fig.set_size_inches(2.4 * fig_width, 1.8 * fig_height)

    fig.tight_layout()

    for i in range(3):
        for j in range(4):
            k = i * 4 + j
            ax[i, j].plot(cip2df[top12[k]].transform(lambda x: x / 1e3))
            ax[i, j].set_title(cip2labels_short[top12[k]])

    # create legend (bug necessitates awkward language)
    ax[1, 3].legend(
        list(map(label_dict.get, cip2df[top12[0]].columns.to_list())),
        loc='center left', bbox_to_anchor=(1, .6))

    fig.suptitle('Bachelor\'s degrees awarded at postsecondary '
                 'institutions (thousands)',
                 x=0.5, y=1.1)


# n_top12(cip2df)

##################################
# Top 12 - Ratio of women to men #
##################################


def r_top12(cip2df):

    # reshape dataframe
    cip2rate = cip2df.swaplevel(axis=1).stack()
    cip2rate['rate'] = cip2rate['ctotalw'] / cip2rate['ctotalm']
    cip2rate = cip2rate['rate'].unstack()

    fig, ax = plt.subplots(3, 4, sharex='col')

    # Figure size shit
    # fig.set_size_inches(2.4 * fig_width, 1.8 * fig_height)

    fig.tight_layout()

    for i in range(3):
        for j in range(4):
            k = i * 4 + j
            ax[i, j].plot(cip2rate[top12[k]])
            ax[i, j].set_title(cip2labels_short[top12[k]])

    fig.suptitle('Ratio of women to men', x=0.5, y=1.1)


# r_top12(cip2df)

####################################
# CIP graphs for individual fields #
####################################

cip11dict = {
    'Computer and information sciences and support, other':
    ['11.02', '11.99'],
        # 'Other': ['11.02', '11.03', '11.06', '11.99'],
}
# fig = cipgraph(11,
#                cipdict=cip11dict,
#                cipnum=True,
#                shareyflag=False,
#                areagraph=True,
#                rategraph=False)

# name = 'n_cip11'
# tikzplotlib.clean_figure(fig)
# tikzplotlib.save(imgpath + name + '.tex',
#                  # axis_width='0.5\\textwidth',
#                  # axis_height='\\axisdefaultheight'
#                  )
# plt.show()
# plt.close()

fig = cipgraph(11,
               cipdict=cip11dict,
               cipnum=True,
               shareyflag=False,
               areagraph=False,
               rategraph=True,
               dropcip=False)
name = 'r_cip11'
tikzplotlib.clean_figure(fig)
tikzplotlib.save(imgpath + name + '.tex',
                 # axis_width='0.5\\textwidth',
                 # axis_height='\\axisdefaultheight'
                 )
plt.show()