# src/agentes/agente_extraccion.py
import os
from typing import List, Dict
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

from src.core.chunking import crear_chunks

class AgenteExtraccion:
    """
    Lee archivos de la carpeta de apuntes y retorna una lista de chunks.
    Soporta .txt, .pdf, .png, .jpg
    """
    def __init__(self, carpeta: str):
        self.carpeta = carpeta

    def extraer_texto_archivo(self, ruta: str) -> str:
        ruta = os.path.abspath(ruta)
        if ruta.lower().endswith(".txt"):
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        if ruta.lower().endswith(".pdf"):
            reader = PdfReader(ruta)
            textos = []
            for p in reader.pages:
                t = p.extract_text() or ""
                textos.append(t)
            return "\n".join(textos)
        if ruta.lower().endswith((".png", ".jpg", ".jpeg")):
            # OCR (Tesseract) - requiere tesseract instalado en el sistema
            img = Image.open(ruta)
            return pytesseract.image_to_string(img, lang="eng+spa")
        return ""

    def procesar(self, tam_chunk:int = 300) -> List[Dict]:
        """
        Devuelve lista de dicts:
        { "documento": nombre, "chunk_id": i, "texto": chunk_text }
        """
        archivos = sorted(os.listdir(self.carpeta))
        todos_chunks = []
        for archivo in archivos:
            ruta = os.path.join(self.carpeta, archivo)
            if not os.path.isfile(ruta):
                continue
            texto = self.extraer_texto_archivo(ruta)
            if not texto or len(texto.strip()) == 0:
                continue
            chunks = crear_chunks(texto, tam= tam_chunk)
            for idx, ch in enumerate(chunks):
                todos_chunks.append({
                    "documento": archivo,
                    "chunk_id": idx,
                    "texto": ch
                })
        return todos_chunks
