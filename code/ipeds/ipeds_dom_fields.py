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


from ipeds_dict import cip2labels, cip2labels_short
from ipeds_df import df2

import tol_colors

# Maybe create a sciences graph?

# Biological sciences (26):
# Instructional programs that focus on the biological sciences and the
# non-clinical biomedical sciences, and that prepare individuals for
# research and professional careers as biologists and biomedical scientists

# Physical sciences (40):
# Instructional programs that focus on the scientific study of inanimate
# objects, processes of matter and energy, and associated phenomena


# Aggregate up to year and cip; keep only year 1990
cip1990 = df2.groupby(['year', 'cip2']).aggregate('sum').loc[1990]

# Create ratio variable
cip1990['rat'] = cip1990['ctotalw'] / cip1990['ctotalm']
# Sort by ratio
cip1990.sort_values(by='rat', ascending=False, inplace=True)

# Map labels to cip index; look at this to find appropriate cip
cip1990['cip2label'] = cip1990.index.to_series().map(cip2labels)

# Computer science
male_dom = ['14', '11', '40', '45', '27', '52']
female_dom = ['51', '50', '42', '16', '13']

#################
# Create figure #
#################

# # top 12 cip codes, aggregated
cip2df = (df2[df2['cip2'].isin(male_dom)]
          .groupby(['year', 'cip2']).aggregate('sum').unstack())

# # switch order of columns
cip2df.columns = cip2df.columns.swaplevel(0, 1)
cip2df.sort_index(axis=1, level=0, inplace=True)

# # reshape dataframe
cip2rate = cip2df.swaplevel(axis=1).stack()
cip2rate['rate'] = cip2rate['ctotalw'] / cip2rate['ctotalm']
cip2rate = cip2rate['rate'].unstack()

# Initialize figure
fig, ax = plt.subplots()

# list of colors you need
color_list = list(tol_colors.tol_cset('bright'))
color_list = color_list[:len(male_dom)]

for cip, hex_color in zip(male_dom, color_list):
    # Plot the rate
    cip2rate.plot(y=cip, ax=ax, color=hex_color)
    # Find text defaults
    y_pos = cip2rate.loc[2018, cip]
    # Can add some manual adjustments to the text
    if cip == '11':
        y_pos = y_pos - .02
    if cip == '40':
        y_pos = y_pos - .02
    ax.text(x=2018.5, y=y_pos, s=cip2labels_short[cip], 
            color=hex_color, fontsize=20)
ax.get_legend().remove()
# Set limit to accomodate labels
ax.set_xlim((1990, 2033))

ax.set_title('Ratio of women to men in historically male-dominated fields')

ax.text(x=1990, y=0, s='Source: IPEDS')

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
    tikzplotlib.save(imgpath + 'male_dom.tex',
                     axis_height='207pt', axis_width='300pt')

    plt.show()
