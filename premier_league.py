#PREMIER LEAGUE

import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL del sitio web
url = 'https://www.skysports.com/premier-league-table'

# Hacemos una solicitud GET a la URL y almacenamos la respuesta en una variable
pag = requests.get(url)

# Creamos un objeto BeautifulSoup a partir del contenido HTML de la página
soup = BeautifulSoup(pag.text, 'html.parser')

# Buscamos la tabla que contiene los datos de la liga
tabla = soup.find('table', class_='standing-table__table callfn')

# Creamos una lista vacía para almacenar los datos de los equipos
datos_equipos = []

# Iteramos sobre todas las filas (equipos) de la tabla
for equipos in tabla.find_all('tbody'):
    hilera = equipos.find_all('tr')
    for columna in hilera:
        # Obtenemos el nombre del equipo
        nombre_equipos = columna.find('td', class_='standing-table__cell standing-table__cell--name').text.strip()
        
        # Obtenemos los puntos del equipo
        puntos_equipos = columna.find_all('td', class_='standing-table__cell')[2].text.strip()
        
        # Obtenemos el número de partidos ganados por el equipo
        partidos_ganados = columna.find_all('td', class_='standing-table__cell is-hidden--bp35')[0].text.strip()
        
        # Agregamos los datos del equipo a la lista de datos de equipos
        datos_equipos.append([nombre_equipos, puntos_equipos, partidos_ganados])

# Convertimos la lista de datos de los equipos a un dataframe de pandas
df_equipos = pd.DataFrame(datos_equipos, columns=['Equipo', 'Puntos', 'Partidos Ganados'])

# Guardamos el dataframe en formato CSV
df_equipos.to_csv('Tabla final_premier.csv', index=False)

# Mostramos el dataframe en la consola
print(df_equipos)
