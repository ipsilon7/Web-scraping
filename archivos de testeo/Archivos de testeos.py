from bs4 import BeautifulSoup
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
import requests
import time


base_url = "https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52;SCAT_ID=-1;SCA_ID=-1;m=0;BUS=;A_PAGENUMBER=1;/compugarden.aspx"
pedido_obtenido = requests.get(base_url)
if pedido_obtenido.status_code != 200:
    print("Pagina caida")
html_obtenido = pedido_obtenido.text
soup = BeautifulSoup(html_obtenido,"html.parser")

print(type(soup))