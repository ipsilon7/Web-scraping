from selenium import webdriver
from selenium.webdriver.common.by import By


def web_driver():
    service = webdriver.ChromeService(executable_path=r"C:\Users\Ivan\Documents\CODING\Python\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.compugarden.com.ar/ARTICULOS/CAT_ID=52/SCAT_ID=-1/SCA_ID=-1/m=0/BUS=/compugarden.aspx")
    return driver


def cant_de_paginas(driver):
    show_items = int(driver.find_element(By.ID, value="cant_a_mostrar").get_attribute("value"))  # Cantidad de productos mostrados por pagina
    total_items_raw = driver.find_element(By.XPATH, value="/html/body/div[3]/div[1]/section/div/div[2]/div[2]/div[2]/div/p").text
    total_items_raw = ' '.join(total_items_raw.split())  # Se borran los espacios extras
    total_items = int(total_items_raw[7:9])  # Se corta la parte con la cantidad de productos y se transforma a entero
    total_pages = round(total_items / show_items)
    if total_pages < (total_items / show_items):
        total_pages += 1
    return total_pages


def print_pages(total_pages):
    print(total_pages)


def main():
    driver_chrome = web_driver()
    total_paginas = cant_de_paginas(driver_chrome)
    print_pages(total_paginas)


if __name__ == '__main__':
    main()
