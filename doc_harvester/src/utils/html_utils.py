"""
Documentation Harvester - Utilidades para manejo de HTML
"""

from bs4 import BeautifulSoup
from typing import List, Optional
import re

def clean_html(html: str) -> str:
    """Limpia el HTML de elementos no deseados"""
    soup = BeautifulSoup(html, 'lxml')
    
    # Eliminar scripts y estilos
    for script in soup(["script", "style"]):
        script.decompose()
    
    return str(soup)

def extract_text(html: str) -> str:
    """Extrae texto limpio del HTML"""
    soup = BeautifulSoup(html, 'lxml')
    return soup.get_text(separator=' ', strip=True)

def find_code_blocks(html: str) -> List[str]:
    """Encuentra bloques de código en el HTML"""
    soup = BeautifulSoup(html, 'lxml')
    code_blocks = []
    
    # Buscar en elementos <code> y <pre>
    for block in soup.find_all(['code', 'pre']):
        code = block.get_text(strip=True)
        if code:
            code_blocks.append(code)
    
    return code_blocks

def get_meta_description(html: str) -> Optional[str]:
    """Obtiene la meta descripción de una página"""
    soup = BeautifulSoup(html, 'lxml')
    meta = soup.find('meta', attrs={'name': 'description'})
    return meta.get('content') if meta else None

def extract_links(html: str) -> List[str]:
    """Extrae todos los enlaces de una página"""
    soup = BeautifulSoup(html, 'lxml')
    links = []
    
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href and not href.startswith(('#', 'javascript:')):
            links.append(href)
    
    return links
