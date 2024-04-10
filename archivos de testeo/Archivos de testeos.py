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

############################## BUCLE DE SCRAPEO ##############################
page = 1
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

print(type(divs_precios))