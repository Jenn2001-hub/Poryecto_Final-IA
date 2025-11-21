# src/core/vector_store.py
import numpy as np
from typing import List, Dict, Any, Optional
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

class VectorStore:
    """
    Almacén de vectores que permite guardar y buscar vectores usando similitud de coseno.
    Utiliza scikit-learn para cálculos de similitud.
    """
    
    def __init__(self, dim: int):
        """
        Inicializa el almacén de vectores.
        
        Args:
            dim: Dimensión de los vectores a almacenar
        """
        self.dim = dim
        self.embeddings = []  # Lista de vectores de embeddings
        self.metadatos = []   # Lista de metadatos correspondientes

    def agregar(self, embs: np.ndarray, metas: List[Dict[str, Any]]) -> None:
        """
        Añade nuevos embeddings y sus metadatos al almacén.
        Los embeddings se normalizan a L2 para optimizar búsquedas de similitud de coseno.
        
        Args:
            embs: Array de numpy con los embeddings (n, dim)
            metas: Lista de diccionarios con metadatos para cada embedding
            
        Raises:
            ValueError: Si el número de embeddings no coincide con el de metadatos
        """
        if len(embs) != len(metas):
            raise ValueError("El número de embeddings debe coincidir con el de metadatos")
        
        # Normalizar embeddings a L2 para optimizar similitud de coseno
        embs_normalized = normalize(embs, norm='l2')
        self.embeddings.extend(embs_normalized.tolist())
        self.metadatos.extend(metas)

    def buscar(self, consulta_emb: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Busca los top_k elementos más similares a la consulta.
        
        Args:
            consulta_emb: Vector de consulta (dim,)
            top_k: Número de resultados a devolver
            
        Returns:
            Lista de diccionarios con los metadatos de los resultados más similares,
            ordenados por similitud (de mayor a menor). Cada diccionario incluye
            una clave 'score' con la puntuación de similitud.
        """
        if not self.embeddings:
            return []
            
        # Convertir a array de numpy
        embeddings_array = np.array(self.embeddings, dtype=np.float32)
        consulta_array = np.array(consulta_emb, dtype=np.float32).reshape(1, -1)
        
        # Calcular similitud de coseno
        similitudes = cosine_similarity(consulta_array, embeddings_array)[0]
        
        # Obtener los índices de los top_k más similares
        indices = np.argpartition(similitudes, -top_k)[-top_k:]
        
        # Ordenar por similitud (de mayor a menor)
        indices = indices[np.argsort(-similitudes[indices])]
        
        # Devolver los metadatos de los más similares con su puntuación
        resultados = []
        for i in indices:
            resultado = self.metadatos[i].copy()
            resultado['score'] = float(similitudes[i])  # Añadir puntuación de similitud
            resultados.append(resultado)
            
        return resultados

    def guardar(self, ruta: str = "vector_store.pkl") -> None:
        """
        Guarda el almacén de vectores en un archivo.
        
        Args:
            ruta: Ruta del archivo donde guardar el almacén
        """
        with open(ruta, "wb") as f:
            pickle.dump({
                "embeddings": self.embeddings, 
                "metadatos": self.metadatos, 
                "dim": self.dim
            }, f)
            
    @classmethod
    def cargar(cls, ruta: str = "vector_store.pkl") -> 'VectorStore':
        """
        Carga un almacén de vectores desde un archivo.
        
        Args:
            ruta: Ruta del archivo a cargar
            
        Returns:
            Instancia de VectorStore cargada
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            pickle.UnpicklingError: Si hay un error al cargar el archivo
        """
        try:
            with open(ruta, "rb") as f:
                datos = pickle.load(f)
                
            vs = cls(datos["dim"])
            vs.embeddings = datos["embeddings"]
            vs.metadatos = datos["metadatos"]
            return vs
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f"No se encontró el archivo {ruta}") from e
        except Exception as e:
            raise ValueError(f"Error al cargar el archivo {ruta}: {str(e)}") from e
