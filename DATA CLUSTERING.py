## CLUSTERING     SCATTER PLOT##

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans # clustering- k means
import matplotlib.pyplot as plt #visualizar datos


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


df_equipos['Partidos Ganados'] = pd.to_numeric(df_equipos['Partidos Ganados'])

# SE CREA EL MODELO DE CLUSTERING USANDO EL ALGORITMO K-MEANS
modelo = KMeans(n_clusters=4, n_init=10)

#SE ENTRENA EL MODELO UTILIZANDO LOS DATOS DE LOS PARTIDOS GANADOS
modelo.fit(df_equipos[['Partidos Ganados']])

#SE AGREGA LA COLUMNA DE CLUSTERS AL DF ORIGINAL
df_equipos['Cluster'] = modelo.predict(df_equipos[['Partidos Ganados']])

#SE MUESTRA UNA COLUMNA NUEVA EN EL QUE SE AGREGAN LOS CLUSTERS
print(df_equipos)


## VISUALIZARLO DE MANERA GRÁFICA##

#SE FILTRAN LOS DATOS QUE QUEREMOS GRAFICAR PARA X,Y
X = df_equipos[['Puntos', 'Partidos Ganados']]

#APLICAMOS EL K MEANS CON n CLUSTERS
kmeans = KMeans(n_clusters=4, n_init=10).fit(X)

#SE AGREGA LA COLUMNA DE CLUSTERS AL DF ORIGINAL
df_equipos['Cluster'] = kmeans.labels_

#GENERAMOS EL GRÁFICO DE DISPERSIÓN
plt.scatter(X['Puntos'], X['Partidos Ganados'], c=kmeans.labels_)
plt.title('Clustering de equipos')
plt.xlabel('Puntos')
plt.ylabel('Partidos Ganados')
plt.show()

