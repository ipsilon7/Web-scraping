"""CREAR ARCHIVO EXCEL A PARTIR DE UN DATAFRAME DE PANDAS"""
import pandas as pd
# Diccionario con datos que vamos a usar
data = {"Producto":["Pro1","Pro2","Pro3"],
        "Fecha":["22-03-24","22-03-24","22-03-24"],
        "Precios":[5250.36, 4526.36, 7563.36]}
# Crear dataframe
tabla = pd.DataFrame(data)
# Crear excel
writer = pd.ExcelWriter("Historial_de_precios.xlsx")
# Convertir dataframe a excel
tabla.to_excel(writer)
# Guardar
writer.close()
print("Historial generado correctamente")


"""AGREGAR DATOS A UN EXCEL YA EXISTENTE"""
import pandas as pd
# Leer archivo excel, especificando el tipo de dato de cada columna ("nombre de columna": tipo de dato),
# en el argumento sheetname se especifica el nombre de la pestaña donde estan los datos
dataframe = pd.read_excel('Book1.xlsx', sheet_name=0, header=0, converters={'names':str,'ages':str})
# Crear dataframe
tabla = pd.DataFrame(dataframe)
# Contar filas de un dataframe para agregar los datos debajo de la ultima fila
tabla.count(axis=1) # axis es la columna de la cual se quiere contar las filas
""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Crear diccionario para el dataframe
data = dict([ 
            ("Prcesadores", productos),
            ("Precios", precios),
            ("Fecha", fecha)
])


"""SCRAPEAR VARIAS PAGINAS"""
// pip3 install requests
import requests

// pip3 install beautifulsoup4
from bs4 import BeautifulSoup

// pip3 install pandas
import pandas as pd

books = []

for i in range(1,5):
  url = f"https://books.toscrape.com/catalogue/page-{i}.html"
  response = requests.get(url)
  response = response.content
  soup = BeautifulSoup(response, 'html.parser')
  ol = soup.find('ol')
  articles = ol.find_all('article', class_='product_pod')
  for article in articles:
    image = article.find('img')
    title = image.attrs['alt']
    starTag = article.find('p')
    star = starTag['class'][1]
    price = article.find('p', class_='price_color').text
    price = float(price[1:])
    books.append([title, star, price])
    

df = pd.DataFrame(books, columns=['Title', 'Star Rating', 'Price'])
df.to_csv('books.csv')

"""OBTENER TOTAL DE ITEMS E ITEMS MOSTRADOS"""


"""CALCULAR CANTIDAD DE PAGINAS"""
x = 51
y = 28
z = round(x / y)
if z < (x/y):
    z += 1
print(z)
print(type(z))

"""ESPERAR PARA QUE CARGUE LA PAGINA X TIEMPO"""
time.sleep(2) # 2 segundos