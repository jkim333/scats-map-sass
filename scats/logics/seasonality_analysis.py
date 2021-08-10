import pandas as pd
import numpy as np

COLUMNS = [f'V{str(i).zfill(2)}' for i in range(96)] + ['CT_ALARM_24HOUR']

def seasonality_analysis(scats_data):
    # convert django object instances to pandas dataframe.
    df = pd.DataFrame(list(scats_data.values()))

    # Calculate mean volumes for each NB_DETECTOR and time period pair.
    # 1. Make a copy of df called df2.
    # 2. Make df2_volumes which is the volumes only columns of df2.
    # 2. Convert negative volumes in df2_volume to np.nan.
    # 3. Group by NB_DETECTOR and calculate mean volumes for specific
    #    NB_DETECTOR and time period (e.g. V00). This dataframe is called
    #    df_mean.
    # 4. If any of the mean values are still np.nan, convert to 0.
    df2 = df.copy()

    df2_volumes = df2.loc[:, 'V00':'V95']
    df2_volumes[df2_volumes < 0] = np.nan

    df.loc[:, 'V00':'V95'] = df2_volumes

    df_mean = df.loc[:, 'NB_DETECTOR':'V95'].groupby('NB_DETECTOR').mean()
    df_mean.fillna(0)

    # Handle negative values
    # 1. Loop through each qt_interval_count and create df_specific_day.
    # 2. For each df_specific_day, fill np.nan with df_mean.
    #    Then, sum them up and append it to dfs.
    # 3. Concatenate all dataframes in dfs to create df_final.
    # 4. Convert df_final to json and return it.
    dfs = []
    for qt_interval_count in df['QT_INTERVAL_COUNT'].unique():
        df_specific_day = df[df['QT_INTERVAL_COUNT'] == qt_interval_count].copy()

        df_specific_day.set_index('NB_DETECTOR', drop=False, inplace=True)

        df_specific_day.loc[:, 'NB_DETECTOR':'V95'] = df_specific_day.loc[:, 'NB_DETECTOR':'V95'].fillna(df_mean)

        dfs.append(df_specific_day.groupby('QT_INTERVAL_COUNT').sum().loc[:, COLUMNS])

    df_final = pd.concat(dfs, axis='index')

    return df_final.to_json(orient='table')
