import matplotlib.pyplot as plt
# import tikzplotlib as tpl

import os
import sys
import inspect

# import pdb
from importlib import reload

try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
rootdir = os.path.dirname(os.path.dirname(currpath))
sys.path.append(rootdir)

from ipeds.make_df import cip4labels_df

from ipeds import plot_by_n
from ipeds import plot_by_cip

plot_n_degrees = plot_by_n.plot_n_degrees
PlotCIP = plot_by_cip.PlotCIP
save_rateplot = plot_by_cip.save_rateplot
save_areaplot = plot_by_cip.save_areaplot
save_comboplot = plot_by_cip.save_comboplot

plt.close('all')

##############################################################################
# 1. Number degrees completed by men and women

plot_n_degrees()
save_rateplot('n_degrees')

##############################################################################
# 2. Ration men to women in historically male dominated fields

male_dom_cip = ['14', '11', '40', '45', '27', '52', '26']

label_edit = {'11': -.04, '40': -.04}

PlotCIP(male_dom_cip, rategraph=True, x_lim=2030, label_edit=label_edit)
save_rateplot('male_dom')

##############################################################################
# 3. Social sciences - rate and area graphs

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

# Rate graph
PlotCIP(cip_list, cip_dict=cip_dict_arg, rategraph=True,
        cip_inlabel=False, drop_other=True, x_lim=2030)
save_rateplot('social_science_rat')

# Area graph
PlotCIP(cip_list, cip_dict=cip_dict_arg, areagraph=True, shareyflag=False)
save_areaplot('social_science_area', 'Social Science')

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
print('done')
