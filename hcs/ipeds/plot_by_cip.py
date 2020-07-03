# Male dominated fields in IPEDS
import pandas as pd
import matplotlib.pyplot as plt
import tikzplotlib as tpl

import os
import sys
import inspect
import codecs

# import pdb
# from importlib import reload

try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
rootdir = os.path.dirname(os.path.dirname(currpath))
sys.path.append(rootdir)

# testdir = os.path.dirname(os.path.dirname(os.path.dirname(rootdir))) \
#     + '/tech/'
# sys.path.append(testdir)
# from tikzplotlib_clone.tikzplotlib import tikzplotlib as tpl
get_tikz_code = tpl._save.get_tikz_code
save = tpl._save.save


from img.code import tol_colors
from img.code import plot_line_labels
plot_df = plot_line_labels.plot_df

imgpath = rootdir + '/img/'

from ipeds.make_df import df4, cip2labels_short, cip4labels_df

# make 2-digit and 4-digit cip codes consistent
# in this program, concordance given by series
cip2labels = pd.Series(cip2labels_short)
cip4labels = cip4labels_df.droplevel(0).squeeze()


class PlotCIP:
    '''
    Plot either:
       1. The amount of men and women using a CIP code over time, or
       2. The ratio of women to men studying a CIP code over time.

    Requried variables:

        * cip_list:     CIP codes as a list

    Optional variables:

        * cip_dict:     Read dict. into graph
        * areagraph:    Create area graphs; default false
        * cip_inlabel:  Include CIP code in legend labels
        * rategraph:    Create rate graph; default true
        * shareyflag:   Have area graph axes share y-axis
        * dropcip:      Drop CIP codes from small majors from rate graph
        * drop_other:   Drop 'Other' category from dictionary
        * rate_title:   Title of rate graph
        * label_edit:   Pass a dictionary that moves labels to rate graph
        * area_leg:     Legend for area plot
    '''
    def __init__(self, cip_list, cip_dict=None,
                 rategraph=False, areagraph=False,
                 drop_other=False, cip_inlabel=False,
                 x_lim=None, rate_title=None, label_edit=None,
                 shareyflag=True, area_leg=None,
                 ):
        self.cip_list = cip_list
        if cip_dict is None:
            self.cip_dict = {}
        else:
            self.cip_dict = cip_dict.copy()
        # Initialize flags
        self.rategraph = rategraph
        self.areagraph = areagraph
        # formatting flags
        self.drop_other = drop_other
        self.cip_inlabel = cip_inlabel
        # formatting flags for rate graph
        self.x_lim = x_lim
        if rate_title is None:
            self.rate_title = 'Ratio of women to men'
        else:
            self.rate_title = rate_title + ' \\\\ ' \
                + 'Ratio of women to men'
        if label_edit is None:
            self.label_edit = {}
        else:
            self.label_edit = label_edit
        # formatting flags for area graph
        self.shareyflag = shareyflag
        if self.rategraph and self.areagraph and area_leg is None:
            self.area_leg = False
        elif area_leg is None:
            self.area_leg = True
        else:
            self.area_leg = area_leg
        # Create CIP labels and dataframe
        self.make_cip_df()
        # plot graph
        self.plot_cip()

    def make_cip_df(self):
        '''
        Make the CIP dataframe and dictionary that can be used to plot:
           1. The amount of men and women using a CIP code over time, or
           2. The ratio of women to men studying a CIP code over time
        '''
        # # Clean up notation
        # cip_list, cip_dict = self.cip_list, self.cip_dict
        # if only a single 2-digit cip code is passed, we want to plot the
        # components
        if (len(self.cip_list) == 1 and len(self.cip_list[0]) == 2
                and len(self.cip_dict) == 0):
            self.cip_list = [cip for cip in cip4labels.index
                             if cip.startswith(self.cip_list[0])]

        # 2 digit & 4 digit column labels
        cip_list_2d = [cip for cip in self.cip_list if len(cip) == 2]
        cip_list_4d = [cip for cip in self.cip_list if len(cip) != 2]

        # create a list of all the cip codes you need to find labels for
        if self.cip_dict == {}:
            cip_nolabel = self.cip_list
        else:
            cip_haslabel = [item for sublist in list(self.cip_dict.values())
                            for item in sublist]
            cip_nolabel = set(self.cip_list).difference(cip_haslabel)
        # for each code without a label, find the appropriate label and append
        # it to the col_label dictionary
        for cip in cip_nolabel:
            if cip in cip_list_2d:
                self.cip_dict[cip2labels.loc[cip]] = [cip]
            elif cip in cip_list_4d:
                self.cip_dict[cip4labels.loc[cip]] = [cip]

        # create a new cip column
        df4.loc[df4['cip2'].isin(cip_list_2d), 'cip'] = df4['cip2']
        df4.loc[df4['cip4'].isin(cip_list_4d), 'cip'] = df4['cip4']

        # create a single cip for cip codes that need to be aggregated together
        for key, value in self.cip_dict.items():
            if len(value) > 1:
                # find group_cip; this should either be either be equal to 99..
                group_cip = [cip for cip in value if cip.endswith('99')]
                # or it should be the last one in the group
                if len(group_cip) != 1:
                    group_cip = [value[-1]]
                # map these group cip codes to new group cip
                df4.loc[df4['cip2'].isin(value) | df4['cip4'].isin(value),
                        'cip'] = group_cip
                # replace cip_label dictionary with appropriate label
                # might want to edit this to incl. a list of included cip codes
                self.cip_dict[key] = group_cip

        # If you want to toggle between graphing the other category, save the
        # other index now
        if self.drop_other:
            other_idx = self.cip_dict['Other'][0]

        # reverse dictionary; make cip code not a list
        # (each value of cip_dict only has 1 element now)
        self.cip_dict = {value[0]: key for key, value in self.cip_dict.items()}
        # Include CIP code in label
        if self.cip_inlabel:
            self.cip_dict = {key: key + ': ' + value
                             for key, value in self.cip_dict.items()}

        # groupby new cip column and year
        # index = (['year', 'cip'], columns = ['ctotalm', ctotalw])
        cipdf = (df4[df4['cip2'].isin(cip_list_2d) | df4['cip4']
                 .isin(cip_list_4d)].groupby(['year', 'cip']).aggregate('sum'))

        # Need to sort from largest to smallest for area graph.
        # Set up that order here so colors match across graphs
        # Create a total variable
        cipdf['total'] = cipdf.sum(axis=1)
        cipdf = (cipdf.unstack(level=0)
                 .sort_values([('total', 2018)], ascending=False))
        # to preserve order you just found, unstack to series
        cipdf = cipdf.unstack()
        # further unstack outermost level
        cipdf = cipdf.unstack(0)
        # drop total column
        cipdf.drop('total', axis=1, inplace=True)

        # drop the specified 'other' category
        if self.drop_other:
            cipdf = cipdf.drop(index=other_idx, level=1)
            self.cip_dict.pop(other_idx)

        # return dataframe
        self.cipdf = cipdf

    def plot_rate(self, ax=None):
        ciprate_df = self.cipdf.copy()
        ciprate_df['ratio'] = ciprate_df['ctotalw'] / ciprate_df['ctotalm']
        ciprate_df = ciprate_df.drop(columns=['ctotalm', 'ctotalw'])
        # set index = year; columns = (None, cip)
        ciprate_df = ciprate_df.unstack()
        # set index = year; columns = cip
        ciprate_df.columns = ciprate_df.columns.droplevel(0)

        plot_df(ciprate_df, col_labels=self.cip_dict, ax=ax,
                x_lim=self.x_lim, title=self.rate_title,
                label_edit=self.label_edit)

    def plot_area(self, ax_w=None, ax_m=None):

        if ax_w is None and ax_m is None:
            fig, ax = plt.subplots(1, 2, sharey=self.shareyflag)
            ax_w = ax[0]
            ax_m = ax[1]

        # get bounds
        first_idx = min(self.cipdf.index.get_level_values(0).unique())
        last_idx = max(self.cipdf.index.get_level_values(0).unique())

        # Plot figures
        self.plot_area_axes(ax_w, 'ctotalw', first_idx, last_idx)
        self.plot_area_axes(ax_m, 'ctotalm', first_idx, last_idx)

        # Set figure titles (could use xlabel for title below)
        if self.areagraph and self.rategraph:
            ax_w.set_xlabel('Women')
            ax_m.set_xlabel('Men')
        else:
            ax_w.set_title('Women')
            ax_m.set_title('Men')
            ax_w.set_xlabel('')
            ax_m.set_xlabel('')

        # Set legends
        ax_w.legend().remove()
        if self.area_leg:
            ax_m.legend(loc=6, bbox_to_anchor=(1.04, 0.5))
        else:
            ax_m.legend().remove()

    def plot_area_axes(self, ax, col, min_x, last_idx):
        my_cmap = tol_colors.tol_cset('bright')

        (self.cipdf[col]
            # Convert to thousands
            .transform(lambda x: x / 1e3).unstack()
            # rename columns; necessary to get legend working in tikzplotlib
            .rename(self.cip_dict, axis='columns')
            # area plot
            .plot.area(ax=ax, color=my_cmap))

        # fix ticks
        xticks = ax.get_xticks().tolist()

        # remove ticks that are beyond the indexed area
        new_xticks = [tick for tick in xticks if
                      ((tick >= min_x) & (tick <= last_idx))]
        ax.set_xticks(new_xticks)

        ax.set_xticklabels([r'$' + '{0:n}'.format(tick)
                            + '$' for tick in new_xticks])

        # Create grid
        ax.grid(axis='y', color='#000000', linewidth=.5, linestyle=':')
        # Remove axes
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

    def plot_cip(self):
        if self.rategraph and not self.areagraph:
            fig, ax = plt.subplots()
            self.plot_rate(ax)
        if self.areagraph and not self.rategraph:
            fig, ax = plt.subplots(1, 2, sharey=self.shareyflag)
            self.plot_area(ax[0], ax[1])
        if self.rategraph and self.areagraph:
            self.plot_rate()
            self.plot_area()


