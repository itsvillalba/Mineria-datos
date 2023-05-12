#PREMIER LEAGUE
# predecir el número de puntos de un equipo en función de su
#número de partidos ganados, el cual muestra una tendencia
# mientr
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt ## data visualization
import seaborn as sns #data visualization
from scipy.stats import ttest_ind  ## statistics test
from sklearn.linear_model import LinearRegression ##linear model
from sklearn.metrics import r2_score ##linear model
from sklearn.model_selection import train_test_split ## LINEAR


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

# Convertimos las variables de Partidos Ganados y Puntos a numéricas
###NOTA: SE CONVIERTEN "PARTIDOS GANADOS" Y "PUNTOS" A VALORES NUMÉRICOS PARA
### QUE PUEDAN SER VISUALIZADOS ####
df_equipos['Partidos Ganados'] = pd.to_numeric(df_equipos['Partidos Ganados'])
df_equipos['Puntos'] = pd.to_numeric(df_equipos['Puntos'])
####/////////////////////////////////////###





print(df_equipos)


######
sns.scatterplot(x='Partidos Ganados', y='Puntos', data=df_equipos)
plt.title('Relación entre Partidos Ganados y Puntos')
plt.show()



#SE DIVIDEN LOS DATOS EN CONJUNTO DE ENTRENAMIENTO Y EVALUACIÓN
X_train, X_test, y_train, y_test = train_test_split(df_equipos[['Partidos Ganados']], df_equipos['Puntos'], test_size=0.2)

###SE CREA LA INSTANCIA DEL MODEL DE REGRESION LINEAL
modelo = LinearRegression()

###SE ENTRENA EL MODELO CON LOS DATOS PREVIAMENTE CREADOS
modelo.fit(X_train, y_train)

#SE EVALUA SU PRECISIÓN UTILIZANDO SUS DATOS DE EVALUACIÓN
y_pred = modelo.predict(X_test)

# SE CALCULA EL COEFICIENTE DE DETERMINACION (R²) DEL MODELO CONr2_score()
r2 = r2_score(y_test, y_pred)

print('Precisión del modelo (R²):', r2)

# Hacer una predicción con el modelo
partidos_ganados = 10
puntos_predichos = modelo.predict([[partidos_ganados]])

print('Número de puntos predichos para', partidos_ganados, 'partidos ganados:', puntos_predichos[0])
