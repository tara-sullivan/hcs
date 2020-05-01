# Create ipeds dataframe
# input: ipeds_c_all.dta
# output: df: dataframe of time series
#         df2: 2-digit cip code dataframe
#         df4: 4-digit cip code dataframe

import pandas as pd
# Nice timing feature
from quantecon.util import timing

# file paths
from sys import platform
import os

if __name__ == '__main__':
    # Ensure we're on the right home file
    my_os = platform
    if my_os == 'darwin':
        home = ('/Users/tarasullivan/Google Drive File Stream/'
                'My Drive/research/hcs/')
    elif my_os == 'win32':
        home = 'Z:/hcs/'
    os.chdir(home)

basepath = os.getcwd()
datapath = basepath + '/data/ipeds/'

# read in raw data
print('reading...')
timing.tic()
df = pd.read_stata(datapath + 'ipeds_c_all.dta')
timing.toc()

# remove rows with missing cipcode in 2010
df = df[df['cipcode2010'] != '']

# keep only bachelor's degrees
df = df[df['awlevel'] == 5]

# drop aggregate values
df = df[(df['cipcode'] != '99') & (df['cipcode'] != '99.') &
        (df['cipcode'] != '99.0000') & (df['cipcode'] != '95.0000') &
        (df['cipcode'] != '95.9500')]

# make year an integer
df['year'] = df['year'].astype(int)

# check if there are duplicated values according to original cip code
# note that these may be aggregated
assert not df.duplicated(
    subset=['year', 'unitid', 'cipcode', 'majornum']).any()

# check if there are any cases where there are no reported students
assert 0 == df[(df['ctotalm'].isna()) & (df['ctotalw'].isna())].sum().sum()

# replace missing values with zeros
# df['ctotalm'].fillna(0, inplace=True)
# df['ctotalw'].fillna(0, inplace=True)

# aggregate over cipcode2010, majornum; reset index
df = df.groupby(['year', 'unitid', 'cipcode2010']).aggregate('sum')

# remove columns
df = df.drop(['awlevel', 'majornum'], axis=1)

# reset index
df = df.reset_index()
df.head()

# Create 2-digit and 4-digit CIP codes

# Create 2-digit CIP code column
df2 = df
# Create 2-digit CIP code
df2['cip2'] = df2['cipcode2010'].str[:2]
# aggregate to two digit level
df2 = df2.groupby(['year', 'unitid', 'cip2']).aggregate('sum')
# reset index
df2 = df2.reset_index()

# Create 4-digit CIP code column
df4 = df
# Create 4-digit CIP code
df4['cip4'] = df4['cipcode2010'].str[:5]
# aggregate to two digit level
df4 = df4.groupby(['year', 'unitid', 'cip4']).aggregate('sum')
# reset index
df4 = df4.reset_index()
# Create 2-digit CIP code
df4['cip2'] = df4['cip4'].str[:2]
