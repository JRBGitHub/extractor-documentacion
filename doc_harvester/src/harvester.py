"""
Documentation Harvester - Clase principal
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import json
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from .utils import html_utils, file_utils

@dataclass
class DocumentationSection:
    """Representa una sección de documentación"""
    title: str
    content: str
    code_examples: List[str]
    category: str
    url: str

class DocumentationHarvester:
    """Clase principal para extraer documentación"""
    
    def __init__(self, base_url: str, output_dir: str = "output"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_urls: Set[str] = set()
        self.setup_driver()
    
    def setup_driver(self):
        """Configura el driver de Selenium"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Modo headless
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def harvest(self, start_url: Optional[str] = None):
        """Inicia el proceso de extracción"""
        if start_url is None:
            start_url = self.base_url
        
        try:
            self._process_url(start_url)
        finally:
            self.driver.quit()
    
    def _process_url(self, url: str):
        """Procesa una URL y extrae su documentación"""
        if url in self.visited_urls or not self._is_valid_url(url):
            return
        
        self.visited_urls.add(url)
        print(f"Procesando: {url}")
        
        self.driver.get(url)
        sleep(2)  # Esperar a que cargue la página
        
        # Extraer contenido
        html = self.driver.page_source
        section = self._extract_section(html, url)
        
        if section:
            self._save_section(section)
        
        # Encontrar más enlaces para procesar
        links = html_utils.extract_links(html)
        for link in links:
            absolute_url = urljoin(url, link)
            if self._should_process_url(absolute_url):
                self._process_url(absolute_url)
    
    def _extract_section(self, html: str, url: str) -> Optional[DocumentationSection]:
        """Extrae una sección de documentación del HTML"""
        soup = BeautifulSoup(html, 'lxml')
        
        # Intentar encontrar el título
        title = soup.find('h1')
        if not title:
            title = soup.find('title')
        title_text = title.get_text(strip=True) if title else "Sin título"
        
        # Extraer contenido principal
        main_content = soup.find(['main', 'article'])
        if not main_content:
            main_content = soup.find('div', {'class': ['content', 'main', 'documentation']})
        
        if not main_content:
            return None
        
        content = html_utils.clean_html(str(main_content))
        code_examples = html_utils.find_code_blocks(content)
        category = self._determine_category(soup)
        
        return DocumentationSection(
            title=title_text,
            content=content,
            code_examples=code_examples,
            category=category,
            url=url
        )
    
    def _determine_category(self, soup: BeautifulSoup) -> str:
        """Determina la categoría de la documentación"""
        # Intentar encontrar la categoría en la navegación o breadcrumbs
        nav = soup.find(['nav', 'breadcrumb'])
        if nav:
            return nav.get_text(strip=True).split()[0]
        return "General"
    
    def _save_section(self, section: DocumentationSection):
        """Guarda una sección de documentación"""
        # Crear nombre de archivo seguro
        safe_title = "".join(c for c in section.title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '-').lower()
        
        # Guardar en JSON
        data = {
            "title": section.title,
            "category": section.category,
            "url": section.url,
            "code_examples": section.code_examples
        }
        
        json_path = os.path.join(self.output_dir, f"{safe_title}.json")
        file_utils.save_json(data, json_path)
        
        # Guardar contenido HTML
        html_path = os.path.join(self.output_dir, f"{safe_title}.html")
        file_utils.save_html(section.content, html_path)
    
    def _is_valid_url(self, url: str) -> bool:
        """Verifica si una URL es válida para procesar"""
        parsed = urlparse(url)
        return (
            parsed.netloc and
            parsed.scheme in ('http', 'https') and
            parsed.netloc in self.base_url
        )
    
    def _should_process_url(self, url: str) -> bool:
        """Determina si una URL debe ser procesada"""
        return (
            self._is_valid_url(url) and
            url not in self.visited_urls and
            'search' not in url.lower() and
            'login' not in url.lower()
        )
