import pandas as pd
import numpy as np
import re

def resetDF():
    dates = pd.date_range('20180101', periods=4)
    featureNames = list('ABCD')
    return pd.DataFrame(np.random.randn(4,4), index=dates, columns=featureNames)
df = resetDF()
df[df.A > df.mean().loc['A']] #split by half
dfZero = pd.DataFrame(np.zeros_like(df), index=df.index, columns=df.columns)
dfZero
df.loc['20180101']
df.loc['20180101','A']
df.iloc[3]
df.iloc[3,3]
df2 = df.copy()
df2['E'] = ['one', 'two', 'three', 'four']
df2
df2Cut = df2[df2['E'].isin(['two','four'])]
df
df.apply(np.cumsum)
df.apply(lambda x: x.max() - x.min())
