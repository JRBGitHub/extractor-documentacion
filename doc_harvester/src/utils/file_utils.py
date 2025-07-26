"""
Documentation Harvester - Utilidades para manejo de archivos
"""

import os
import json
from typing import Any, Dict
from pathlib import Path

def ensure_directory(path: str) -> None:
    """Asegura que un directorio existe"""
    Path(path).mkdir(parents=True, exist_ok=True)

def save_json(data: Dict[str, Any], filepath: str) -> None:
    """Guarda datos en formato JSON"""
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_json(filepath: str) -> Dict[str, Any]:
    """Carga datos desde un archivo JSON"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_markdown(content: str, filepath: str) -> None:
    """Guarda contenido en formato Markdown"""
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def save_html(content: str, filepath: str) -> None:
    """Guarda contenido en formato HTML"""
    ensure_directory(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
