# Male dominated fields in IPEDS
import matplotlib.pyplot as plt

import os
import sys
import inspect

try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
rootdir = os.path.dirname(os.path.dirname(currpath))
sys.path.append(rootdir)

from ipeds.make_df import df
from img.code import plot_line_labels
plot_df = plot_line_labels.plot_df

imgpath = rootdir + '/img/'


def plot_n_degrees():
    # Define dataframe
    cipdf = (df.groupby(['year']).aggregate('sum')
             .transform(lambda x: x / 1e6))
    cols = ['ctotalm', 'ctotalw']
    col_labels = {'ctotalm': 'Men', 'ctotalw': 'Women'}
    title_str = ('Number of Bachelor\'s Degrees awarded'
                 ' in US 4-year colleges (millions)')

    plot_df(df=cipdf, cols=cols, col_labels=col_labels, title=title_str)


if __name__ == '__main__':

    plot_n_degrees()
    plt.show()
