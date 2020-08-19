import matplotlib.pyplot as plt

import os
import sys
import inspect

# import pdb
# from importlib import reload

try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
# rootdir: /hcs/hcs
rootdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    currpath))))
sys.path.append(rootdir)

# Image path
imgpath = rootdir + '/img/'

from data.ipeds.c.clean_data.make_df import cip4labels_df
# get figure heigth and width
from img.code import tikzplotlib_functions as tplf
from img.code.figsize import ArticleSize
size = ArticleSize()

from data.ipeds.c import plot_by_n
plot_n_degrees = plot_by_n.plot_n_degrees

from data.ipeds.c import plot_by_cip
PlotCIP = plot_by_cip.PlotCIP
from data.ipeds.c import save_ipeds_plots
save_rateplot = save_ipeds_plots.save_rateplot
save_areaplot = save_ipeds_plots.save_areaplot
save_comboplot = save_ipeds_plots.save_comboplot

plt.close('all')

##############################################################################
# 1. Number degrees completed by men and women

plot_n_degrees()
title_str = ('Number of Bachelor\'s Degrees awarded'
             ' in US 4-year colleges')
save_rateplot('n_degrees', source='Snyder (2013)', plot_title=title_str)

##############################################################################
# 2. Ration men to women in historically male dominated fields

male_dom_cip = ['14', '11', '40', '45', '27', '52', '26', '42']

# Initialize first sub-plot
plt.close('all')
fig, ax = plt.subplots(1, 2)
ref_name = 'fig:ipeds'
subplot_titles = ''
group_caption = ''
# Subplot specific data
ax_loc = 0
subtitle_id = 'a'

cip_dict = {
    'Social Sciences': ['45', '42'],
    'All Fields': ['98']
}

label_edit = {'11': -.07, '14': .02, '40': -.08}

# Create standalong version of graph
cip_cls = PlotCIP(male_dom_cip, rategraph=True, x_lim=2030,
                  label_edit=label_edit, cip_dict=cip_dict, rate_total=True)
save_rateplot('male_dom')

# Create version for sub-plot version
# edit cip dictionary
cip_cls.cip_dict['42'] = 'Social \\\\ Sciences'
cip_cls.cip_dict['11'] = 'Computer \\\\ Services'
cip_cls.cip_dict['26'] = 'Biological \\\\ Sciences'
cip_cls.cip_dict['27'] = 'Math'
cip_cls.cip_dict['40'] = 'Physical \\\\ Sciences'

# cip_dict = {'Computer \\\\ Services': ['11'],
#             'Biological \\\\ Sciences': ['26'],
#             'Math': ['27'],
#             'Physical \\\\ Sciences': ['40'],
#             'Social \\\\ Sciences': ['45', '42'],
#             'All Fields': ['98']
#             }

cip_cls.label_edit = {
    '14': 0, '11': -.22,
    '40': -.23, '27': 0, '52': -.05,
    '26': -.2, '42': -.05, '98': -.05}

# plot sub-pot graph
cip_cls.plot_rate(ax=ax[ax_loc], xticks=[1990, 1995, 2000, 2005, 2010, 2015])

# edit variable for save_subplots
plt_title = ax[ax_loc].get_title()
# remove y-axis label
ax[ax_loc].set_title('')
subplot_titles += tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, col=False,
    subtitle_id=subtitle_id, plt_title=plt_title
)
group_caption += 'Ratio of women to men completing Bachelor\'s degrees' \
    + ' in U.S. 4-year colleges. Source: IPEDS.'


##############################################################################
# 3. Social sciences - rate and area graphs

# Subplot variables
ax_loc = 1
subtitle_id = 'b'

# Social science degrees
cip_list = ['42', '45.10', '45.11', '45.02', '45.06',
            # '45.07',
            '45.09',
            # '45.04',
            '45.01', '45.05', '45.14', '45.03', '45.12', '45.13', '45.99'
            ]