def add_begin_content(filepath):
    # edit the file to include \begin{tikzpicture} at top
    with open(filepath, 'r+') as file_handle:
        content = file_handle.read()
        file_handle.seek(0, 0)
        line = "\\begin{tikzpicture}"
        file_handle.write(line.rstrip('\r\n') + '\n' + content)


def add_end_content(filepath, group_title=None, title_space="1cm"):
    '''
    Add end content, including:
       * a title for subplots, if a group plot
       * end the tikzpicture
       * add the caption
    '''
    with open(filepath, 'a+') as file_handle:
        content = file_handle.read()
        file_handle.seek(0, 0)
        if group_title is None:
            line = "\n\\end{tikzpicture}\n\\caption{Source: IPEDS}"
        else:
            line = "\\draw" \
                   + " ($(my plots c1r1.north)!0.5!(my plots c2r1.north)" \
                   + " + (0, " + title_space + ")$)" \
                   + " node {" + group_title + "};" \
                   + "\n\\end{tikzpicture}" \
                   + "\n\\caption{Source: IPEDS}"
        file_handle.write('\n' + line.rstrip('\r\n') + '\n' + content)


def save_rateplot(filename):
    tpl.clean_figure()
    filepath = imgpath + filename + '.tex'
    tpl.save(filepath, wrap=False, axis_height='207pt', axis_width='300pt')
    add_begin_content(filepath)
    add_end_content(filepath)


