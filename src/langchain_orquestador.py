from typing import List, Optional, Any
import json

from langchain.tools import BaseTool

from src.agentes.agente_extraccion import AgenteExtraccion
from src.agentes.agente_analisis import AgenteAnalisis
from src.agentes.agente_respuesta import AgenteRespuesta


# En algunas versiones de LangChain `BaseTool` es una clase abstracta
# que exige implementar `_run`. Para mantener compatibilidad y evitar
# dependencias concretas de la versión, definimos una herramienta
# mínima con `run()` que envuelve una función Python.
class SimpleTool:
    def __init__(self, name: str, description: str, func):
        self.name = name
        self.description = description
        self._func = func

    def run(self, *args, **kwargs):
        # Compatibilidad: si se pasa un único dict con keys, lo desempaquetamos
        if len(args) == 1 and isinstance(args[0], dict):
            payload = args[0]
            # Caso común: {'query': ..., 'top_k': ...}
            if 'query' in payload:
                return self._func(payload.get('query'), payload.get('top_k', 4))
            # Caso: payload ya tiene los parámetros esperados
            return self._func(**payload)

        # Si se pasa una cadena o args normales, los delegamos
        if args and not kwargs:
            # si la función espera (query, top_k)
            try:
                return self._func(*args)
            except TypeError:
                return self._func(args[0])

        return self._func(**kwargs)



def create_search_tool(analisis: AgenteAnalisis) -> BaseTool:
    """Crea una herramienta de búsqueda para LangChain."""
    def _search(query: str, top_k: int = 4) -> str:
        frags = analisis.buscar_similares(query, top_k=top_k)
        return json.dumps(frags, ensure_ascii=False)

    return SimpleTool(
        name="search_documents",
        description="Busca fragmentos relevantes para una consulta y devuelve una lista JSON con metadatos y texto.",
        func=_search,
    )

def create_answer_tool(respuesta_agent: AgenteRespuesta) -> BaseTool:
    """Crea una herramienta de respuesta para LangChain."""
    def _answer(payload_json: str) -> str:
        try:
            payload = json.loads(payload_json)
            pregunta = payload.get('pregunta', '')
            fragmentos = payload.get('fragmentos', [])
            return respuesta_agent.generar_respuesta(pregunta, fragmentos)
        except Exception as e:
            return f"Error al procesar la solicitud: {str(e)}"

    return SimpleTool(
        name="generate_answer",
        description="Genera una respuesta basada en la pregunta y fragmentos (recibe JSON con 'pregunta' y 'fragmentos').",
        func=_answer,
    )

class LangChainOrquestador:
    """Orquestador mínimo que expone Tools y usa los agentes existentes."""

    def __init__(self, data_dir: str, modelo_name: str = "all-MiniLM-L6-v2", api_key: Optional[str] = None):
        self.data_dir = data_dir
        self.modelo_name = modelo_name
        self.api_key = api_key

        self.extractor = AgenteExtraccion(self.data_dir)
        self.analisis = AgenteAnalisis(modelo_name=self.modelo_name)
        self.respuesta_agent = None

        # Tools se inicializarán tras indexar / configurar la API key
        self.search_tool: Optional[BaseTool] = None
        self.answer_tool: Optional[BaseTool] = None

    def indexar(self, tam_chunk: int = 300) -> List[dict]:
        """Procesa la carpeta de datos, crea chunks y construye el índice."""
        # Extraer y procesar documentos
        # AgenteExtraccion expone `procesar()`; llamamos a ese método.
        chunks_meta = self.extractor.procesar(tam_chunk)
        
        # Construir índice de embeddings (AgenteAnalisis expone `indexar_chunks`)
        self.analisis.indexar_chunks(chunks_meta)
        
        # Inicializar el agente de respuesta si hay una API key
        if self.api_key:
            self.respuesta_agent = AgenteRespuesta(api_key=self.api_key)
        
        # Crear herramientas
        self.search_tool = create_search_tool(self.analisis)
        if self.respuesta_agent:
            self.answer_tool = create_answer_tool(self.respuesta_agent)
        
        return chunks_meta

    def consultar(self, pregunta: str, top_k: int = 4) -> str:
        """Ejecuta el flujo: buscar fragmentos (SearchTool) -> generar respuesta (AnswerTool)."""
        if self.search_tool is None:
            return "Error: La herramienta de búsqueda no está inicializada. Ejecuta indexar() primero."

        # 1. Buscar fragmentos relevantes
        fragmentos_json = self.search_tool.run({"query": pregunta, "top_k": top_k})
        fragmentos = json.loads(fragmentos_json)

        # 2a. Si no hay agente de respuesta (sin API key), devolvemos los fragmentos encontrados
        if self.answer_tool is None:
            if not fragmentos:
                return "No encontré información relevante en los documentos indexados."
            # Construir una respuesta simple basada en los fragmentos
            partes = []
            for f in fragmentos:
                score = f.get("score", None)
                doc = f.get("documento", f.get("document", "unknown"))
                texto = f.get("texto", "")
                partes.append(f"- {doc} (score={score:.3f}): {texto[:300].strip()}")
            resumen = "\n".join(partes)
            return f"Resultados relevantes encontrados:\n{resumen}"

        # 2b. Si hay agente de respuesta, delegamos en él
        payload = {
            "pregunta": pregunta,
            "fragmentos": fragmentos
        }
        respuesta = self.answer_tool.run(json.dumps(payload))
        return respuesta

__all__ = ["LangChainOrquestador", "SearchTool", "AnswerTool"]
