import pandas as pd
import numpy as np

import os
import sys
import inspect

import time
# import pdb

try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
rootdir = os.path.dirname(os.path.dirname(os.path.dirname(currpath)))
sys.path.append(rootdir)

rawpath = '/Volumes/GoogleDrive/My Drive/data/ACS/'
datapath = rootdir + '/data/acs/'

# Read in graduation data

# Info on data:

# 1. size of data
# Num Columns: 15,840,681
# Num Rows: 29
# Size data: 1.82 GB


# 2. Tasks
# Appending columns, dropping rows; boolean logic on rows
def drop_by_row(readdf):
    # pdb.set_trace()
    df = readdf.copy()
    # # drop those living in institutional group quaters
    df.drop(df.loc[df['GQ'] == 3].index, inplace=True)
    df.drop(columns=(df.columns[df.columns.str.startswith('GQ')]),
            inplace=True)

    # born in 50 states or DC
    df.drop(df.loc[(df['BPL'] > 56)].index, inplace=True)
    df.drop(columns=(df.columns[df.columns.str.startswith('BPL')]),
            inplace=True)

    # # Ages between 23-67
    df.drop(df.loc[(df['AGE'] < 23) & (df['AGE'] > 67)].index, inplace=True)

    # drop those with non-imputed values for the following
    df.drop(df.loc[(df['QAGE'] == 4)
                   | (df['QSEX'] == 4)
                   | (df['QRACE'] == 4)
                   | (df['QBPL'] == 4)
                   | (df['QEDUC'] == 4)
                   | (df['QDEGFIELD'] == 4)
                   ].index, inplace=True)
    df.drop(columns=(df.columns[df.columns.str.startswith('Q')]), inplace=True)

    # # 4 years college completion
    df.drop(df.loc[df['EDUCD'] < 101].index, inplace=True)

    return df


# Get data types
dtypes = {
    'YEAR': np.int16,
    'SAMPLE': np.int64,
    'SERIAL': np.int64,
    'CBSERIAL': np.int64,
    'HHWT': np.float64,
    'CLUSTER': np.int64,
    'STRATA': np.int64,
    'GQ': np.int64,
    'PERNUM': np.int64,
    'PERWT': np.float64,
    'SEX': np.int16,
    'AGE': np.int16,
    'BIRTHYR': np.int16,
    'RACE': np.int16,
    'RACED': np.int16,
    'BPL': np.int64,
    'BPLD': np.int64,
    'EDUC': np.int16,
    'EDUCD': np.int16,
    'DEGFIELD': np.int16,
    'DEGFIELDD': np.int16,
    'DEGFIELD2': np.int16,
    'DEGFIELD2D': np.int16,
    'QAGE': np.int16,
    'QSEX': np.int16,
    'QBPL': np.int16,
    'QRACE': np.int16,
    'QEDUC': np.int16,
    'QDEGFIELD': np.int16,
}

# Compressed file
# Engine = c
print('compressed with c engine')
start_time = time.time()
df = pd.read_csv(rawpath + 'usa_00005.csv.gz', dtype=dtypes, sep=',',
                 engine='c', compression='gzip')
print('time to load: %s' % (time.time() - start_time))
df = drop_by_row(df)
with pd.HDFStore(datapath + 'acs.h5', mode='w') as store:
    store['df'] = df
print('time to clean and save: %s' % (time.time() - start_time))

# # chunk size
# print('pd.read_csv with chunk size')
# start_time = time.time()
# reader = pd.read_csv(rawpath + 'usa_00005.csv.gz', dtype=dtypes, sep=',',
#                      engine='c', compression='gzip',
#                      iterator=True, chunksize=100000)
# df = pd.concat(reader, ignore_index=True)
# print('time to load: %s' % (time.time() - start_time))
# df = drop_by_row(df)
# print('time to clean: %s' % (time.time() - start_time))

# temporary, for checks
# df = df[(df['YEAR'] >= 2014) & (df['YEAR'] <= 2017)]
# this is still more obs. than in the appendix of Sloane, Hurst, and Black.
