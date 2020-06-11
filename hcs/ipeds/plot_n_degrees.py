# Male dominated fields in IPEDS

import matplotlib.pyplot as plt
import tikzplotlib
import os

from make_df import df
import plot_line_labels
plot_df = plot_line_labels.plot_df

imgpath = os.path.join(os.path.dirname(os.getcwd()), 'img/')


def main():
    # Define dataframe
    cipdf = (df.groupby(['year']).aggregate('sum')
             .transform(lambda x: x / 1e6))
    cols = ['ctotalm', 'ctotalw']
    col_labels = {'ctotalm': 'Men', 'ctotalw': 'Women'}
    title_str = ('Number of Bachelor\'s Degrees awarded'
                 ' in US 4-year colleges (millions)')

    plot_df(df=cipdf, cols=cols, col_labels=col_labels, title=title_str)


if __name__ == '__main__':
    main()
    tikzplotlib.clean_figure()
    # default tikz (width, height) = (240pt, 207pt) (manual 4.10.01)
    tikzplotlib.save(imgpath + 'n_degrees' + '.tex',
                     axis_height='207pt', axis_width='260pt')

    plt.show()
