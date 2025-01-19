from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from bs4 import BeautifulSoup

from selenium.webdriver.support.wait import WebDriverWait

# Configura Chrome para trabajar en modo headless (sin ventana)
options = Options()

# Ruta al ejecutable de ChromeDriver
service = Service(
    "D:/CRIS/Documentos/Israel/semestre_9/Tendencias_innovadoras_de_la_profesion/Proyecto-web-scraping/Proyecto-web-scraping/chromedriver-win64/chromedriver.exe")

my_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=1950-01-01,2025-12-31&sort=num_votes,desc"

# Crea el navegador
driver = webdriver.Chrome(service=service, options=options)
driver.get(my_url)

# Esperar explícitamente a que un elemento clave esté presente
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item"))
)

# Obtén el HTML renderizado
html = driver.page_source

# Ahora usa BeautifulSoup para analizar el HTML
page_soup = BeautifulSoup(html, "html.parser")

# Ejemplo de cómo buscar elementos con BeautifulSoup
containers = page_soup.find_all("div", {"class": "sc-b3251686-3 iBNlQv dli-parent"})

# Archivo de salida
filename = "./imdb_m.csv"
f = open(filename, "w")

# Encabezados del archivo CSV
headers = "Name,Year,Runtime,Clasif\n"
f.write(headers)

for container in containers:
    # Título de la película
    name = container.h3.text

    year_runtime_clasif_mov = container.find_all("span", {"class": "sc-300a8231-7 eaXxft dli-title-metadata-item"})

    year_mov, runtime_mov, clasif_mov = year_runtime_clasif_mov

    # Año de la película
    year = year_mov.text if year_mov else "N/A"

    # Duración de la película
    runtime = runtime_mov.text if runtime_mov else "N/A"

    # Clasificación de la película
    clasif = clasif_mov.text if runtime_mov else "N/A"

    print(name + "," + year + "," + runtime + "," + clasif + "\n")
    f.write(name + "," + year + "," + runtime + "," + clasif + "\n")

# Cierra el archivo
f.close()

# Cierra el navegador
driver.quit()
