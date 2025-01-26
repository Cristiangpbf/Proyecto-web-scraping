from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Configura Chrome para trabajar en modo headless (sin ventana)
options = Options()

# Ruta al ejecutable de ChromeDriver
service = Service("./chromedriver-win64/chromedriver.exe")

my_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=1950-01-01,2025-12-31&sort=num_votes,desc"

# Crea el navegador
driver = webdriver.Chrome(service=service, options=options)
driver.get(my_url)

# Esperar explícitamente a que un elemento clave esté presente
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item"))
)
# total_paginas = 10426
total_paginas = 10

# # # # Descomentar para hacer clic en el páginador y cargar 50 peliculas nuevas en cada iteración.
#
# for i in range(total_paginas):
#     btn_paginator = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable(
#             (By.CLASS_NAME,
#              "ipc-btn.ipc-btn--single-padding.ipc-btn--center-align-content.ipc-btn--default-height.ipc-btn--core-base.ipc-btn--theme-base.ipc-btn--button-radius.ipc-btn--on-accent2.ipc-text-button.ipc-see-more__button")
#         )
#     )
#     # btn_paginator = driver.find_element(By.CLASS_NAME, "ipc-btn.ipc-btn--single-padding.ipc-btn--center-align-content.ipc-btn--default-height.ipc-btn--core-base.ipc-btn--theme-base.ipc-btn--button-radius.ipc-btn--on-accent2.ipc-text-button.ipc-see-more__button")
#     ActionChains(driver).move_to_element(btn_paginator).perform()
#     btn_paginator.click()

s_container = driver.find_elements(By.CLASS_NAME, "sc-2bfd043a-3.jpWwpQ.dli-parent")

# Archivo de salida
filename = "./imdb_m.csv"
f = open(filename, "w", encoding="utf-8")

# Encabezados del archivo CSV
headers = "Pos,Title,Year,Runtime,Clasif,Rating,VoteCount,Score,Plot\n"
f.write(headers)

separador = ";"
salto = "\n"
count = 0

for container in s_container:
    # Título de la película
    name = container.find_element(By.CLASS_NAME, "ipc-title__text").text

    # Dividir el texto en número y título
    parts = name.split(".", 1)  # Dividimos solo en el primer punto
    number = parts[0].strip()  # Número, eliminando espacios
    title = parts[1].strip()  # Título, eliminando espacios

    f.write(number + separador)
    f.write(title + separador)

    year_runtime_clasif_mov = container.find_elements(By.CLASS_NAME, "sc-300a8231-7")

    year_mov, runtime_mov, clasif_mov = [element.text if element else "N/A" for element in year_runtime_clasif_mov]

    f.write(year_mov + separador)
    f.write(runtime_mov + separador)
    f.write(clasif_mov + separador)

    rating_group = container.find_element(By.CLASS_NAME, "ipc-rating-star--rating")
    rating = rating_group.text if rating_group else "N/A"
    f.write(rating + separador)

    voteCount_group = container.find_element(By.CLASS_NAME, "ipc-rating-star--voteCount")
    voteCount = voteCount_group.text if voteCount_group else "N/A"
    voteCount = voteCount.lstrip().replace('(', '').replace(')', '')
    f.write(voteCount + separador)

    score_group = container.find_element(By.CLASS_NAME, "sc-b0901df4-0")
    score = score_group.text if score_group else "N/A"
    f.write(score + separador)

    plot_group = container.find_element(By.CLASS_NAME, "ipc-html-content-inner-div")
    plot = plot_group.text if plot_group else "N/A"
    plot = plot.lstrip().rstrip().replace(';', '')
    f.write(plot + separador)

    f.write(salto)

# Cierra el archivo
f.close()

# Cierra el navegador
driver.quit()
