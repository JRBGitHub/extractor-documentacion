# Web Scraping Tool

Esta es una herramienta de web scraping que te permite extraer información de páginas web y guardarla en formatos JSON o CSV para su posterior uso.

## Características

- Extracción de datos de páginas web usando BeautifulSoup4
- Manejo de headers personalizados para evitar bloqueos
- Guardado de datos en formato JSON y CSV
- Soporte para selectores CSS personalizados
- Manejo de errores robusto

## Requisitos

- Python 3.7+
- beautifulsoup4
- requests
- pandas

## Instalación

1. Clona este repositorio o descarga los archivos
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1. Modifica el archivo `main.py` con la URL y los selectores CSS que necesites
2. Ejecuta el script:

```bash
python main.py
```

## Ejemplo de uso personalizado

```python
from scraper import WebScraper

scraper = WebScraper()

# Define la URL y los selectores
url = "https://tuwebsite.com"
selectors = {
    "titulo": "h1.title",
    "precio": "span.price",
    "descripcion": "div.description"
}

# Obtiene y procesa los datos
soup = scraper.get_page_content(url)
if soup:
    data = scraper.extract_data(soup, selectors)
    scraper.save_to_json([data], "resultados.json")
    scraper.save_to_csv([data], "resultados.csv")
```

## Nota importante

Asegúrate de revisar los términos de servicio y las políticas de robots.txt de los sitios web que planeas scrapear. Algunos sitios web no permiten el web scraping o tienen restricciones específicas.
