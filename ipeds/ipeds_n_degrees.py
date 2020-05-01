# Male dominated fields in IPEDS

import pandas as pd
import matplotlib.pyplot as plt
import tikzplotlib

# file paths
from sys import platform, path
import os

if __name__ == '__main__':
    # Ensure we're on the right home file
    my_os = platform
    if my_os == 'darwin':
        home = ('/Users/tarasullivan/Google Drive File Stream/'
                'My Drive/research/hcs/')
    elif my_os == 'win32':
        home = 'Z:/hcs/'
    os.chdir(home)
    path.append(home + '/code/ipeds/')
    imgpath = home + 'img/'

from ipeds_df import df

import tol_colors

# def plot_n_degrees(df, figname='n_degrees'):
# '''
# Plots the total number of bachelor's degrees awarded each year in millions

#  * df: dataframe of total bachelor's degrees completed
#  * figname: name to call figure. default is n_degrees.tex
# '''

# Create grouped dataset
cipdf = (df.groupby(['year']).aggregate('sum')
         .transform(lambda x: x / 1e6))

# Initialize figure
fig, ax = plt.subplots()

cols = ['ctotalm', 'ctotalw']
cols_label = {'ctotalm': 'Men', 'ctotalw': 'Women'}

# list of colors you need
color_list = list(tol_colors.tol_cset('bright'))
color_list = color_list[:len(cols)]

for col, hex_color in zip(cols, color_list):
    # Plot the rate
    cipdf.plot(y=col, ax=ax, color=hex_color)
    # Find text defaults
    y_pos = cipdf.loc[2018, col]
    # Can add some manual adjustments to the text
    ax.text(x=2018.5, y=y_pos, s=cols_label[col],
            color=hex_color, fontsize=20)
ax.get_legend().remove()
# Set limit to accomodate labels
ax.set_xlim((1990, 2025))
ax.set_ylim(top=1.25)

# remove label from x axis
ax.set_xlabel('')

ax.set_title('Number of Bachelor\'s Degrees awarded in US 4-year colleges (millions)')

# Create grid
ax.grid(axis='y', color='#000000', linewidth=.5, linestyle=':')
ax.set_xlabel('')
# Set ticks
ax.set_xticks((1990, 1995, 2000, 2005, 2010, 2015))
ax.set_xticklabels((r'$1990$', r'$1995$', r'$2000$',
                    r'$2005$', r'$2010$', r'$2015$'))
# Remove axes
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)

if __name__ == '__main__':
    tikzplotlib.clean_figure()
    # default tikz (width, height) = (240pt, 207pt) (manual 4.10.01)
    tikzplotlib.save(imgpath + 'n_degrees' + '.tex',
                     axis_height='207pt', axis_width='260pt')

    plt.show()