#PREMIER LEAGUE

import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt ## data visualization
import seaborn as sns #data visualization
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
        
       
        puntos_equipos = columna.find_all('td', class_='standing-table__cell')[2].text.strip()
        
    
        partidos_ganados = columna.find_all('td', class_='standing-table__cell is-hidden--bp35')[0].text.strip()
        
    
        datos_equipos.append([nombre_equipos, puntos_equipos, partidos_ganados])


df_equipos = pd.DataFrame(datos_equipos, columns=['Equipo', 'Puntos', 'Partidos Ganados'])

# Convertir las variables Partidos Ganados y Puntos a numéricas
###NOTA: SE CONVIERTEN "PARTIDOS GANADOS" Y "PUNTOS" A VALORES NUMÉRICOS PARA
### QUE PUEDAN SER VISUALIZADOS ####

df_equipos['Partidos Ganados'] = pd.to_numeric(df_equipos['Partidos Ganados'])
df_equipos['Puntos'] = pd.to_numeric(df_equipos['Puntos'])
####/////////////////////////////////////###

# Guardamos el dataframe en formato CSV
df_equipos.to_csv('Tabla final_premier.csv', index=False)


# Mostramos el dataframe en la consola
print(df_equipos)





### STATISTICS TEST ENTRE EQUIPO 1 Y 2$###
# Seleccionar dos equipos para comparar
equipo1 = df_equipos.loc[0, 'Equipo']
equipo2 = df_equipos.loc[1, 'Equipo']

# SE FILTRAN LOS DATOS PARA OBTENER LOS PARTIDOS GANADOS DE AMBOS EQUIPOS
datos_equipo1 = df_equipos.loc[df_equipos['Equipo'] == equipo1, 'Partidos Ganados']
datos_equipo2 = df_equipos.loc[df_equipos['Equipo'] == equipo2, 'Partidos Ganados']

#SE REALIZA LA PRUEBA DE HIPÓTESIS
t, p = ttest_ind(datos_equipo1, datos_equipo2)



#SE IMPRIMEN LOS RESULTADOS DE LA PRUEBA DE HIPÓTESIS

print(f"La diferencia media en partidos ganados entre {equipo1} y {equipo2} es de {datos_equipo1.mean()-datos_equipo2.mean():.2f} ({equipo1}: {datos_equipo1.mean():.2f}, {equipo2}: {datos_equipo2.mean():.2f})")
if p < 0.05:
    print("La diferencia es estadísticamente significativa (p < 0.05)")
else:
    print("La diferencia no es estadísticamente significativa (p > 0.05)")
    ### TERMINA STATISTICS TEST##############


