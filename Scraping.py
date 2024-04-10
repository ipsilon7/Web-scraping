"""""""""""""""""""""""""""""""""""""""
        SECUENCIA DE SCRAPING
.IMPORTAR PAQUETES
.CARGAR WEBDRIVER 
.AVERIGUAR CANTIDAD TOTAL DE PAGINAS
.WHILE page < (total_pages+1)
    OBTENER Y PARSEAR LA URL 
    EXTRAER INFO DE PRODUCTOS
    GUARDAR DATOS EN UN DATAFRAME
    AGREGARLO AL ARCHIVO EXISTENTE
    GUARDAR ARCHIVO
    PASAR DE PAGINA, INCREMENTAR BUCLE Y REPETIR
.FINALIZAR PROGRAMA

"""""""""""""""""""""""""""""""""""""""
############################## IMPORTAR PAQUETES ##############################
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import time

############################## INICIO ##############################
# Cargamos el webdriver de selenium
def web_driver() -> webdriver:
    service = webdriver.ChromeService(executable_path=r"C:\Users\Ivan\Documents\CODING\Python\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52/SCAT_ID=-1/SCA_ID=-1/m=0/BUS=/compugarden.aspx")
    return driver

############################## AVERIGUANDO CUANTAS PAGINAS HAY EN ESTA CATEGORIA ##############################
def cant_de_paginas(driver) -> int:
    show_items = int(driver.find_element(By.ID, value="cant_a_mostrar").get_attribute("value")) # Cantidad de productos mostrados por pagina
    total_items_raw = driver.find_element(By.XPATH, value="/html/body/div[3]/div[1]/section/div/div[2]/div[2]/div[2]/div/p").text
    total_items_raw = ' '.join(total_items_raw.split()) # Se borran los espacios extras
    total_items = int(total_items_raw[7:9]) # Se corta la parte con la cantidad de productos y se transforma a entero
    total_pages = round(total_items / show_items)
    if total_pages < (total_items / show_items):
        total_pages += 1
    return total_pages

############################## BUCLE DE SCRAPEO ##############################
page = 1
while page < (cant_de_paginas() + 1):
    
    def respuesta_url(page:int) -> :
        time.sleep(2)
        base_url = f"https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52;SCAT_ID=-1;SCA_ID=-1;m=0;BUS=;A_PAGENUMBER={page};/compugarden.aspx"
        pedido_obtenido = requests.get(base_url)
        if pedido_obtenido.status_code != 200:
            return print("Pagina caida")
        return pedido_obtenido
    
    def parsear_pagina(pedido_obtenido):
        html_obtenido = pedido_obtenido.text
        soup = BeautifulSoup(html_obtenido,"html.parser") # Parseamos el HTML
        return soup
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
   

    def fecha_actual() -> str:
        current_date = date.today()
        formatted_date = current_date.strftime("%d-%m-%Y")
        return formatted_date
    
    def fecha_por_producto(formatted_date:str, products:list) -> list:
        fecha = []
        i = 0
        while i < len(products):
            fecha.append(formatted_date)
            i+=1
        return fecha

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

    ############################## PASAR DE PAGINA E INCREMENTO DEL BUCLE ##############################
    # PASAR DE PAGINA ES SOLO PARA ALGO VISUAL, SU AUSENCIA NO MODIFICA EL RESULTADO
    next_page = driver.find_element(By.XPATH, value="/html/body/div[3]/div[1]/section/div/div[2]/div[2]/div[2]/div/div/li[5]/a")
    next_page.click() 
    # Incremento
    page += 1

############################## FINAL ##############################
driver.quit()
print("Historial generado correctamente")