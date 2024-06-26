# IMPORTAR PAQUETES
from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import time

# INICIO
# Cargamos el webdriver de selenium


def web_driver():
    service = webdriver.ChromeService(executable_path=r"C:\Users\Ivan\Documents\CODING\Python\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52/SCAT_ID=-1/SCA_ID=-1/m=0/BUS=/compugarden.aspx")
    return driver


def cant_de_paginas(driver) -> int:
    """Averiguar cuantas paginas tiene la categoria

    Args:
        driver (_type_): _description_

    Returns:
        int: total de paginas de la categoria
    """
    show_items = int(driver.find_element(By.ID, value="cant_a_mostrar").get_attribute("value"))  # Cantidad de productos mostrados por pagina
    total_items_raw = driver.find_element(By.XPATH, value="/html/body/div[3]/div[1]/section/div/div[2]/div[2]/div[2]/div/p").text
    total_items_raw = ' '.join(total_items_raw.split())  # Se borran los espacios extras
    total_items = int(total_items_raw[7:9])  # Se corta la parte con la cantidad de productos y se transforma a entero
    total_pages = round(total_items / show_items)
    if total_pages < (total_items / show_items):
        total_pages += 1
    return total_pages

# BUCLE DE SCRAPEO


while page <= total_pages:

    def respuesta_url(page: int):
        """Estado de la url

        Args:
            page (int): Numero de pagina

        Returns:
            _type_: _description_
        """
        time.sleep(2)
        base_url = f"https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52;SCAT_ID=-1;SCA_ID=-1;m=0;BUS=;A_PAGENUMBER={page};/compugarden.aspx"
        pedido_obtenido = requests.get(base_url)
        if pedido_obtenido.status_code != 200:
            return print("Pagina inaccesible")
        return pedido_obtenido

    def parsear_pagina(pedido_obtenido):
        """Parseo de la url

        Args:
            pedido_obtenido (_type_): _description_

        Returns:
            _type_: _description_
        """
        html_obtenido = pedido_obtenido.text
        soup = BeautifulSoup(html_obtenido, "html.parser")  # Parseamos el HTML
        return soup

    # EXTRACCION DE DATOS NUEVOS
    # Obtener y extraer datos
    def extraccion_de_datos(soup):
        divs_products = soup.find_all('div', class_='product')
        divs_precios = soup.find_all('div', class_='price')
        return divs_precios, divs_products
    # Bucle para agregar los productos a la lista

    def lista_productos(divs_products):
        products = []
        for z in divs_products:
            product = z.h4.get_text(strip=True)
            products.append(product)
        return products
    # Bucle para agregar los precios a la lista

    def lista_precios(divs_precios):
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
    # Leer archivo excel, especificando el tipo de dato de cada columna ("nombre de columna": tipo de dato),
    # en el argumento sheetname se especifica el nombre de la pestaña donde estan los datos
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
    # Crear excel
    def guardar_excel(tabla_concatenada):
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
    print_pages(total_paginas)


if __name__ == '__main__':
    main()
