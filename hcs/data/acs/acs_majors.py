import pandas as pd
import numpy as np

import os
import sys
import inspect

try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
rootdir = os.path.dirname(os.path.dirname(os.path.dirname(currpath)))
sys.path.append(rootdir)

rawpath = '/Volumes/GoogleDrive/My Drive/data/ACS/'
datapath = rootdir + '/data/acs/'
tablepath = rootdir + '/img/'

from data.ipeds.c.clean_data.make_df import cip4labels_df
from data.ipeds.c.clean_data.make_df import cip2labels_short, cip2labels


df = pd.read_hdf(datapath + 'acs.h5', 'df')


codebook = rawpath + 'codebook.txt'


def make_dict(var_name, codebook=codebook):
    # Read in codebook
    with open(codebook, 'r') as file:
        lines = list(file)

        # Find the table that contains the variable name
        # Note that the first time a variable appears, it is in the summary.
        # However, this value starts with a space (i.e. " DEGFIELD")
        # So searching for lines that start with the variable is sufficient.
        newlist = []
        intable = False
        for line in lines:
            if intable is True and line == '\n':
                intable = False
            if intable is True:
                item = line.split(maxsplit=1)
                item[0] = int(item[0])
                item[1] = item[1].strip()
                newlist.append(item)
            if line.startswith(var_name):
                if line.split()[0] == var_name:
                    intable = True
    return dict(newlist)


# create labels of varibles
acs2labels = make_dict('DEGFIELD')
acs4labels = make_dict('DEGFIELDD')


# create dictionaries for acs-provided degree descriptions
def make_dict(dict_file):
    dict_name = {}
    with open(dict_file, 'r') as file:
        _ = next(file)
        _ = next(file)
        for line in file:
            split_line = line.split(maxsplit=1)
            dict_name[int(split_line[0])] = ','.join(split_line[1:]).rstrip()
    return dict_name


# basic degree descriptions
acs2labels = make_dict(datapath + 'degfield.txt')

# detailed degree descriptions
acs4labels = make_dict(datapath + 'degfieldd.txt')

# find the difference between degrees in data and degrees not in data
s1 = set(list(acs4labels.keys()))
s2 = set(np.unique(df['DEGFIELDD']))
diff_ddeg = list((s1 - s2).union(s2 - s1))

# check that the codes from dict are in the data
# print('Codes in dictionary not in data:')
# print({key: acs4labels[key] for key in diff_ddeg})
# 3200: 'Law': has sub-fields 3201, 3202
# 4003: 'Neuroscience': duplicate; also 3611
# 3300: 'English,Language,,Literature,,and,Composition': 3301 and 3302
# 2600: 'Linguistics,and,Foreign,Languages': composed of 2601, 2602, and 2603
# 5801: 'Precision,Production,and,Industrial,Arts': no clue
# 3400: 'Liberal,Arts,and,Humanities': composed of 3401 and 3402
# 4008: 'Multi-disciplinary,or,General,Science': not sure
# 1900: 'Communications': 1901, 1902, 1903, 1904 (or just dup of 1901)
# 1300: 'Environment,and,Natural,Resources': 1301, 1302, 1303
# 5400: 'Public,Affairs,,Policy,,and,Social,Work': 5401, 5402, 5403, 5404

deg_table = df.groupby(['DEGFIELD', 'DEGFIELDD']).size()
deg_table.rename(index=acs2labels, inplace=True)
deg_table.rename(index=acs4labels, inplace=True)
deg_table.rename('Frequency', inplace=True)

deg_table.index.set_names(['Broad classification', 'Detailed classification'],
                          inplace=True)


# possible edits before exporting to tex
deg_table = deg_table.reset_index().drop(columns='Frequency')
# export to tex
deg_table.to_latex(
    tablepath + 'degree_labels.tex',
    index=False, longtable=True,
    caption='ACS degree fields')

# with open(tablepath + 'degree_labels.tex', 'x') as file:
#     file.write(deg_table.to_latex())

# combined classification
# ['01', '03', '04', '05', '09', '10', '11', '12', '13', '14', '15',
# '16', '19', '22', '23', '24', '25', '26', '27', '28', '29', '30',
# '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41',
# '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52',
# '53', '54', '60']

#fid: field ID
# pd.DataFrame()

idx = pd.IndexSlice
# cip4labels_df.loc['01', 'did'] = 11

# fid_df = pd.DataFrame(columns=['cipcode', 'ciplabel', 'acscode', 'acslabel'],

                      # index=['fid'])

# fid = 11
# cip = '01'
# acs = 11
# idlist =[]

# idlist.append([11, '01', 11])
# idlist.append(13)


# fid[11]
