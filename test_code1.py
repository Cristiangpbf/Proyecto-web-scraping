from urllib.request import urlopen as uReq, Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd

# URL de IMDb para extraer datos
my_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=1950-01-01,2025-12-31&sort=num_votes,desc"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/91.0.4472.124 Safari/537.36"}
req = Request(my_url, headers=headers)
uClient = urlopen(req)
page_html = uClient.read()


# Abre la conexión y descarga el contenido de la página
print(page_html[:500])
print(type(page_html))
decoded_html = page_html.decode("utf-8")
print(decoded_html[:500])  # Muestra los primeros 500 caracteres
uClient.close()

# Analiza la página con BeautifulSoup
page_soup = soup(page_html, "html.parser")

# Encuentra todos los contenedores de películas
containers = page_soup.findAll("div", {"class": "ipc-metadata-list-summary-item"})

# Archivo de salida
filename = "imdb_movies.csv"
f = open(filename, "w", encoding="utf-8")

# Encabezados del archivo CSV
headers = "Name,Year,Runtime\n"
f.write(headers)

# Itera sobre los contenedores y extrae información
for container in containers:
    # Título de la película
    name = container.h3.a.text

    # Año de la película
    year_mov = container.h3.find("span", {"class": "lister-item-year"})
    year = year_mov.text if year_mov else "N/A"

    # Duración de la película
    runtime_mov = container.p.find("span", {"class": "runtime"})
    runtime = runtime_mov.text if runtime_mov else "N/A"

    # Imprime y escribe en el archivo
    print(name + "," + year + "," + runtime + "\n")
    f.write(name + "," + year + "," + runtime + "\n")

# Cierra el archivo
f.close()