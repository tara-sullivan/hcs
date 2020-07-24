import pandas as pd

import os
import sys
import inspect

try:
    currpath = os.path.abspath(__file__)
except NameError:
    currpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
# rootdir: /hcs/hcs
rootdir = os.path.dirname(os.path.dirname(os.path.dirname(currpath)))
sys.path.append(rootdir)

datapath = rootdir + '/ipeds/historical_data/table28/'


def convert(df, old_col, new_col):
    # Remove weird footnote
    df[new_col] = df[old_col].str.replace('2 ', '')
    # Convert to int
    df[new_col] = df[new_col].str.replace(',', '').astype('int')


def make_df():
    list_data = []
    for table_pg in ['a', 'b', 'c']:
        table_name = datapath + 'table28' + table_pg + '-page-1-table-1.csv'
        # Read in data
        raw_data = pd.read_csv(table_name)

        raw_data['year'] = raw_data['1'].str.slice(0, 4).astype('int')
        raw_data = raw_data.set_index('year')

        convert(raw_data, '2', 'total')
        convert(raw_data, '3', 'men')
        convert(raw_data, '4', 'women')

        clean_data = raw_data[['total', 'men', 'women']]

        list_data.append(clean_data)

    df = pd.concat(list_data)

    # check
    df['check_total'] = df[['men', 'women']].sum(axis=1)
    pd.testing.assert_series_equal(df['total'], df['check_total'],
                                   check_names=False)
    df.drop(columns=['total', 'check_total'], inplace=True)

    return df


if __name__ == '__main__':
    df = make_df()

    print(df.head())
