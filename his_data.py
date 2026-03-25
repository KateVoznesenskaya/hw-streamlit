import pandas as pd

df_data = pd.read_csv('temperature_data.csv')

df_data['rol_temp'] = df_data.groupby('city')['temperature'].transform(lambda x: x.rolling(window = 30, min_periods = 1).mean())

df_data_mn = df_data.groupby(['city', 'season'])['temperature'].mean().reset_index(name = 'mean')
df_data = pd.merge(df_data, df_data_mn, left_on = ['city', 'season'], right_on = ['city', 'season'])

df_data_std = df_data.groupby(['city', 'season'])['temperature'].std().reset_index(name = 'std')
df_data = pd.merge(df_data, df_data_std, left_on = ['city', 'season'], right_on = ['city', 'season'])

df_data['an'] = (df_data['temperature'] > (df_data['mean'] + 2 * df_data['std'])) | (df_data['temperature'] < (df_data['mean'] - 2 * df_data['std']))

df_data.to_csv('historical_data.csv', index = False)