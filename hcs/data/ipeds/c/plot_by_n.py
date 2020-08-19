# Male dominated fields in IPEDS
import pandas as pd
import matplotlib.pyplot as plt

import os
import sys
import inspect

try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
rootdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    currpath))))
sys.path.append(rootdir)

# from ipeds.historical_data.historical_df import make_df
from data.ipeds.c.clean_data.historical_data.historical_df import make_df
from data.ipeds.c.clean_data.make_df import df
from img.code import plot_line_labels
plot_df = plot_line_labels.plot_df

imgpath = rootdir + '/img/'


def plot_n_degrees(plot_title=False, ax=None, x_lim=None):
    # Modern data
    newdf = df.groupby(['year']).aggregate('sum')
    newdf = newdf.rename(columns={'ctotalm': 'men', 'ctotalw': 'women'})
    # historical data
    olddf = make_df()
    # Create dataset
    totdf = pd.concat([olddf, newdf])
    # Convert to millions
    totdf = totdf.transform(lambda x: x / 1e6)
    col_labels = {'men': 'Men', 'women': 'Women'}
    if plot_title is True:
        title_str = ('Number of Bachelor\'s Degrees awarded'
                     ' in US 4-year colleges (millions)')
        y_title = None
    else:
        title_str = ''
        y_title = 'Number degrees (millions)'

    plot_df(df=totdf.loc[1960:], col_labels=col_labels, ax=ax,
            title=title_str, y_title=y_title, x_lim=x_lim,
            xticks=[1960, 1970, 1980, 1990, 2000, 2010])


if __name__ == '__main__':

    fig, ax = plt.subplots()
    plot_n_degrees(ax=ax, x_lim=2018)

    # Edit the standalone version
    # Remove the in text labels
    ax.texts = []
    # Capitalize legend entries; move to upper left
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(labels=[x.capitalize() for x in labels],
              loc='upper left')

    plt.show()
