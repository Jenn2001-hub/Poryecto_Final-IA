import os
import sys

# Asegurarse de que el directorio raíz del proyecto esté en el PATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Ahora importamos la aplicación
from src.app import main

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", "-d", default="data/", help="Carpeta con apuntes")
    parser.add_argument("--chunk", type=int, default=300)
    parser.add_argument("--modelo", default="all-MiniLM-L6-v2")
    parser.add_argument("--api_key", default=None, help="OPENAI API KEY (si no está en env)")
    
    args = parser.parse_args()
    
    # Asegurarse de que la ruta de datos sea absoluta
    if not os.path.isabs(args.data):
        args.data = os.path.join(project_root, args.data)
    
    # Ejecutar la aplicación
    main()
