'''
access figure width and height
'''

import math

# Determine figure size from latex

# Default beamer size:
# paperwidth: 12.80cm
# paperheight: 9.60cm

# article size:
# textwidth: 16.50746cm
# textheigh: 22.85675 cm

# default tikz: (manual 4.10.01)
# axis_width = 240pt
# axis_height = 207pt

# Set up sizes
textwidth = 16.50746
fig_width = textwidth / 2
golden_mean = (math.sqrt(5) - 1.0) / 2.0
fig_height = fig_width * golden_mean


class ArticleSize:
    def __init__(self):
        pass

    def w(self, scale=None, fig_width=fig_width, float=False):
        # print(fig_width)
        if scale is None or scale == 0:
            fw = fig_width
        else:
            fw = fig_width * scale

        if float:
            doc_w = fw
        else:
            doc_w = str(fw) + 'cm'

        return doc_w

    def h(self, scale=None, fig_height=fig_height, float=False):
        if scale is None or scale == 0:
            fh = fig_height
        else:
            fh = fig_height * scale

        if float:
            doc_h = fh
        else:
            doc_h = str(fh) + 'cm'

        return doc_h


if __name__ == '__main__':

    size = ArticleSize()

    print(size.w())
    print(size.w(0, float=True))
    print(size.w(2))

    print(size.h())
    print(size.h(0, float=True))
    print(size.h(2))
