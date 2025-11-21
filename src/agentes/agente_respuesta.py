# src/agentes/agente_respuesta.py
from typing import List, Optional
import os
import google.generativeai as genai

class AgenteRespuesta:
    """
    Usa Google's Gemini para generar respuestas basadas en fragmentos de texto.
    Requiere que tengas GOOGLE_API_KEY en el entorno o la pases como parámetro.
    """
    def __init__(self, api_key: Optional[str] = None, temperatura: float = 0.2):
        """Inicializa el modelo Gemini."""
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Se requiere una API key de Google. Configura GOOGLE_API_KEY en .env o pásala como argumento.")
        
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        
        # Listar modelos disponibles
        try:
            models = genai.list_models()
            print("\nModelos disponibles:")
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
            
            # Usar un modelo disponible (gemini-2.5-flash según la lista mostrada)
            model_name = "gemini-2.5-flash"
            print(f"\nUsando el modelo: {model_name}")
            self.model = genai.GenerativeModel(model_name)
            self.generation_config = {
                'temperature': temperatura,
                'max_output_tokens': 2000,
            }
        except Exception as e:
            print(f"\nError al configurar el modelo: {str(e)}")
            print("\nAsegúrate de que tu API key sea válida y tenga acceso a los modelos de Gemini.")
            print("Puedes verificar tu clave aquí: https://aistudio.google.com/app/apikey")
            raise

    def _formatear_contexto(self, fragmentos: List[dict]) -> str:
        """Formatea los fragmentos en un solo string de contexto."""
        return "\n\n".join(
            f"[Documento: {f['documento']} - Chunk {f['chunk_id']}]\n{f['texto']}" 
            for f in fragmentos
        )

    def generar_respuesta(self, pregunta: str, fragmentos: List[dict]) -> str:
        """
        Genera una respuesta usando el modelo Gemini basado en los fragmentos proporcionados.
        
        Args:
            pregunta: La pregunta del usuario
            fragmentos: Lista de fragmentos relevantes
            
        Returns:
            str: La respuesta generada
        """
        contexto = self._formatear_contexto(fragmentos)
        
        prompt = f"""Eres un asistente útil que responde preguntas basándose en el contexto proporcionado.

INSTRUCCIONES:
1. Usa SOLO la información del contexto para responder.
2. Si la respuesta no está en el contexto, di honestamente "No encontré información sobre esto en los apuntes".
3. Mantén las respuestas concisas y en español.
4. Si hay múltiples fragmentos, integra la información de manera coherente.

CONTEXTO:
{contexto}

PREGUNTA: {pregunta}

RESPUESTA:"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            return response.text
        except Exception as e:
            return f"Error al generar la respuesta: {str(e)}"
