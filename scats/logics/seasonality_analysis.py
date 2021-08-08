import pandas as pd
import numpy as np

def seasonality_analysis(scats_data):
    # convert django object instances to pandas dataframe.
    df = pd.DataFrame(list(scats_data.values()))

    # calculate mean volumes for each NB_DETECTOR and time period pair.
    # 1. make a copy of df called df_all_positive.
    # 2. convert negative volumes in df_all_positive to None.
    # 3. group by NB_DETECTOR and calculate mean volumes for specific
    #    NB_DETECTOR and time period (e.g. V00).
    # 4. If any of the mean values are still None, convert to 0.
    df_positive_or_nan = df.copy()
    df_positive_or_nan.loc[:, 'V00':'V95'][df_positive_or_nan.loc[:, 'V00':'V95'] < 0] = None
    df_mean = df_positive_or_nan.groupby('NB_DETECTOR').mean().loc[:, 'V00':'V95']
    df_mean.fillna(0)

    # handle negative values
    # 1. make a copy of df called df2.
    # 2. convert negative volumes in df2 to None.
    # 3. convert none to the mean values calculated from above.
    df2 = df.copy()
    df2.loc[:, 'V00':'V95'][df2.loc[:, 'V00':'V95'] < 0] = None
    df2.loc[:, 'NB_DETECTOR':'V95'].groupby('NB_DETECTOR').fillna(df_mean)

    df3 = df2.groupby('QT_INTERVAL_COUNT').sum()

    df_final = pd.concat([df3.loc[:, 'V00':'V95'], df3.loc[:, ['CT_ALARM_24HOUR']]], axis=1)

    df_final_json = df_final.to_json(orient='table')

    return df_final_json