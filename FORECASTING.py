## FORECASTING##

import pandas as pd
import requests
from bs4 import BeautifulSoup
from scipy.stats import ttest_ind  ## statistics test
from sklearn.linear_model import LinearRegression ##linear model
from sklearn.metrics import r2_score ##linear model


url = 'https://www.skysports.com/premier-league-table'


pag = requests.get(url)


soup = BeautifulSoup(pag.text, 'html.parser')


tabla = soup.find('table', class_='standing-table__table callfn')


datos_equipos = []


for equipos in tabla.find_all('tbody'):
    hilera = equipos.find_all('tr')
    for columna in hilera:

        nombre_equipos = columna.find('td', class_='standing-table__cell standing-table__cell--name').text.strip()
     
        puntos_equipos = columna.find_all('td', class_='standing-table__cell')[9].text.strip()
        
       
        partidos_ganados = columna.find_all('td', class_='standing-table__cell is-hidden--bp35')[0].text.strip()

        datos_equipos.append([nombre_equipos, puntos_equipos, partidos_ganados])


df_equipos = pd.DataFrame(datos_equipos, columns=['Equipo', 'Puntos', 'Partidos Ganados'])




df_equipos.to_csv('Tabla final_premier.csv', index=False)



print(df_equipos)



### SE CREA EL MODELO DE REGRESION LINEAL
modelo = LinearRegression()

#EL MODELO SE ENTRENA EN BASE A LOS PARTIDOS GANADOS Y LOS PUNTOS OBTENIDOS
modelo.fit(df_equipos[['Partidos Ganados']], df_equipos['Puntos'])

#SE REALIZA UNA "PREDICCIÓN" DE LOS PUNTOS QUE SE OBTENDRÁN SI SE GANAN 10 PARTIDOS EN LA TEMPORADA

prediccion = modelo.predict([[10]])

print("Un equipo con 10 partidos ganados tendría aproximadamente", round(prediccion[0]), "puntos en la temporada.")
