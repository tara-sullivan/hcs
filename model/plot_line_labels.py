# Plot line graphs of ipeds data, with the end of each line labeled

import matplotlib.pyplot as plt
import tol_colors

from itertools import cycle
import math

import pdb

def plot_df(df, cols=None, col_labels=None, title='',
            label_edit={}, x_lim=None,
            add_text=None, xticks=None, yticks=None):
    '''
    Plot line chart with labels at end of each line

        * df:           dataframe to plot; year shoudl be index
        * cols:         list of columns of dataframe to plot
        * col_labels:   column labels as a dictionary
        * title:        title of plot
        * label_edit:   manually edit position of label using dict
        * x_lim:        manually set the x-axis limit
        * add_text:     text to add
        * xticks:       list of xticks
        * yticks:       list of yticks
    '''

    # List of colors used
    color_list = list(tol_colors.tol_cset('bright'))
    # remove black
    color_list.remove('#000000')

    if cols is None:
        cols = list(df.columns)
    if col_labels is None:
        col_labels = {num: num for num in cols}

    # Initialize figure
    # pdb.set_trace()
    fig, ax = plt.subplots()

    for col, hex_color in zip(cols, cycle(color_list)):
        # Plot the rate
        df.plot(y=col, ax=ax, marker='x', color=hex_color)
        # Find text defaults
        last_idx = max(df.index.array)
        y_pos = df.loc[last_idx, col]
        # Can add some manual adjustments to the text
        if len(label_edit) > 0:
            for col_edit, adjustment in label_edit.items():
                if col == col_edit:
                    y_pos = y_pos + adjustment
        # Plot text for each line
        ax.text(x=20.5, y=y_pos, s=col_labels[col],
                color=hex_color, fontsize=20)
    ax.get_legend().remove()

    # get default x tick values
    if xticks is None:
        xticks = ax.get_xticks().tolist()

    # longest labels
    len_labels = max(len(value) for key, value in col_labels.items())
    if x_lim is None:
        max_x = 20 + max(5, math.floor(len_labels * .4))
    else:
        max_x = x_lim
    # Set limit to accomodate labels
    min_x, _ = ax.get_xlim()
    ax.set_xlim((min_x, max_x))
    ax.set_ylim((0, 1))

    # Get default y tick values
    if yticks is None:
        yticks = ax.get_yticks().tolist()

    # set ticks
    new_xticks = [tick for tick in xticks if
                  ((tick >= min_x) & (tick <= 20))]
    new_yticks = [tick for tick in yticks if ((tick >= 0) & (tick <= 1))]
    # xticklabels = [r'$' + str(int(xtick)) + r'$' for xtick in new_xticks]
    ax.set_xticks(new_xticks)
    ax.set_yticks(new_yticks)

    def tick_str_labels(ticks, round_num=2):
        # There's a weird thing going to tikzplotlib where it overrides ticks
        # unless you format them as strings
        if round_num == 0:
            ticks_str = [r'$' + str(tick) + r'$' for tick in ticks]
        else:
            ticks_str = [r'$' + str(round(tick, round_num)) + r'$' for tick in ticks]
        return ticks_str

    ax.set_xticklabels(tick_str_labels(new_xticks))
    ax.set_yticklabels(tick_str_labels(new_yticks))

    # Add any additional text
    if add_text is not None:
        # Added text should take the form:
        # add_text = {'add_loc': (1, 0.95), 'add_str': 'N simulations'}
        ax.text(x=add_text['add_loc'][0], y=add_text['add_loc'][1],
                s=add_text['add_str'], fontsize=20)

    # remove label from x axis
    ax.set_xlabel(r'$t$')
    ax.set_ylabel('Fraction students enrolled in field')

    ax.set_title(title)

    # Create grid
    ax.grid(axis='y', color='#000000', linewidth=.5, linestyle=':')
    # set ticks, if necessary
    # if xticks is not None:
    # Set ticks


    # Remove axes
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

if __name__ == '__main__':

    import simulate_timeline
    import plot_simulations
    SimulateAgents = simulate_timeline.SimulateAgents
    course_history_df = plot_simulations.course_history_df

    sim = SimulateAgents()
    df = course_history_df(sim.course_history)

    xticks = [-5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0]
    xlim = (-1.05, 25.0)
    # plot_df(df, xticks=[0, 5, 10, 20])

    plot_df(df)
    plt.show()
