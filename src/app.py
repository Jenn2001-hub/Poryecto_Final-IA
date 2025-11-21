# src/app.py
import os
import argparse
from dotenv import load_dotenv
from src.langchain_orquestador import LangChainOrquestador

# Cargar variables de entorno desde .env (si existe)
load_dotenv()


def construir_indice(data_dir: str, tam_chunk: int = 300, modelo: str = "all-MiniLM-L6-v2", api_key: str = None):
    """Construye el índice usando el `LangChainOrquestador` y devuelve el orquestador.

    El orquestador encapsula extracción, análisis e instancia el agente de respuesta.
    """
    orchestrator = LangChainOrquestador(data_dir, modelo_name=modelo, api_key=api_key)
    print("[*] Extrayendo, creando chunks e indexando con LangChainOrquestador...")
    chunks_meta = orchestrator.indexar(tam_chunk)
    print(f"[*] Chunks creados: {len(chunks_meta)}")
    return orchestrator


def modo_interactivo(orchestrator: LangChainOrquestador):
    print("\nModo interactivo. Escribe 'salir' para terminar.\n")
    while True:
        pregunta = input("Pregunta > ").strip()
        if pregunta.lower() in ["salir", "exit", "quit"]:
            break
        try:
            out = orchestrator.consultar(pregunta, top_k=4)
            print("\n--- RESPUESTA ---")
            print(out)
            print("-----------------\n")
        except Exception as e:
            print(f"Error al consultar: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", "-d", default="data/apuntes/", help="Carpeta con apuntes")
    parser.add_argument("--chunk", type=int, default=300)
    parser.add_argument("--modelo", default="all-MiniLM-L6-v2")
    parser.add_argument("--api_key", default=None, help="GOOGLE API KEY (si no está en env)")
    args = parser.parse_args()

    # Si no se pasó api_key por argumento, leer de las variables de entorno
    api_key = args.api_key or os.getenv("GOOGLE_API_KEY")

    orchestrator = construir_indice(args.data, tam_chunk=args.chunk, modelo=args.modelo, api_key=api_key)
    modo_interactivo(orchestrator)

if __name__ == "__main__":
    main()
