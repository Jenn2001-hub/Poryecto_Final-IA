# src/core/utils.py
import os
from typing import List

def listar_archivos(carpeta: str, ext_permitidas: List[str] = None) -> List[str]:
    if ext_permitidas is None:
        ext_permitidas = [".txt", ".pdf", ".png", ".jpg", ".jpeg"]
    archivos = []
    for nombre in sorted(os.listdir(carpeta)):
        if any(nombre.lower().endswith(ext) for ext in ext_permitidas):
            archivos.append(os.path.join(carpeta, nombre))
    return archivos