cip_dict_arg = {
    'Political science': ['45.10'],
    'Int\'l relations': ['45.09'],
    # 'Geography': ['45.07'],
    'Other': ['45.01', '45.04', '45.05', '45.05', '45.14', '45.03',
              '45.12', '45.13', '45.99']
}

# cip_list = ['42', '45.10', '45.11', '45.02', '45.06',
#             '45.09',
#             '45.01', '45.05', '45.14', '45.03', '45.12', '45.13', '45.99'
#             ]
# cip_dict_arg = {
#     'Political \\\\ science': ['45.10'],
#     'Int\'l relations': ['45.09'],
#     # 'Geography': ['45.07'],
#     'Other': ['45.01', '45.04', '45.05', '45.05', '45.14', '45.03',
#               '45.12', '45.13', '45.99']
# }

# Rate graph
cip_cls = PlotCIP(cip_list, cip_dict=cip_dict_arg,
                  cip_inlabel=False, drop_other=True, x_lim=2030)
cip_cls.plot_rate()
save_rateplot('social_science_rat')

# save version of subplot
cip_cls.cip_dict['45.10'] = 'Political \\\\ science'
cip_cls.label_edit = {
    '45.11': -.1, '45.09': -.1, '45.10': -.15, '45.06': -.2
}

# plot sub-pot graph
cip_cls = PlotCIP(cip_list, cip_dict=cip_dict_arg,
                  cip_inlabel=False, drop_other=False, x_lim=2030)
cip_cls.plot_rate(ax=ax[ax_loc], xticks=[1990, 1995, 2000, 2005, 2010, 2015])
# edit variable for save_subplots
plt_title = ax[ax_loc].get_title() + ' - Social Sciences'
# remove y-axis label
ax[ax_loc].set_title('')
subplot_titles += tplf.subplot_title(
    ax_loc=ax_loc, ref_name=ref_name, col=False,
    subtitle_id=subtitle_id, plt_title=plt_title
)

tplf.save_subplots(imgpath + 'intro_ipeds.tex', figure=fig,
                   node_code=subplot_titles, caption=group_caption,
                   height=size.h(1.25), width=size.w(1.1),
                   extra_tikzpicture_parameters={
                       'every node/.style={font=\\footnotesize}',
                       'align=left'
                   })

# Area graph
PlotCIP(cip_list, cip_dict=cip_dict_arg, areagraph=True, shareyflag=False)
save_areaplot('social_science_area', 'Social Science')

# Add plot to subplot

##############################################################################
# Social Sciences cip
plt.close('all')

cip_list = ['45.01', '45.02', '45.03', '45.04', '45.05', '45.06', '45.07',
            '45.09', '45.10', '45.11', '45.12', '45.13', '45.14', '45.99']
cip42dict = {
    'Political science': ['45.10'],
    'Int\'l relations': ['45.09'],
    'Geography': ['45.07'],
    'Other': ['45.01', '45.05', '45.14', '45.03', '45.12', '45.13', '45.99']
}

label_edit = {'45.06': -.04}
ss = PlotCIP(cip_list, cip_dict=cip42dict,
             rategraph=True, areagraph=True, x_lim=2031)

save_comboplot(ss, 'cip45')

##############################################################################
# Engineering

cip_list = list(cip4labels_df.loc['14'].index)

cip_dict = {'Biomedical': ['14.05'],
            'Chemical': ['14.07'],
            'Industrial': ['14.35'],
            'Civil': ['14.08'],
            'Mechanical': ['14.19'],
            'Electrical': ['14.10'],
            'Computer': ['14.09'],
            'Other': ['14.01', '14.02', '14.03', '14.04', '14.06', '14.11',
                      '14.12', '14.13', '14.14', '14.18', '14.20',
                      '14.21', '14.22', '14.23', '14.24', '14.25',
                      '14.27', '14.28', '14.32', '14.33', '14.34',
                      '14.36', '14.37', '14.38', '14.39', '14.40',
                      '14.41', '14.42', '14.43', '14.44', '14.45',
                      '14.99']}

