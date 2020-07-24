import pandas as pd
import numpy as np

file = 'ICPSR_{id}/DS{ds}/{id}-{ds}-Data.dta'.format(id='02138', ds='0001')

df = pd.read_stata(file)

# I think this is the correct thing to do, 
# but the documentation is barely legible
# df = df[df['SYSCODE'] == 'A']

# df = df.rename({'FICE': 'inst'})
print(np.unique(df['SEQCODE'].loc[df['SYSCODE'] == 'A'], return_counts=True))
print(np.unique(df['SYSCODE'].loc[df['SEQCODE'] == 'D'], return_counts=True))

