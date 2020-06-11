# CIP graph figure

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


from ipeds_dict import cip2labels, cip4labels_df
from ipeds_df import df4

import tol_colors
my_cmap = tol_colors.tol_cset('muted')


def cipgraph(cip,
             cipdict={},
             shareyflag=True,
             cipnum=False,
             areagraph=False,
             rategraph=True,
             dropcip=False,
             ):
    '''
    Return a figure with a stacked area graph for particular CIP codes

        * cip:          CIP code
        * cipdict:      Read dict. into 'other' category
        * shareyflag:   Have axes share y-axis
        * cipnum:       Include CIP code in legend labels
        * areagraph:    Create area graphs
        * rategraph:    Create rate graph
        * dropcip:      Drop CIP codes from small majors from rate graph

    '''
    # from ipeds_dict import cip2labels, cip4labels_df
    # from ipeds_df import df4

    # Make CIP code a string
    if isinstance(cip, int):
        cip = str(cip)

    # if relevant, pass dictionary of cip codes to 'other' category
    if len(cipdict) != 0:
        # Invert map
        cipmap = {}
        for key, value in cipdict.items():
            for cipcode4 in value:
                cipmap.update({cipcode4: key})

        # create dataframe for all cip4 that replaces with ciptitle undefined
        cip_desc = cip4labels_df.loc[cip].reset_index()
        # create variable
        cip_desc['group'] = cip_desc['cip4'].map(cipmap)
        if cipnum is False:
            cip_desc['group'] = cip_desc.group.fillna(cip_desc['ciptitle2010'])
        else:
            cip_desc['group'] = (cip_desc.group.fillna(
                cip_desc['cip4'] + ': ' +
                cip_desc['ciptitle2010']))
        # drop title column
        cip_desc = cip_desc.drop(['ciptitle2010'], axis=1)
        # create as a dictionary that can be mapped
        cip_mapdict = cip_desc.set_index('cip4').to_dict()['group']

    # Create dataset
    # copy relevant portion of the dataset
    cipdf = df4.loc[df4['cip2'] == cip].copy()

    # create group variable
    if len(cipdict) != 0:
        groupvar = 'group'
        cipdf['group'] = cipdf['cip4'].map(cip_mapdict)
    else:
        groupvar = 'cip4'

    # aggregate by the group
    cipdf = cipdf.groupby(['year', groupvar]).aggregate('sum').unstack()

    # find the maximum value in dataframe; add 5% to be consistent with
    #   what matplotlib automatically does
    maxval = (cipdf.transform(lambda x: x / 1e3).stack()
              .groupby(['year']).aggregate('sum').values.max()) * 1.05

    # order graph elements; first find largest groups
    ciplist = ((cipdf.sum().groupby(groupvar).aggregate('sum') /
                cipdf.sum().sum()).sort_values(ascending=False))

    # re-order columns
    cipdf = cipdf.reindex(list(ciplist.index.values), axis=1, level=1)

    # rate data
    if rategraph:
        # keep only those cip that you want to graph
        if dropcip is True:
            keepcip = list(ciplist[ciplist.ge(.03)].index.values)
        else:
            keepcip = list(ciplist.index.values)
        # create dataset of rates
        ciprate_df = cipdf.stack(dropna=False)
        ciprate_df = ciprate_df.loc[pd.IndexSlice[:, keepcip], :]
        ciprate_df['rate'] = ciprate_df['ctotalw'] / ciprate_df['ctotalm']
        ciprate_df = ciprate_df['rate'].unstack()

    # Create figure
    if areagraph is True:
        fig, ax = plt.subplots(1, 2, sharey=shareyflag)

        # fig.set_size_inches(3*fig_width,3*fig_height)

        (cipdf['ctotalw'].transform(lambda x: x / 1e3)
            .plot.area(ax=ax[0], legend=None, color=my_cmap))
        (cipdf['ctotalm'].transform(lambda x: x / 1e3)
            .plot.area(ax=ax[1], legend=None, color=my_cmap))

        ax[0].set_title('Women')
        ax[1].set_title('Men')

        if shareyflag is True:
            ax[0].set_ylim((0, maxval))

        # remove label from x axis
        ax[0].set_xlabel('')
        ax[1].set_xlabel('')

        # fig.suptitle(cip2labels[cip], size=20pt)
        fig.suptitle(cip2labels[cip], x=0.5, y=1.05)

        handles, labels = ax[0].get_legend_handles_labels()
        if len(cipdict) != 0:
            txt_labels = labels
        else:
            # txt_labels = list(map(f
            #     cip4labels_df.loc[cip].to_dict()['ciptitle2010']
            #     .get, labels))
            txt_labels = list(map(
                cip4labels_df.loc[cip, 'ciptitle2010'].to_dict().get,
                labels))
        ax[0].legend(handles[::-1], txt_labels[::-1],
                     bbox_to_anchor=(0, 0), loc=3,
                     )

        # ax[0].get_legend().remove()


        # ax[1].legend(handles[::-1], txt_labels[::-1],
        #              bbox_to_anchor=(1.04, 0), loc=3,
        #              )
        # plt.tight_layout()
        # fig.subplots_adjust(bottom=0.55)

        # plt.show()

        # ax[1].text(x='')

        return fig

    # Create second figure showing rates
    if rategraph is True:
        fig, ax = plt.subplots(1, 1)

        # Create list of columns
        # Index is year, columns are real names of variables
        cols = ciprate_df.columns
        cols_label = ciprate_df.columns.to_list()
        print(cols_label[0])

        # list of colors you need
        color_list = list(tol_colors.tol_cset('bright'))
        color_list = color_list[:len(cols)]

        for col, hex_color in zip(cols, color_list):
            # Plot the rate
            ciprate_df.plot(y=col, ax=ax, color=hex_color)
            # Find text defaults
            y_pos = ciprate_df.loc[2018, col]
            print((2018.5, y_pos))
            # Can add some manual adjustments to the text
            ax.text(x=2018.5, y=y_pos,
                    # s=cols_label[col],
                    s = col,
                    color=hex_color, fontsize=20
                    )
        ax.get_legend().remove()
        # Set limit to accomodate labels
        ax.set_xlim((1990, 2035))
        # ax.set_ylim(top=1.25)

        # remove label from x axis
        ax.set_xlabel('')

        # ax.set_title('Number of Bachelor\'s Degrees awarded (millions)')

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

        ax.set_title('Ratio of women to men - ' + cip2labels[cip])

        # ax.set_title('Ratio of women to men')

        # plt.show()
        return fig, ax



if __name__ == '__main__':
    cip11dict = {
        'Computer and information sciences and support, other':
            ['11.02', '11.99'],
        # 'Other': ['11.02', '11.03', '11.06', '11.99'],
    }
    cip42dict = {
        'Political science': ['45.10'],
        'International relations': ['45.09'],
        'Geography': ['45.07'],
        'Other': ['45.01', '45.05', '45.14', '45.03', '45.12', '45.13', '45.99']
    }
    # cipgraph(11, cipdict=cip11dict, cipnum=True, shareyflag=False,
    # cipgraph(45, cipdict=cip42dict, cipnum=True, shareyflag=False,
             # areagraph=True, rategraph=False)
    cipgraph(45, cipdict=cip42dict, cipnum=False, shareyflag=False,
             areagraph=False, rategraph=True)
    # fig, ax = cipgraph(11, cipdict=cip11dict, cipnum=True, shareyflag=False,
    #          areagraph=False, rategraph=True, dropcip=False)

    tikzplotlib.clean_figure()
    # default tikz (width, height) = (240pt, 207pt) (manual 4.10.01)
    tikzplotlib.save(imgpath + 'cip42_rat' + '.tex',
                     axis_height='207pt', axis_width='280pt')

    plt.show()
