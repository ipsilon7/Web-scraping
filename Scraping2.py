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
import re
import math
import time
import pandas as pd
import requests
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By


class WebScraper:
    def __init__(self, url, driver_path):
        self.url = url
        self.driver_path = driver_path
        self.driver = None

    def start_driver(self):
        service = ChromeService(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(self.url)
        time.sleep(2)

    def check_page_status(self, base_url):
        response = requests.get(base_url)
        if response.status_code != 200:
            print("Pagina inaccesible")
            return None
        return response.text

    def parse_page(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def scrape(self, page):
        self.start_driver()
        base_url = f"https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52;SCAT_ID=-1;SCA_ID=-1;m=0;BUS=;A_PAGENUMBER={page};/compugarden.aspx"
        html = self.check_page_status(base_url)
        if html:
            soup = self.parse_page(html)
            scraper = ScraperProductos(soup)
            total_pages = scraper.cant_de_paginas(self.driver)
            print(f"Total de páginas: {total_pages}")
            return soup
        return None


class ScraperProductos:
    def __init__(self, soup):
        self.soup = soup
        self.products = []
        self.precios = []

    def extraccion_de_productos(self):
        divs_products = self.soup.find_all('div', class_='product')
        self.products = [div.h4.get_text(strip=True) for div in divs_products]

    def extraccion_de_precios(self):
        divs_precios = self.soup.find_all('div', class_='price')
        self.precios = []
        for div in divs_precios:
            price = div.get_text(strip=True).replace('$ ', '')
            price = price.replace('.', '')
            price = price.replace(',', '.')
            price = float(price)
            self.precios.append(price)

    def lista_productos(self):
        return self.products

    def lista_precios(self):
        return self.precios

    def cant_de_paginas(self, driver):
        show_items = int(driver.find_element(By.ID, value="cant_a_mostrar").get_attribute("value"))  # Cantidad de productos mostrados por página
        total_items_raw = driver.find_element(By.XPATH, value="/html/body/div[3]/div[1]/section/div/div[2]/div[2]/div[2]/div/p").text
        total_items_raw = total_items_raw.strip().replace('\n', '')  # Quita espacios y saltos de línea
        total_items = int(re.search(r'(\d+)', total_items_raw).group())  # Extrae el primer número encontrado
        total_pages = math.ceil(total_items / show_items)  # Redondea hacia arriba
        return total_pages

    @staticmethod
    def fecha_de_producto(products: list) -> list:
        current_date = date.today()
        formatted_date = current_date.strftime("%d-%m-%Y")
        return [formatted_date] * len(products)


class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def crear_dataframe(self, products, precios, fecha):
        data = {
            "Procesadores": products,
            "Precios": precios,
            "Fecha": fecha
        }
        tabla = pd.DataFrame(data)
        return tabla

    def recuperar_tabla_anterior(self):
        tabla_ant = pd.read_excel(
            self.file_path,
            sheet_name=0,
            header=0,
            converters={'Procesadores': str, 'Precios': float, 'Fecha': str}
        )
        tabla_ant_df = pd.DataFrame(tabla_ant)
        tabla_ant_df = tabla_ant_df.drop(tabla_ant_df.columns[[0]], axis=1)  # Borrar primera columna
        return tabla_ant_df

    def concatenar_tablas_anterior_nueva(self, tabla_ant_df, tabla):
        tabla_concatenada = pd.concat([tabla_ant_df, tabla], axis=0, ignore_index=True)
        return tabla_concatenada

    def guardar_excel(self, tabla_concatenada):
        with pd.ExcelWriter(self.file_path) as writer:
            tabla_concatenada.to_excel(writer)


if __name__ == '__main__':
    # Configuración de la URL y el path del driver
    url = "https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52/SCAT_ID=-1/SCA_ID=-1/m=0/BUS=/compugarden.aspx"
    driver_path = r"C:\Users\Ivan\Documents\CODING\Python\chromedriver.exe"

    # Inicialización del web scraper
    web_scraper = WebScraper(url, driver_path)
    soup = web_scraper.scrape()

    if soup:
        # Extracción de productos y precios
        scraper_productos = ScraperProductos(soup)
        scraper_productos.extraccion_de_productos()
        scraper_productos.extraccion_de_precios()

        # Generación de la fecha actual para los productos
        fecha = ScraperProductos.fecha_de_producto(scraper_productos.lista_productos())

        # Inicialización del manejador de datos
        file_path = 'Historial_de_precios.xlsx'
        data_handler = DataHandler(file_path)

        # Creación del dataframe con los nuevos datos
        tabla_nueva = data_handler.crear_dataframe(scraper_productos.lista_productos(), scraper_productos.lista_precios(), fecha)

        # Recuperación de la tabla anterior y concatenación con los nuevos datos
        tabla_anterior = data_handler.recuperar_tabla_anterior()
        tabla_concatenada = data_handler.concatenar_tablas_anterior_nueva(tabla_anterior, tabla_nueva)

        # Guardado de los datos concatenados en el archivo Excel
        data_handler.guardar_excel(tabla_concatenada)
