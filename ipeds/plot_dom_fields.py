# Male dominated fields in IPEDS
import os
import matplotlib.pyplot as plt
import tikzplotlib

from make_df import df2, cip2labels, cip2labels_short
import plot_line_labels
plot_df = plot_line_labels.plot_df

imgpath = os.path.join(os.path.dirname(os.getcwd()), 'img/')


def find_dom():
    '''Find male-dominated fields'''

    # # Aggregate up to year and cip; keep only year 1990
    cip1990 = df2.groupby(['year', 'cip2']).aggregate('sum').loc[1990]

    # Create ratio variable
    cip1990['rat'] = cip1990['ctotalw'] / cip1990['ctotalm']
    # Sort by ratio
    cip1990.sort_values(by='rat', ascending=False, inplace=True)

    # Map labels to cip index; look at this to find appropriate cip
    cip1990['cip2label'] = cip1990.index.to_series().map(cip2labels)

    '''Nicely print dictionaries'''
    print(cip1990[['rat', 'cip2label']])


def main():

    # List of male (and female) dominated fields
    male_dom = ['14', '11', '40', '45', '27', '52']
    # female_dom = ['51', '50', '42', '16', '13']

    # top 12 cip codes, aggregated
    cip2df = (df2[df2['cip2'].isin(male_dom)]
              .groupby(['year', 'cip2']).aggregate('sum').unstack())

    # switch order of columns
    cip2df.columns = cip2df.columns.swaplevel(0, 1)
    cip2df.sort_index(axis=1, level=0, inplace=True)

    # reshape dataframe
    # make index [year, cip2], columns [ctotalm, ctotalf]
    cip2rate = cip2df.swaplevel(axis=1).stack()
    # create rate variable
    cip2rate['rate'] = cip2rate['ctotalw'] / cip2rate['ctotalm']
    # only keep rate variable and unstack; index=year, column=cip2
    cip2rate = cip2rate['rate'].unstack()

    # cols = male_dom
    col_labels = {key: cip2labels_short[key] for key in male_dom}
    title_str = 'Ratio of women to men'
    label_edit = {'11': -.02, '40': -.02}

    plot_df(df=cip2rate, cols=male_dom, col_labels=col_labels,
            title=title_str, label_edit=label_edit, x_lim=2030)


if __name__ == '__main__':
    # If necessary, list ratio in 1990
    # find_dom()
    # define dataframe
    main()
    tikzplotlib.clean_figure()
    # default tikz (width, height) = (240pt, 207pt) (manual 4.10.01)
    tikzplotlib.save(imgpath + 'male_dom.tex',
                     axis_height='207pt', axis_width='300pt')

    plt.show()


# Maybe create a sciences graph?

# Biological sciences (26):
# Instructional programs that focus on the biological sciences and the
# non-clinical biomedical sciences, and that prepare individuals for
# research and professional careers as biologists and biomedical scientists

# Physical sciences (40):
# Instructional programs that focus on the scientific study of inanimate
# objects, processes of matter and energy, and associated phenomena
