# create python dictionaries
import pandas as pd

# input: cip2names.dta, cip4names.dta
# output: cip2labels (dict),
#         ciplabels_short (dict),
#         cip4labels_df (df)

# file paths
import os
from sys import platform

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
namepath = basepath + '/data/ipeds/cip_edit/'


######################################
# Create 2-digit CIP code dictionary #
######################################

# Read in variable names
df = pd.read_stata(namepath + 'cip2names.dta')

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

# Finish re-labeling these dictionaries, and cleaning the data below

######################################
# Create 4-digit CIP code dictionary #
######################################

# Read in variable names
df = pd.read_stata(namepath + 'cip4names.dta')

# create 2-digit CIP code
df['cip2'] = df['cip4'].str[:2]

# remove periods; change capitalization
df['ciptitle2010'] = df['ciptitle2010'].str.replace('.', '')
df['ciptitle2010'] = df['ciptitle2010'].str.capitalize()

# set index; create dataframe
cip4labels_df = df.set_index(['cip2', 'cip4'])

# to create dictionary:
# cip4df.loc['01'].to_dict()['ciptitle2010']
