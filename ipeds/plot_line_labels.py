# Plot line graphs of ipeds data, with the end of each line labeled

import matplotlib.pyplot as plt
import tol_colors

from itertools import cycle
import math

if __name__ == '__main__':
    from make_df import df


def plot_df(df, cols, col_labels, title='', label_edit={}, x_lim=None):
    '''
    Plot line chart with labels at end of each line

        * df:           dataframe to plot; year shoudl be index
        * cols:         columns of dataframe to plot
        * col_labels:   column labels as a dictionary
        * title:        title of plot
        * label_edit:   manually edit position of label using dict
        * x_lim:        manually set the x-axis limit
    '''

    # List of colors used
    color_list = list(tol_colors.tol_cset('bright'))
    # remove black
    color_list.remove('#000000')

    # Initialize figure
    fig, ax = plt.subplots()

    for col, hex_color in zip(cols, cycle(color_list)):
        # Plot the rate
        df.plot(y=col, ax=ax, color=hex_color)
        # Find text defaults
        y_pos = df.loc[2018, col]
        # Can add some manual adjustments to the text
        if len(label_edit) > 0:
            for col_edit, adjustment in label_edit.items():
                if col == col_edit:
                    y_pos = y_pos + adjustment
        # Plot text for each line
        ax.text(x=2018.5, y=y_pos, s=col_labels[col],
                color=hex_color, fontsize=20)
    ax.get_legend().remove()

    # longest labels
    len_labels = max(len(value) for key, value in col_labels.items())
    if x_lim is None:
        max_x = 2018 + max(7, math.floor(len_labels * .8))
    else:
        max_x = x_lim
    # Set limit to accomodate labels
    ax.set_xlim((1990, max_x))
    # ax.set_ylim(top=1.25)

    # remove label from x axis
    ax.set_xlabel('')

    ax.set_title(title)

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

    # Create grouped dataset
    cipdf = (df.groupby(['year']).aggregate('sum')
             .transform(lambda x: x / 1e6))
    # columns to plot and their labels
    cols = ['ctotalm', 'ctotalw']
    col_labels = {'ctotalm': 'Men', 'ctotalw': 'Women'}
    label_edit = {'ctotalm': -.4}

    plot_df(df=cipdf,
            cols=cols,
            col_labels=col_labels,
            label_edit= label_edit,
            x_lim=2033
            )

    plt.show()
