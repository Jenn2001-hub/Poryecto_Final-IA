# src/agentes/agente_analisis.py
from typing import List, Optional
import numpy as np
import os
from dotenv import load_dotenv
from src.core.embeddings import EmbeddingModel
from src.core.vector_store import VectorStore

load_dotenv()

class AgenteAnalisis:
    """
    Genera embeddings y administra el VectorStore con persistencia automática.
    Soporta guardar/cargar el índice desde VECTOR_STORE_PATH (.env).
    """
    def __init__(self, modelo_name: str = "all-MiniLM-L6-v2", vector_store_path: Optional[str] = None):
        self.embedder = EmbeddingModel(modelo_name)
        self.store = None
        
        # Leer VECTOR_STORE_PATH de .env si no se proporciona
        if vector_store_path is None:
            vector_store_path = os.getenv("VECTOR_STORE_PATH", "./data/vector_store.pkl")
        self.vector_store_path = vector_store_path

    def indexar_chunks(self, chunks_meta: List[dict]):
        """Indexa chunks y guarda automáticamente el VectorStore en VECTOR_STORE_PATH."""
        textos = [c["texto"] for c in chunks_meta]
        embs = self.embedder.embedir(textos)  # np.ndarray
        dim = embs.shape[1]
        self.store = VectorStore(dim)
        self.store.agregar(embs, chunks_meta)
        
        # Guardar automáticamente en VECTOR_STORE_PATH
        os.makedirs(os.path.dirname(self.vector_store_path) or ".", exist_ok=True)
        self.store.guardar(self.vector_store_path)
        print(f"[*] Índice guardado en: {self.vector_store_path}")
        return self.store

    def cargar_indice(self) -> bool:
        """Carga el VectorStore desde VECTOR_STORE_PATH si existe.
        
        Returns:
            True si se cargó exitosamente, False si el archivo no existe.
        """
        if os.path.exists(self.vector_store_path):
            try:
                self.store = VectorStore.cargar(self.vector_store_path)
                print(f"[*] Índice cargado desde: {self.vector_store_path}")
                return True
            except Exception as e:
                print(f"[!] Error al cargar índice: {e}")
                return False
        return False

    def buscar_similares(self, consulta: str, top_k: int = 3):
        """Busca fragmentos similares a la consulta.
        
        Si el store no existe, intenta cargar el índice guardado.
        """
        if self.store is None:
            if not self.cargar_indice():
                raise RuntimeError("No hay índice disponible. Indexa documentos primero.")
        
        consulta_emb = self.embedder.embedir([consulta])[0]
        resultados = self.store.buscar(consulta_emb, top_k)
        return resultados
