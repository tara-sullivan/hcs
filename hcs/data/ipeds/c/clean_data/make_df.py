# Create ipeds dataframe
# input: ipeds_c_all.dta
# output: df: dataframe of time series
#         df2: 2-digit cip code dataframe
#         df4: 4-digit cip code dataframe

import pandas as pd
from quantecon.util import timing

import os
import sys
import inspect

try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
rootdir = (os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    currpath)))))
sys.path.append(rootdir)

datapath = rootdir + '/ipeds/c/clean_data/'
cippath = rootdir + '/ipeds/c/clean_data/'


class ReadData:
    '''
    Read in IPEDs data and creates a dataframe
    '''
    def __init__(self):
        self.df = self.make_df()
        self.df2 = self.make_df2()
        self.df4 = self.make_df4()

    def make_df(self):
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
        assert 0 == df[(df['ctotalm'].isna()) &
                       (df['ctotalw'].isna())].sum().sum()

        # replace missing values with zeros
        # df['ctotalm'].fillna(0, inplace=True)
        # df['ctotalw'].fillna(0, inplace=True)

        # aggregate over cipcode2010, majornum; reset index
        df = df.groupby(['year', 'unitid', 'cipcode2010']).aggregate('sum')

        # remove columns
        df = df.drop(['awlevel', 'majornum'], axis=1)

        # reset index
        df = df.reset_index()

        return df

    # Create 2-digit CIP code column
    def make_df2(self):
        df2 = self.df
        # Create 2-digit CIP code
        df2['cip2'] = df2['cipcode2010'].str[:2]
        # aggregate to two digit level
        df2 = df2.groupby(['year', 'unitid', 'cip2']).aggregate('sum')
        # reset index
        df2 = df2.reset_index()

        return df2

    def make_df4(self):
        # Create 4-digit CIP code column
        df4 = self.df
        # Create 4-digit CIP code
        df4['cip4'] = df4['cipcode2010'].str[:5]
        # aggregate to two digit level
        df4 = df4.groupby(['year', 'unitid', 'cip4']).aggregate('sum')
        # reset index
        df4 = df4.reset_index()
        # Create 2-digit CIP code
        df4['cip2'] = df4['cip4'].str[:2]

        return df4


class MakeDict:
    '''
    Create python CIP dictionaries
    '''
    def __init__(self):
        self.cip2labels, self.cip2labels_short = self.make_cip2labels()
        self.cip4labels_df = self.make_cip4labels()

    def make_cip2labels(self):
        # Read in variable names
        df = pd.read_stata(cippath + 'cip2names.dta')

        # set index
        df = df.set_index('cip2')

        # remove periods; change capitalization
        df['ciptitle2010'] = df['ciptitle2010'].str.replace('.', '')
        df['ciptitle2010'] = df['ciptitle2010'].str.capitalize()

        # specific edits
        df.loc['01'] = 'Agriculture and related sciences'
        df.loc['10'] = 'Communications technologies and support services'
        df.loc['11'] = 'Computer and information services'
        df.loc['15'] = 'Engineering technologies'
        df.loc['16'] = 'Foreign languages'
        df.loc['19'] = 'Family and consumer sciences'
        df.loc['24'] = 'Liberal arts'
        df.loc['26'] = 'Biological sciences'
        df.loc['30'] = 'Interdisciplinary studies'
        df.loc['43'] = 'Law enforcement and protective services'
        df.loc['52'] = 'Business and related services'

        # to dictionary
        cip2labels = df.to_dict()['ciptitle2010']

        df.loc['05'] = 'Group studies'
        df.loc['09'] = 'Communcation'
        df.loc['10'] = 'Communications tech.'
        df.loc['11'] = 'Computer services'
        df.loc['27'] = 'Math and stats'
        df.loc['30'] = 'Interdisciplinary'
        df.loc['43'] = 'Law enforcement'
        df.loc['50'] = 'Arts'
        df.loc['51'] = 'Health'
        df.loc['52'] = 'Business'

        # to dictionary
        cip2labels_short = df.to_dict()['ciptitle2010']

        return cip2labels, cip2labels_short

    def make_cip4labels(self):
        # Read in variable names
        df = pd.read_stata(cippath + 'cip4names.dta')

        # create 2-digit CIP code
        df['cip2'] = df['cip4'].str[:2]

        # remove periods; change capitalization
        df['ciptitle2010'] = df['ciptitle2010'].str.replace('.', '')
        df['ciptitle2010'] = df['ciptitle2010'].str.capitalize()

        # set index; create dataframe
        cip4labels_df = df.set_index(['cip2', 'cip4'])

        return cip4labels_df


ipeds_df = ReadData()
df, df2, df4 = ipeds_df.df, ipeds_df.df2, ipeds_df.df4

ipeds_dict = MakeDict()
cip2labels = ipeds_dict.cip2labels
cip2labels_short = ipeds_dict.cip2labels_short
cip4labels_df = ipeds_dict.cip4labels_df