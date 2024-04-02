############################## IMPORTAR PAQUETES ##############################
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
import requests
import time

############################## INICIO ##############################
# Cargamos el webdriver de selenium
service = webdriver.ChromeService(executable_path=r"C:\Users\Ivan\Documents\CODING\Python\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52/SCAT_ID=-1/SCA_ID=-1/m=0/BUS=/compugarden.aspx")

############################## AVERIGUANDO CUANTAS PAGINAS HAY EN ESTA CATEGORIA ##############################
show_items = int(driver.find_element(By.ID, value="cant_a_mostrar").get_attribute("value")) # Cantidad de productos mostrados por pagina
total_items_raw = driver.find_element(By.XPATH, value="/html/body/div[3]/div[1]/section/div/div[2]/div[2]/div[2]/div/p").text
total_items_raw = ' '.join(total_items_raw.split()) # Se borran los espacios extras
total_items = int(total_items_raw[7:9]) # Se corta la parte con la cantidad de productos y se transforma a entero
total_pages = round(total_items / show_items)
if total_pages < (total_items / show_items):
  total_pages += 1
print(total_pages)

############################## BUCLE DE SCRAPEO ##############################
page = 1
while page < (total_pages + 1):
    time.sleep(2)
    URL_BASE = f"https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52;SCAT_ID=-1;SCA_ID=-1;m=0;BUS=;A_PAGENUMBER={page};/compugarden.aspx"
    pedido_obtenido = requests.get(URL_BASE)
    html_obtenido = pedido_obtenido.text
    # Parseamos el HTML
    soup = BeautifulSoup(html_obtenido,"html.parser")
    ############################## EXTRACCION DE DATOS NUEVOS ##############################
    # Obtener y extraer datos
    divs_products = soup.find_all('div', class_='product')
    divs_precios = soup.find_all('div', class_='price')
    products = []
    precios = []
    # Bucle para obtener los productos
    for z in divs_products:
        product = z.h4.get_text(strip=True)
        products.append(product)
    # Bucle para obtener los precios
    for x in divs_precios:
        price = x.get_text(strip=True).replace('$ ', '')
        price = price.replace('.', '')
        price = price.replace(',', '.')
        price = float(price)
        precios.append(price)
    # Variable fecha
    current_date = date.today()
    formatted_date = current_date.strftime("%d-%m-%Y")
    fecha = []
    i = 0
    while i < len(products):
        fecha.append(formatted_date)
        i+=1

    ############################## GUARDAR DATOS EN DATAFRAME ##############################
    # Crear diccionario para el dataframe
    data = dict([ 
                ("Prcesadores", products),
                ("Precios", precios),
                ("Fecha", fecha)
    ])
    # Convertimos el diccionario en un dataframe
    tabla = pd.DataFrame(data)

    ############################## AGREGAR AL ARCHIVO DEL HISTORIAL ##############################
    # Leer archivo excel, especificando el tipo de dato de cada columna ("nombre de columna": tipo de dato),
    # en el argumento sheetname se especifica el nombre de la pestaña donde estan los datos
    tabla_ant = pd.read_excel('Historial_de_precios.xlsx', sheet_name=0, header=0, converters={'Procesadores':str,'Precio':float, 'Fecha':str})
    # Convertimos en dataframe los datos recuperados del archivo antiguo.
    tabla_ant_df = pd.DataFrame(tabla_ant)
    tabla_ant_df = tabla_ant_df.drop (tabla_ant_df.columns [[0]], axis= 1) # Borrar primer columna
    tabla_concatenada = pd.concat([tabla_ant_df, tabla], axis=0, ignore_index= True)

    ############################## GUARDAR ARCHIVO ##############################
    # Crear excel
    writer = pd.ExcelWriter("Historial_de_precios.xlsx")
    # Guardar dataframe a excel
    tabla_concatenada.to_excel(writer)
    # Cerrar
    writer.close()

    ############################## INCREMENTO DEL BUCLE ##############################
    page += 1
    print(page)

############################## FINAL ##############################
driver.quit()
print("Historial generado correctamente")