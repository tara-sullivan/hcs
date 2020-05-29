import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
import tikzplotlib
import tol_colors

from scipy.stats import beta

imgpath = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())),
                       'img/')
color_list = list(tol_colors.tol_cset('bright'))

def beta_example_gender():
    '''
    Plot example beta distribution for males and females
    '''

    a_f, b_f = 3 * 1, 2 * 1
    a_m, b_m = a_f * 2, b_f * 2
    # a_f, b_f = 3*2, 1*2
    # a_m, b_m = a_f*3, b_f*3

    # Mean and sample size
    mu_m = beta.moment(1, a_m, b_m)
    mu_f = beta.moment(1, a_f, b_f)
    n_m, n_f = a_m + b_m, a_f + b_f

    x = np.linspace(0, 1, 1000)

    fig, ax = plt.subplots()

    # Function to create label
    def label_str(g, mu, n):
        label_str = g + ' \\\\ ' \
            + r'($\mu = $' + str(round(mu, 2)) + r', $n = $' + str(n) + ')'
        return label_str

    ax.plot(x, beta.pdf(x, a_m, b_m),
            label=label_str('Men', mu_m, n_m),
            color=color_list[0])

    ax.plot(x, beta.pdf(x, a_f, b_f),
            label=label_str('Women', mu_f, n_f),
            color=color_list[1])



    ax.legend(loc='upper left',
              handlelength=0.5,
              frameon=False,
              borderpad=0)

    # get teh current limit of y-axis
    _, y_max = ax.get_ylim()

    # Dotted line at mean
    ax.plot([mu_f, mu_f], [0, y_max], ':', color='#BBBBBB')

    # set y-limit
    ax.set_ylim(0, y_max)

    ax.set_title('PDF of Beta distribution')


def ab_str(a, b, t):
    ab_str = r'$\alpha_{' + str(t) + r'} = ' + str(a) + r'$, ' \
             + r'$\beta_{' + str(t) + r'} = ' + str(b) + r'$'
    return ab_str


def tikz_save(figname):
    tikzplotlib.clean_figure()
    # default tikz (width, height) = (240pt, 207pt) (manual 4.10.01)
    tikzplotlib.save(imgpath + figname + '.tex',
                     axis_height='120pt', axis_width='150pt')

def beta_example_main(ab0, history):

    x_range = np.linspace(0, 1, 50)

    a0, b0 = ab0
    y0 = beta.pdf(x_range, a0, b0)

    if len(history) >= 1:
        a1 = a0 + history[0]
        b1 = b0 + (1 - history[0])
        y1 = beta.pdf(x_range, a1, b1)
    if len(history) >= 2:
        a2 = a1 + history[1]
        b2 = b1 + (1 - history[1])
        y2 = beta.pdf(x_range, a2, b2)
    if len(history) >= 3:
        a3 = a2 + history[2]
        b3 = b2 + (1 - history[2])
        y3 = beta.pdf(x_range, a3, b3)

    # plot initial distribution
    fig, ax = plt.subplots()

    ax.plot(x_range, y0, linewidth=3)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2.25)

    ax.set_xticks((0, 0.5, 1))
    ax.set_yticks([0, 1, 2])

    title_str = r'Beliefs $p(\theta | \alpha, \beta)$'
    ax.set_title(title_str)

    tikz_save('beta_example0')
    plt.show()

    # plot t=1 distribution
    fig, ax = plt.subplots()

    ax.plot(x_range, y0, 'k', alpha=0.5)
    ax.plot(x_range, y1, linewidth=3)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2.25)

    ax.set_xticks((0, 0.5, 1))
    ax.set_yticks([0, 1, 2])

    # title_str = r'$p(\theta | \alpha, \beta)$'
    ax.set_title(title_str)

    tikz_save('beta_example1')
    plt.show()

    # plot t=2 distribution
    fig, ax = plt.subplots()

    ax.plot(x_range, y0, 'k', alpha=0.3)
    ax.plot(x_range, y1, 'k', alpha=0.5)
    ax.plot(x_range, y2, linewidth=3)


    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2.25)

    ax.set_xticks((0, 0.5, 1))
    ax.set_yticks([0, 1, 2])

    # title_str = r'$p(\theta | \alpha, \beta)$'
    ax.set_title(title_str)

    tikz_save('beta_example2')
    plt.show()

    # plot t=3 distribution
    fig, ax = plt.subplots()

    ax.plot(x_range, y0, 'k', alpha=0.1)
    ax.plot(x_range, y1, 'k', alpha=0.3)
    ax.plot(x_range, y2, 'k', alpha=0.5)
    ax.plot(x_range, y3, linewidth=3)


    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2.25)

    ax.set_xticks((0, 0.5, 1))
    ax.set_yticks([0, 1, 2])

    # title_str = r'$p(\theta | \alpha, \beta)$'
    ax.set_title(title_str)

    tikz_save('beta_example3')
    plt.show()  

if __name__ == '__main__':
    
    beta_example_gender()

    tikzplotlib.clean_figure()
    # default tikz (width, height) = (240pt, 207pt) (manual 4.10.01)
    tikzplotlib.save(imgpath + 'beta_example_gender' + '.tex',
                     axis_height='150pt', axis_width='250pt')
    # plt.show()

    beta_example_main((1, 1), [1, 0, 1])

    # beta_example_main((3, 3), [1, 0, 1])

    # beta_example_main((1, 1), [0, 1, 1])


    # beta_example((1, 1), True)
    # beta_example((1, 1), True, True)

    # plt.show()

    # param_list = [(1, 1), (2, 1), (1, 2), (2, 2), (3, 1), (2, 2), (1, 3)]
    # for a, b in param_list:
    #     beta_example(a, b)
    #     figname = 'beta_example_' + str(a) + '_' + str(b)
    #     print(figname)
    #     tikzplotlib.clean_figure()
    #     # default tikz (width, height) = (240pt, 207pt) (manual 4.10.01)
    #     tikzplotlib.save(imgpath + figname + '.tex', strict=True,
    #                      axis_height='70pt', axis_width='90pt', textsize=8.0)

    #     plt.show()