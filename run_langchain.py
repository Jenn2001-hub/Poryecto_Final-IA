"""Script de entrada mínimo para demostrar la orquestación con LangChain.

Ejemplo de uso (PowerShell):
    python run_langchain.py --data data/apuntes/ --chunk 300 --modelo all-MiniLM-L6-v2

Luego escribe preguntas en modo interactivo.
"""
import argparse
from src.langchain_orquestador import LangChainOrquestador


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", "-d", default="data/apuntes/", help="Carpeta con apuntes")
    parser.add_argument("--chunk", type=int, default=300)
    parser.add_argument("--modelo", default="all-MiniLM-L6-v2")
    parser.add_argument("--api_key", default=None, help="GOOGLE API KEY (si no está en env)")
    args = parser.parse_args()

    orchestrator = LangChainOrquestador(args.data, modelo_name=args.modelo, api_key=args.api_key)
    print("[*] Indexando documentos...")
    chunks = orchestrator.indexar(tam_chunk=args.chunk)
    print(f"[*] Chunks creados: {len(chunks)}")

    print("Modo interactivo (escribe 'salir' para terminar)")
    while True:
        q = input("Pregunta> ").strip()
        if q.lower() in ["salir", "exit", "quit"]:
            break
        try:
            out = orchestrator.consultar(q, top_k=4)
            print("\n--- RESPUESTA ---")
            print(out)
            print("-----------------\n")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
