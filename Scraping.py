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
# IMPORTAR PAQUETES
from typing import Any
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import time

# INICIO

# Cargamos el webdriver de selenium
URL = "https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52/SCAT_ID=-1/SCA_ID=-1/m=0/BUS=/compugarden.aspx"
service = webdriver.ChromeService(executable_path=r"C:\Users\Ivan\Documents\CODING\Python\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(URL)
time.sleep(2)

# Verigicamos el estado de la URL
base_url = f"https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52;SCAT_ID=-1;SCA_ID=-1;m=0;BUS=;A_PAGENUMBER={page};/compugarden.aspx"
pedido_obtenido = requests.get(base_url)
if pedido_obtenido.status_code != 200:
    print("Pagina inaccesible")

# Parseamos la pagina
html_obtenido = pedido_obtenido.text  # Conversion a texto
soup = BeautifulSoup(html_obtenido, "html.parser")  # Parseo

########################################################

Se puede optimizar esta funcion?:

def cant_de_paginas(driver):
    show_items = int(driver.find_element(By.ID, value="cant_a_mostrar").get_attribute("value"))  # Cantidad de productos mostrados por pagina
    total_items_raw = driver.find_element(By.XPATH, value="/html/body/div[3]/div[1]/section/div/div[2]/div[2]/div[2]/div/p").text
    total_items_raw = ' '.join(total_items_raw.split())  # Se borran los espacios extras
    total_items = int(total_items_raw[7:9])  # Se corta la parte con la cantidad de productos y se transforma a entero
    total_pages = round(total_items / show_items)
    if total_pages < (total_items / show_items):
        total_pages += 1
    return total_pages

# EXTRACCION DE DATOS NUEVOS
# Obtener y extraer datos


def extraccion_de_productos(soup):
    divs_products = soup.find_all('div', class_='product')
    return divs_products


def extraccion_de_precios(soup):
    divs_precios = soup.find_all('div', class_='price')
    return divs_precios


def lista_productos(divs_products):
    products = []
    # Bucle para agregar los productos a la lista
    for z in divs_products:
        product = z.h4.get_text(strip=True)
        products.append(product)
    return products


def lista_precios(divs_precios):  # Bucle para agregar los precios a la lista
    precios = []
    for x in divs_precios:
        price = x.get_text(strip=True).replace('$ ', '')  # Quita espacios en blanco y simbolo $
        price = price.replace('.', '')  # Quita punto de miles
        price = price.replace(',', '.')  # Reemplaza la coma decimal por punto
        price = float(price)  # Convierte el numero en flotante
        precios.append(price)
    return precios


def fecha_actual() -> str:
    """Fecha actual del scrapeo

    Returns:
        str: fecha con formato para tabla
    """
    current_date = date.today()
    formatted_date = current_date.strftime("%d-%m-%Y")
    return formatted_date


def fecha_por_producto(formatted_date: str, products: list) -> list:
    fecha = []
    i = 0
    while i < len(products):
        fecha.append(formatted_date)
        i += 1
    return fecha

# GUARDAR DATOS EN DATAFRAME
# Crear diccionario para el dataframe

def crear_dataframe(products, precios, fecha):
    data = dict([
                ("Prcesadores", products),
                ("Precios", precios),
                ("Fecha", fecha)
                ])
    # Convertimos el diccionario en un dataframe
    tabla = pd.DataFrame(data)
    return tabla

# AGREGAR AL ARCHIVO DEL HISTORIAL
# Leer archivo excel, especificando el tipo de dato de cada columna ("nombre
# de columna": tipo de dato), en el argumento sheetname se especifica el
# nombre de la pestaña donde estan los datos

def recuperar_tabla_anterior():
    tabla_ant = pd.read_excel('Historial_de_precios.xlsx', sheet_name=0, header=0, converters={'Procesadores': str, 'Precio': float, 'Fecha': str})
    # Convertimos en dataframe los datos recuperados del archivo antiguo.
    tabla_ant_df = pd.DataFrame(tabla_ant)
    tabla_ant_df = tabla_ant_df.drop(tabla_ant_df.columns[[0]], axis=1)  # Borrar primer columna
    return tabla_ant_df

def concatenar_tablas_anterior_nueva(tabla_ant_df, tabla):
    tabla_concatenada = pd.concat([tabla_ant_df, tabla], axis=0, ignore_index=True)
    return tabla_concatenada


# GUARDAR ARCHIVO

def guardar_excel(tabla_concatenada):
    # Crear excel
    writer = pd.ExcelWriter("Historial_de_precios.xlsx")
    # Guardar dataframe a excel
    tabla_concatenada.to_excel(writer)
    # Cerrar
    writer.close()


# FINAL


def finalizar(driver):
    driver.quit()
    print("Historial generado correctamente")


def main():
    driver_chrome = web_driver()
    total_paginas = cant_de_paginas(driver_chrome)
    pagina = 1
    while pagina <= total_paginas:
        pedido_obtenido = respuesta_url(pagina)
        soup = parsear_pagina(pedido_obtenido)
        divs_productos = extraccion_de_productos(soup)
        divs_precios = extraccion_de_precios(soup)
        productos = lista_productos(divs_productos)
        precios = lista_precios(divs_precios)
        fecha_formateada = fecha_actual()
        fecha = fecha_por_producto(fecha_formateada,
                                   productos)
        tabla = crear_dataframe(productos,
                                precios,
                                fecha)
        tabla_ant_df = recuperar_tabla_anterior()
        tabla_concatenada = concatenar_tablas_anterior_nueva(tabla_ant_df,
                                                             tabla)
        guardar_excel(tabla_concatenada)
        pagina += 1
    finalizar(driver_chrome)


if __name__ == '__main__':
    main()
