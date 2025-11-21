# src/core/embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class EmbeddingModel:
    def __init__(self, modelo_name: str = "all-MiniLM-L6-v2"):
        self.modelo_name = modelo_name
        self.model = SentenceTransformer(modelo_name)

    def embedir(self, textos: List[str]) -> np.ndarray:
        """
        Retorna un array numpy de shape (n_textos, dimension).
        Los embeddings se normalizan internamente a L2 en VectorStore.agregar() para optimizar similitud de coseno.
        """
        embs = self.model.encode(textos, show_progress_bar=True, convert_to_numpy=True)
        return np.array(embs, dtype=np.float32)
