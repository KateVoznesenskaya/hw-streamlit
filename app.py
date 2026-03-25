import streamlit as st
import pandas as pd
import requests

st.title('Анализ температурных данных')

file = st.file_uploader('Выберите CSV-файл с историческими данными')
if not file:
    st.info('Загрузите historical_data.csv')
    st.stop()
df_his_data = pd.read_csv(file)

city = st.selectbox('Выберите город', df_his_data['city'].unique())

API_key = st.text_input(label = 'Введите API-ключ OpenWeatherMap', value = '')
if API_key == '':
    st.info('API-ключ OpenWeatherMap не введен')
    st.stop()
response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric')
if response.status_code != 200:
    st.write(response.status_code, response.text)
    st.stop()
w_data = response.json()

cur_t = w_data['main']['temp']
st.write(f'Погода в {city}: {cur_t}')

m_to_s = {1: 'winter', 2: 'winter', 12: 'winter', 3: 'spring', 4: 'spring', 5: "spring", 6: 'summer', 7: 'summer', 8: 'summer', 9: 'autumn', 10: 'autumn', 11: 'autumn'}
cur_s = m_to_s[pd.to_datetime(w_data['dt'], unit = 's').month]
cur_t_mn = df_his_data[(df_his_data['city'] == city) & (df_his_data['season'] == cur_s)]['mean'].mean()
cur_t_st = df_his_data[(df_his_data['city'] == city) & (df_his_data['season'] == cur_s)]['std'].mean()
if (cur_t > (cur_t_mn + 2 * cur_t_st)) or (cur_t < (cur_t_mn - 2 * cur_t_st)):
    st.write(f'Текущяя погода не нормальна для текущего сезона в {city}')
else:
    st.write(f'Текущяя погода нормальна для текущего сезона в {city}')

df_cur_his_data = df_his_data[df_his_data['city'] == city]
if st.checkbox('Показать описательную статистику'):
    st.write(f'Описательная статистика по историческим данным для города {city}')
    st.write(df_cur_his_data.describe())

df_cur_his_data['timestamp'] = pd.to_datetime(df_cur_his_data['timestamp'])
if st.checkbox('Показать временной ряд температур'):
    df_p = df_cur_his_data.copy()
    df_p['col'] = df_cur_his_data['an']
    df_p.loc[df_p['col'] == True, 'col'] = '#ff0000'
    df_p.loc[df_p['col'] == False, 'col'] = '#00ff00'
    st.scatter_chart(df_p, x = 'timestamp', y = 'temperature', color = 'col')
