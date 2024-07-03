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
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import requests
from bs4 import BeautifulSoup
import time


class WebScraper:
    def __init__(self, url, driver_path):
        self.url = url
        self.driver_path = driver_path
        self.driver = None

    def start_driver(self):
        service = ChromeService(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=service)

    def fetch_page(self):
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

    def scrape(self):
        self.start_driver()
        self.fetch_page()
        base_url = "https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52;SCAT_ID=-1;SCA_ID=-1;m=0;BUS=;A_PAGENUMBER=1;/compugarden.aspx"
        html = self.check_page_status(base_url)
        if html:
            soup = self.parse_page(html)
            return soup
        return None


if __name__ == '__main__':
    url = "https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52/SCAT_ID=-1/SCA_ID=-1/m=0/BUS=/compugarden.aspx"
    driver_path = r"C:\Users\Ivan\Documents\CODING\Python\chromedriver.exe"

    scraper = WebScraper(url, driver_path)
    soup = scraper.scrape()

    if soup:
        pass
