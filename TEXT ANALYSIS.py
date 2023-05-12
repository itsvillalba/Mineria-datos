## TEXT ANALYSIS ##


import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
import string

#OBTENEMMOS EL CONTENIDO 
url = "https://www.fcfm.uanl.mx/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

#SACAMOS EL TEXTO DE LA PAGINA
texto = soup.get_text()

# AQUÍ EXCLUIMOS LOS CARACTERES
translator = str.maketrans('', '', string.punctuation + '–' + '‘' + '’' + '“' + '”')
texto = texto.translate(translator)

#Tokenizamos EL TEXTO PARA OBTENER LOS SEGMENTOS DE TODO EL TEXTO
tokens = word_tokenize(texto.lower())

#ELIMINAMOS LAS PALABRAS VACÍAS
stop_words = set(stopwords.words("spanish"))
tokens = [token for token in tokens if token.lower() not in stop_words]

#HACEMOS UN CONTEO DE LAS PALABRAS
contador_palabras = Counter(tokens)

#INDICAMOS QUE NOS DÉ LAS 10 PALABRAS MÁS COMUNES
mas_repetidas = contador_palabras.most_common(10)

#CREAMOS LA GRÁFICA
x, y = zip(*mas_repetidas)
plt.bar(x, y)

#SE MUESTRA LA GRÁFICA
plt.show()
