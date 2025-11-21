# src/core/chunking.py
import re
from typing import List

def limpiar_texto(texto: str) -> str:
    # limpia saltos de línea extras y espacios repetidos
    t = texto.replace("\r", " ")
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def crear_chunks(texto: str, tam: int = 300, salto: int = 50) -> List[str]:
    """
    Divide el texto en chunks de 'tam' palabras con solapamiento 'salto'.
    tam: tamaño en palabras
    salto: número de palabras que se solapan entre chunks (overlap)
    """
    texto = limpiar_texto(texto)
    palabras = texto.split()
    if not palabras:
        return []
    chunks = []
    i = 0
    n = len(palabras)
    while i < n:
        chunk = palabras[i:i+tam]
        chunks.append(" ".join(chunk))
        i += tam - salto  # solapamiento
    return chunks