def save_areaplot(filename, title):
    tpl.clean_figure()
    filepath = imgpath + filename + '.tex'
    tpl.save(filepath, wrap=False,
             extra_axis_parameters={"height=180pt, width=150pt",
                                    "reverse legend",
                                    "legend style={"
                                    + "at={(2.02, 0.5)},"
                                    + "anchor=west,"
                                    + "}"},
             extra_groupstyle_parameters={"horizontal sep=0.8cm",
                                          "group name=my plots"},
             )
    add_begin_content(filepath)
    title_str = title + " - number Bachelor's degrees awarded (thousands)"
    add_end_content(filepath, title_str)


def save_comboplot(cip_cls, filename):
    filepath = imgpath + filename + '.tex'
    file_handle = codecs.open(filepath, 'w')

    # Rate graph
    cip_cls.plot_rate()
    # To do: figure out why computer science ('11') raises error here
    try:
        tpl.clean_figure()
    except ValueError:
        pass
    code = tpl.get_tikz_code(axis_height='140pt',
                             axis_width='300pt',
                             # axis_width='150pt',
                             # extra_axis_parameters={'x post scale=2',
                             #                        'y post scale=1'}
                             )
    file_handle.write(code)
    file_handle.write('\n\\vspace{0.1cm}\n\\begin{tikzpicture}')
    file_handle.close()

    # area graph
    cip_cls.plot_area()
    tpl.clean_figure()
    code = tpl.get_tikz_code(
        wrap=False,
        extra_axis_parameters={"height=90pt, width=160pt",
                               "reverse legend",
                               "legend style={"
                               + "at={(2.02, 0.5)},"
                               + "anchor=west,"
                               + "}"},
        extra_groupstyle_parameters={"horizontal sep=0.8cm",
                                     "group name=my plots"},
    )
    with open(filepath, 'a+') as file_handle:
        content = file_handle.read()
        file_handle.seek(0, 0)
        file_handle.write('\n' + code + '\n' + content)
    group_title = 'Number Bachelor\'s degrees awarded (thousands)'
    add_end_content(filepath, group_title, title_space="0.25cm")

    # if group_title is None:
    #         line = "\n\\end{tikzpicture}\n\\caption{Source: IPEDS}"
    #     else:
    #         line = "\\draw" \
    #                + " ($(my plots c1r1.north)!0.5!(my plots c2r1.north)" \
    #                + " + (0, 1cm)$) node {" + group_title + "};" \
    #                + "\n\\end{tikzpicture}" \
    #                + "\n\\caption{Source: IPEDS}"


