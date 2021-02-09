import pandas as pd
from scipy.signal import argrelextrema
import numpy as np



class ChartAnalyzer:


    def __init__(self):
        pass


    def extreams(self, df, order=3):
        """
        Returns the extreames of the timeseries provided
        https://eddwardo.github.io/posts/2019-06-05-finding-local-extreams-in-pandas-time-series/
        """

        # Do I want to provide the column in the function parameters?

        col = df.price.values
        ilocs_min = argrelextrema(col, np.less_equal, order=order)[0]
        ilocs_max = argrelextrema(col, np.greater_equal, order=order)[0]

        df['local_min'] = False
        df['local_max'] = False

        df.loc[df.iloc[ilocs_min].index, 'local_min'] = True
        df.loc[df.iloc[ilocs_max].index, 'local_max'] = True

        return df


    # Basic Analyze:
        # mix, max, mean
        # log Returns
