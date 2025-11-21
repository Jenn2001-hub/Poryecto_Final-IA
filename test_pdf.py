try:
    from PyPDF2 import PdfReader
    print("¡PyPDF2 se importó correctamente!")
    print(f"Versión de PyPDF2: {PdfReader.__version__}")
except Exception as e:
    print(f"Error al importar PyPDF2: {e}")
