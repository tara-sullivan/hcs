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

datapath = rootdir + '/ipeds/data/'
rawpath = datapath + '/raw/'
cippath = rootdir + '/ipeds/data/cip_edit/'

# Read in graduation data
df = pd.read_csv(rawpath + '2016/gr2016_rv_data_stata.csv')

# Drop imputed columns
df = df.loc[:, ~df.columns.str.startswith('X')]

# Keep only those seeking bachelor's degrees at 4-year universities
df = df[df['COHORT'] == 2]
df.drop(['COHORT', 'SECTION'], axis=1, inplace=True)

# Keep relevant identifier variables
df.drop(['CHRTSTAT', 'LINE'], axis=1, inplace=True)

# Set index according to unique identifiers
df.set_index(['UNITID', 'GRTYPE'], inplace=True)

# Considering men and women right now; race variables are also available
df.drop(df.columns.difference(
    ['GRTOTLT', 'GRTOTLM', 'GRTOTLW']), axis=1, inplace=True)

#############################
# Checks to understand data #
#############################

# From documentation, where:
# BE4y = bachelor's or equiv (4-yr institution)
# 6   BE4y
# 7   BE4y exclusions
# 8   BE4y adjusted cohort (revised cohort minus exclusions)
# 9   BE4y Completers within 150% of normal time total
# 10  BE4y Completers of programs of < 2 yrs (150% of normal time)
# 11  BE4y Completers of programs of 2 but <4 yrs (150% of normal time)
# 12  BE4y Completers of bachelor's or equiv degrees total(150% of normal time)
# 13  BE4y Completers of bachelor's or equiv degrees in 4 years or less
# 14  BE4y Completers of bachelor's or equiv degrees in 5 years
# 15  BE4y Completers of bachelor's or equiv degrees in 6 years
# 16  BE4y Transfer-out students
# 43  BE4y noncompleters still enrolled
# 44  BE4y, No longer enrolled

# Checks to understand this data
idx = pd.IndexSlice


def is_agg(a, b):
    # check that a is an aggregate of b
    pd.testing.assert_series_equal(
        df.loc[idx[:, a], 'GRTOTLT'].droplevel(1),
        df.loc[idx[:, b], 'GRTOTLT'].groupby('UNITID').sum()
    )


# check that the total (6) equals adjusted cohort (8) + exclusions (7)
is_agg(6, [7, 8])

# check that those who finish in (2, 3, 4, 5, 6) years
# equals those who finish in 150% of normal time (ghtotlt = 9)
is_agg(9, [10, 11, 13, 14, 15])

# relationship between total in 150% of normal time variables
is_agg(9, [10, 11, 12])
is_agg(12, [13, 14, 15])

# check that total students (6) equals those who complete in normal time (9) +
# those who transfer (16) + those who are still enrolled (43) + those who are
# not enrolled (44) and those who are excluded (7)
# is_agg(8, [9, 16, 43, 44])
# FAILS because of institutions 130624 and 164155
bool_idx = (
    df.loc[idx[:, [9, 16, 43, 44]], 'GRTOTLT'].groupby('UNITID').sum()
    .ne(df.loc[idx[:, 8], 'GRTOTLT'].droplevel(1))
)
bad_idx = df['GRTOTLT'].unstack()[bool_idx].index.to_list()
# But the difference is small for these two institutions
diff = \
    df.loc[idx[bad_idx, [9, 16, 43, 44]], 'GRTOTLT'].groupby('UNITID').sum() \
    - df.loc[idx[bad_idx, 8], 'GRTOTLT'].droplevel(1)
diff / df.loc[idx[bad_idx, 8], 'GRTOTLT'] < .01

########################
# 200% completion data #
########################
# OSU: 204796
# Read in graduation data
df200 = pd.read_csv(rawpath + '2018/gr200_18_data_stata.csv')
# Drop imputed columns
df200 = df200.loc[:, ~df200.columns.str.startswith('X')]
# set index
df200.set_index('UNITID', inplace=True)

# checks on this data to understand aggregates
# Total + exclusions in old data
pd.testing.assert_series_equal(
    df200['BAREVCT'], df200['BAAC150'] + df200['BAEXCLU'],
    check_names=False
)

# Total + additional exclusions
pd.testing.assert_series_equal(
    df200['BAAC150'], df200['BAAC200'] + df200['BAAEXCL'],
    check_names=False
)

# Complete degrees in 7/8 yrs + complete degrees within 6
pd.testing.assert_series_equal(
    df200['BANC200'], df200['BANC150'] + df200['BANC200A'],
    check_names=False
)


# compare the total adjusted number in cohort from 2016 with 2018
bool_idx = df['GRTOTLT'].loc[:, 8].ne(df200['BAAC150'])

df[bool_idx[df.index.get_level_values('UNITID')].values]

testdf = df['GRTOTLT'].unstack().join(
    df200.loc[:, df200.columns.str.startswith('B')], how='left')
testdf[[6, 'BAREVCT']].loc[(
    testdf[6] != testdf['BAREVCT']) & testdf['BAREVCT'].notna()]
testdf['BAREVCT'].fillna(testdf[6], inplace=True)
testdf['diff'] = np.abs((testdf[6] - testdf['BAREVCT']))

# rename items
df200_dict = {
    'BANC200A': 8,
}
join_df = df200[list(df200_dict.keys())].rename(columns=df200_dict)
join_df.columns.set_names('GRTYPE', inplace=True)
join_df = join_df.stack()
join_df.name = 'GRTOTLT'

##############
# stata data #
##############
# cwd = os.getcwd()
# os.chdir(rootdir)
# run_do = "do ipeds/data/ipeds_c_clean.do 2014"
# os.system("/usr/local/bin/stata-se " + run_do)
# df_c = pd.read_csv(datapath + 'ipeds_c_temp.csv')
# os.chdir(cwd)

###################################
# Approximate time to complettion #
###################################

# Drop unnecessary aggregates (see checks above)
df.drop(index=[6, 7, 9], level=1, inplace=True)
# Drop total cohort size (adjusted)
df.drop(index=8, level=1, inplace=True)
# Drop transfers
df.drop(index=16, level=1, inplace=True)
# Drop if did not complete a degree
df.drop(index=[43, 44], level=1, inplace=True)

time_dict = {
    10: 2,
    11: 3,
    13: 4,
    14: 5,
    15: 6,
}

# Rename types to reflect graduation
(df.loc[idx[:, list(time_dict.keys())], :]
    .rename(index=time_dict, level=1, inplace=True))


