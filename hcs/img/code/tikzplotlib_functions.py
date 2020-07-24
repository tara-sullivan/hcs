'''
Sometimes I have to manually write tizkplotlib code.

For instance, sometimes I want to add nodes to tikzplotlib code.
These need to be written before the \\end{tikzplicutre} command.
Therefore, I select the option wrap=off in tikzplotlib,
save the initial version of the graph, and then manually add content
to the beginning and the end of the file.

Note the first place I employed this method was in save_ipeds_plots.py.
I have not incorporated these updated functions into that code.
'''
import numpy as np
import tikzplotlib as tpl
import matplotlib.pyplot as plt

from img.code.figsize import ArticleSize
size = ArticleSize()


def add_begin_content(filepath, extra_tikzpicture_parameters=None):
    # Write \begin{tikzpicture} at top of already created file
    with open(filepath, 'r+') as file_handle:
        content = file_handle.read()
        file_handle.seek(0, 0)
        line = '\\begin{tikzpicture}'
        if extra_tikzpicture_parameters is not None:
            line = line + '[' + ',\n'.join(extra_tikzpicture_parameters) + ']'
        file_handle.write(line.rstrip('\r\n') + '\n' + content)


def subplot_title(ax_loc, ref_name, subtitle_id,
                  plt_title, group_name='my plots',
                  text_width=size.w(.9),
                  col=True):
    '''
    To create subplot titles that can be referenced, you want to use the
    '\\subcaption' package within a node.

        * ax_loc: location of axes in subplot (i.e. [0, 0])
        * subtitle_id: how you will reference the subplot (i.e. 'a' for sim_a)
        * ref_name: main name for referencing figures from plot (i.e. sim)
        * plt_title: title of the plot to come after label
          i.e. plt_title='baseline' > title is '(a) baseline'
        * group_name: name of group; default is 'my plots'
        * text_width: width of subplot (default shorter to avoid overfill)
        * col: column orientation instead of row orientation

    To use:
        1) initialize string for subplot titles:
           >>> subplot_titles = ''
        2) After each plot, use subplot_title command
           >>> subplot_titles += tplf.subplot_title(
           ...     ax_loc=ax_loc, ref_name=ref_name,
           ...     subtitle_id=subtitle_id, plt_title=plt_title)
        3) In the save_subplots function, include the subplot_titles string as
           the node_code

    '''
    # find column and row of pgfplot from ax_loc. Some notes:
    #    * pgfplots names subplots according to c<column>r<row>
    #    * need to re-index: python starts at 0, while pgfplots start at 1
    if type(ax_loc) is int:
        if not col:
            row, col = 1, ax_loc + 1
        else:
            col, row = 1, ax_loc + 1
    elif type(ax_loc) is list:
        if len(ax_loc) == 1:
            if not col:
                row, col = 1, ax_loc[0] + 1
            else:
                col, row = 1, ax_loc[0] + 1
        else:
            row, col = np.array(ax_loc) + 1
    # write node code
    node_code = (
        '\\node [text width={w}, align=center, anchor=south] at '
        .format(w=text_width)
        + '({plt_name} c{col}r{row}.north)'
        .format(plt_name=group_name, col=col, row=row)
        + ' {{\\subcaption{{\\label{{{name}_{id}}} {title}}}}};'
        .format(name=ref_name, id=subtitle_id, title=plt_title)
    )
    return '\n' + node_code


def add_end_content(filepath, node_code=None, caption=None,):
    '''
    Add end content, when saving tikzplotlib figures

        * filepath: full filepath to tex code (including imgpath and .tex)
        * node_code: nodes to add before \\end{tikzpicture}
            - if you write subtitles as nodes, you can reference them using the
              subcaption package.
        * caption: line to include in \\caption{}, after \\end{tikzpicture}

    '''
    # open the file path for updating, appending to the end if it exists.
    with open(filepath, 'a+') as file_handle:
        # content = file_handle.read()
        file_handle.seek(0, 0)

        if node_code is not None:
            # write content, strip trailing newlines
            # note: used to add + '\n' + content) after this
            file_handle.write('\n\n' + node_code.strip('\r\n'))
        file_handle.write('\n\n\\end{tikzpicture}')
        if caption is not None:
            file_handle.write('\n\n\\caption{' + caption + '}' + '\n')


