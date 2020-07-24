# Male dominated fields in IPEDS
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

# Image path
imgpath = rootdir + '/img/'
# get figure heigth and width
from img.code.figsize import ArticleSize
size = ArticleSize()
import img.code.tikzplotlib_functions as tplf
add_begin_content = tplf.add_begin_content

# from other ipeds data folders
from ipeds import plot_by_cip
PlotCIP = plot_by_cip.PlotCIP
from ipeds import plot_by_n
plot_n_degrees = plot_by_n.plot_n_degrees

# add_begin_content: moved to tplf


def add_end_content(filepath, plot_title=None, group_title=None,
                    title_space="1cm", source=None):
    '''
    Add end content, including:
       * plot title (better to use \\caption to define title) than pgfplots
       * a title for subplots, if a group plot
       * end the tikzpicture
       * add the caption
    '''
    with open(filepath, 'a+') as file_handle:
        # Edit strings that will be included
        caption = 'Source: IPEDS'
        if source is not None:
            caption = caption + '; ' + source

        content = file_handle.read()
        file_handle.seek(0, 0)

        if group_title is None:
            line = '\n\\end{tikzpicture}'
        else:
            line = '\\draw' \
                   + ' ($(my plots c1r1.north)!0.5!(my plots c2r1.north)' \
                   + ' + (0, ' + title_space + ')$)' \
                   + ' node {' + group_title + '};' \
                   + '\n\\end{tikzpicture}'

        if plot_title is not None:
            line = line + '\n\\caption{' + plot_title + '. ' + caption + '.}'
        # line = line + '\n\\caption*{' + caption + '}'
        file_handle.write('\n' + line.rstrip('\r\n') + '\n' + content)


def save_rateplot(filename, source=None, plot_title=None,
                  width=size.w(1.25), height=size.h(1.25)):
    tpl.clean_figure()
    filepath = imgpath + filename + '.tex'
    tpl.save(filepath, wrap=False, axis_height=height,
             axis_width=width)
    add_begin_content(filepath)
    add_end_content(filepath, source=source, plot_title=plot_title)


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


if __name__ == '__main__':
    plt.close('all')

    # Test 1: n degrees
    plot_n_degrees()
    title_str = ('Number of Bachelor\'s Degrees awarded'
                 ' in US 4-year colleges')
    save_rateplot('n_degrees', source='NCES', plot_title=title_str)

    plt.show()
