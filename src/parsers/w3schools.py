"""
Documentation Harvester - Parser específico para W3Schools
"""

from bs4 import BeautifulSoup
from typing import List, Dict
from .base import DocumentationParser

class W3SchoolsParser(DocumentationParser):
    """Parser específico para W3Schools"""
    
    def parse_section(self, html: str) -> dict:
        """Parsea una sección de W3Schools"""
        soup = BeautifulSoup(html, 'lxml')
        
        # Obtener el título principal
        title = soup.find(['h1', 'h2'])
        title_text = title.get_text(strip=True) if title else "Sin título"
        
        # Obtener el contenido principal
        main_content = soup.find('div', {'id': 'main'})
        if not main_content:
            main_content = soup.find('div', {'class': 'w3-main'})
        
        content = str(main_content) if main_content else ""
        
        # Extraer ejemplos de código
        code_examples = self.extract_code_examples(html)
        
        # Determinar categoría
        category = self.get_category(html)
        
        return {
            "title": title_text,
            "content": content,
            "code_examples": code_examples,
            "category": category
        }
    
    def extract_code_examples(self, html: str) -> List[str]:
        """Extrae ejemplos de código de W3Schools"""
        soup = BeautifulSoup(html, 'lxml')
        examples = []
        
        # Buscar en diferentes tipos de bloques de código de W3Schools
        code_blocks = soup.find_all([
            'div', 'pre'
        ], class_=[
            'w3-example',
            'w3-code',
            'notranslate'
        ])
        
        for block in code_blocks:
            code = block.get_text(strip=True)
            if code:
                examples.append(code)
        
        return examples
    
    def get_category(self, html: str) -> str:
        """Obtiene la categoría de la página de W3Schools"""
        soup = BeautifulSoup(html, 'lxml')
        
        # Intentar obtener la categoría del menú de navegación
        nav = soup.find('nav', {'class': 'w3-sidenav'})
        if nav:
            current = nav.find('a', {'class': 'active'})
            if current:
                return current.get_text(strip=True)
        
        # Intentar obtener del título de la página
        title = soup.find('title')
        if title:
            title_text = title.get_text()
            if ' - ' in title_text:
                return title_text.split(' - ')[0].strip()
        
        return "General"