def save_subplots_code(filepath, figure='gcf',
                       height=size.h(), width=size.w(),
                       xlabel_loc=None,
                       extra_groupstyle_parameters=None):
    '''
    Make tizplotlib plots with subplots

        * filepath: name if file, incl. path and '.tex'
        * height, width: size of each individual plot
        * xlabel_loc: re-size font of x label and move it
            - currently only set up for xlabel_loc='right'
        * extra_groupstyle_parameters: parameters to pass onto tpl.save()

    '''
    # extra_axis_parameters: things to be included in \\nextgroupplot[]
    # initialize extra axis parameters
    if xlabel_loc is None:
        extra_axis_parameters = None
    # Add items if necessary
    else:
        extra_axis_parameters = set()
        # label the x-axis on the right hand side
        if xlabel_loc == 'right':
            extra_axis_parameters.add(
                'xlabel style={at={(ticklabel* cs:1.00)},'
                + ' anchor=north east, font=\\normalsize}'
            )

    tpl.save(
        figure=figure, filepath=filepath, wrap=False,
        axis_height=height, axis_width=width,
        # group style parameters included in \\begin{groupplot}[group style={}]
        extra_groupstyle_parameters=extra_groupstyle_parameters,
        # will be included in \\nextgroupplot[]
        extra_axis_parameters=extra_axis_parameters,
    )


def save_subplots(filepath,
                  figure='gcf',
                  node_code=None, caption=None,
                  height=size.h(), width=size.w(),
                  xlabel_loc=None,
                  extra_tikzpicture_parameters=None,
                  extra_groupstyle_parameters=None,
                  clean_figure=False):
    '''
    Tikzplotlib code to save figures.

        * filepath: full filepath to tex code (including imgpath and .tex)
        * figure: figure to plot
        * node_code: nodes to add before '\\end{tikzpicture}'
        * caption: line to include in '\\caption{}', after '\\end{tikzpicture}'
        * height, width: width and height of each subplot
        * xlabel_loc: location of the x-label.
        * extra_tikzpicture_parameters: parameter from tikzplotlib
        * extra_groupstyle_parameters: parameter from tizkplotlib
        * clean_picture: run tikzplotlib.clean_figure() command

    Options:

    node_code: code to add before '\\end{tikzpicture}'. It is often convenient
    to write plot subtitles as drawn tikz nodes, instead of using the
    matplotlib plt.title() command. Nodes drawn on the tikz graphs can use the
    '\\subcaption' package in tex. Then you can reference subplots using the
    '\\ref' command in tex. To do this, save the code to write a subtitle as a
    '\\node' as a string. This can be done using the subplot_title() function
    in this program. Then include the string of node commmands as a node_code
    when saving.

    caption: cation to include in the '\\caption{}' command, after
    '\\endtikzpicture{}'

    xlabel_loc: location of the x-label.
        * None [default]
        * 'right': move x-label to the right of the x-axis. currently also
           increases the size of the label.

    extra_tikzpicture_parameters: parameter from tikzplotlib.
        * defaults to 'every node/.style={font=\\small}'; makes font small

    clean_figure: run tikzplotlib.clean_figure() command. This command has
    been breaking when I plot subplots, specifically with dataframes with
    missing data at the end (i.e. one ends with np.nan). For examples of
    this problem, see the subplots of the model simulation in model_plots.py

    '''
    if figure == 'gcf':
        figure = plt.gcf()
    if clean_figure:
        tpl.clean_figure(figure)

    # add a name to the plot
    if extra_groupstyle_parameters is None:
        extra_groupstyle_parameters = {
            # space between plots
            'horizontal sep=1.2cm', 'vertical sep=2cm',
            'group name=my plots',
        }
    else:
        extra_groupstyle_parameters.add('group name=my plots')
    # Create the file with figure code; save most of it
    save_subplots_code(
        filepath=filepath, figure=figure,
        xlabel_loc=xlabel_loc,
        height=height, width=width,
        extra_groupstyle_parameters=extra_groupstyle_parameters,
    )
    # add \\begin{tikzpicure} and appropriate parameters
    if extra_tikzpicture_parameters is None:
        # Set default font to small
        extra_tikzpicture_parameters = {'every node/.style={font=\\small}'}
    add_begin_content(
        filepath,
        extra_tikzpicture_parameters=extra_tikzpicture_parameters,
    )
    # add nodes at the end of graph, \\end{tikzpicture}, and \\caption{}
    add_end_content(
        filepath,
        node_code=node_code, caption=caption
    )