if __name__ == '__main__':

    # Keep desired cip codes

    # # Social science degrees
    # cip_list = ['42', '45.10', '45.11', '45.02', '45.06',
    #             # '45.07',
    #             '45.09',
    #             '45.04',
    #             '45.01', '45.05', '45.14', '45.03', '45.12', '45.13', '45.99'
    #             ]
    # cip_dict_arg = {
    #     'Political science': ['45.10'],
    #     'Int\'l relations': ['45.09'],
    #     # 'Geography': ['45.07'],
    #     'Other': ['45.01', '45.05', '45.14', '45.03', '45.12', '45.13',
    #               '45.99']
    # }

    # social_science = PlotCIP(cip_list, cip_dict=cip_dict_arg, rategraph=True,
    #                          cip_inlabel=False, drop_other=True, x_lim=2030)

    # save_rateplot('social_science_rat')

    # plt.close('all')

    # social_science = PlotCIP(cip_list, cip_dict=cip_dict_arg,
    #                          areagraph=True, x_lim=2030, shareyflag=False)
    # save_areaplot('social_science_area', 'Social Science')

    # plt.close('all')

    # ss = PlotCIP(['42'], rategraph=True, areagraph=True, x_lim=2031)

    # Plot
    # save_comboplot(ss, 'test')



    # cip14dict = {'Other': ['14.01', '14.03', '14.04', '14.06', '14.11',
    #                        '14.12', '14.13', '14.14', '14.18', '14.20',
    #                        '14.21', '14.22', '14.23', '14.24', '14.25',
    #                        '14.27', '14.28', '14.32', '14.33', '14.34',
    #                        '14.36', '14.37', '14.38', '14.39', '14.40',
    #                        '14.41', '14.42', '14.43', '14.44', '14.45',
    #                        '14.99']}

    # PlotCIP(['14'], cip_dict = cip14dict, rategraph=True)

    # PlotCIP('14',cip_dict = cip14dict,shareyflag=False)

    # figure = plt.gcf()
    plt.show()