label_edit = {'14.07': .05, '14.35': .02,
              '14.19': .04, '14.09': -.12, '14.10': -.04,
              '14.99': -.04, '14.08': .04}

cip_cls = PlotCIP(cip_list=cip_list, cip_dict=cip_dict,
                  rategraph=True, areagraph=True,
                  label_edit=label_edit,
                  x_lim=2031, shareyflag=False)
save_comboplot(cip_cls, 'cip14')

##############################################################################
# Business and related services

cip_list = list(cip4labels_df.loc['52'].index)

cip_dict = {'General': ['52.01'],
            'Business admin.': ['52.02'],
            'Accounting': ['52.03'],
            'Finance': ['52.08'],
            'Hospitality': ['52.09'],
            'Human Resources': ['52.10'],
            'Management services': ['52.12'],
            'Other': ['52.04', '52.05', '52.06', '52.07', '52.11',
                      '52.12', '52.13', '52.15', '52.16', '52.17',
                      '52.18', '52.19', '52.20', '52.21', '52.99']}

label_edit = {'52.01': .03, '52.02': -.12, '52.03': .05,
              '52.08': -.15, '52.11': .06,
              '52.14': .15, '52.99': -.19}

cip_cls = PlotCIP(cip_list=cip_list, cip_dict=cip_dict,
                  rategraph=True, areagraph=True,
                  label_edit=label_edit,
                  x_lim=2031)

save_comboplot(cip_cls, 'cip52')

##############################################################################
# CS
plt.close('all')

cip_list = list(cip4labels_df.loc['11'].index)

cip_dict = {'General': ['11.01'],
            'Information science': ['11.04'],
            'Media applications': ['11.08'],
            'Systems network': ['11.09'],
            'IT': ['11.10'],
            'Other': ['11.02', '11.05', '11.99', '11.03', '11.06']}

label_edit = {'11.01': .06, '11.04': .08,
              '11.09': -.14, '11.10': -.1,
              '11.99': -.05,
              }

cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  x_lim=2031, shareyflag=False,
                  )

save_comboplot(cip_cls, 'cip11')

##############################################################################
# Education

cip_list = list(cip4labels_df.loc['13'].index)

cip_dict = {'Other': ['13.02', '13.03', '13.04', '13.05',
                      '13.06', '13.07', '13.09', '13.11',
                      '13.14', '13.15', '13.99'],
            'Specific subject area': ['13.13'],
            'Specific levels': ['13.12'],
            'Special Ed': ['13.10'],
            'General': ['13.01']}

label_edit = {'13.12': -1, '13.99': -.05
              # '11.09': -.14, '11.10': -.1,
              # '11.99': -.05,
              }

cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  x_lim=2031, shareyflag=False,
                  )

save_comboplot(cip_cls, 'cip13')

##############################################################################
# Biological and Physical Sciences and math
plt.close('all')

cip_list = ['26', '27'] + list(cip4labels_df.loc['40'].index)

cip_dict = {'Biology': ['26'], 'Math': ['27'],
            'Geosciences': ['40.06'],
            'Other': ['40.01', '40.02', '40.04', '40.99']}

label_edit = {'40.99': -.1, '27': .1}

cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  x_lim=2031, shareyflag=False,
                  )

save_comboplot(cip_cls, 'science_math')

##############################################################################
# Physical Sciences and math

cip_list = ['27'] + list(cip4labels_df.loc['40'].index)

cip_dict = {'Biology': ['26'], 'Math': ['27'],
            'Geosciences': ['40.06'],
            'Other': ['40.01', '40.02', '40.04', '40.99']}

label_edit = {'40.99': -.1, '27': .05, '40.06': -.03}

cip_cls = PlotCIP(cip_list=cip_list,
                  cip_dict=cip_dict, label_edit=label_edit,
                  rategraph=True, areagraph=True,
                  x_lim=2031, shareyflag=False,
                  )

save_comboplot(cip_cls, 'physical_science_math')


##############################################################################
plt.close('all')
print('done: ipeds_plots.py')
