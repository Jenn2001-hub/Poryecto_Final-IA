# Documentación del Sistema de Gestión de Apuntes con IA

## Descripción General

Este proyecto es un sistema de gestión de apuntes potenciado por IA que permite extraer, analizar y consultar información de diversos formatos de documentos. El sistema está compuesto por tres agentes principales que trabajan en conjunto para proporcionar respuestas precisas basadas en los documentos proporcionados.

## Estructura del Proyecto


## Componentes Principales

### 1. Agente de Extracción ([agente_extraccion.py](cci:7://file:///c:/Users/PC/Desktop/Proyecto%20IA/proyecto-ia-apuntes/src/agentes/agente_extraccion.py:0:0-0:0))

**Responsabilidad**: Extraer texto de diferentes formatos de archivo.

- Soporta múltiples formatos: PDF, TXT, PNG, JPG/JPEG
- Utiliza PyPDF2 para archivos PDF
- Emplea Tesseract OCR para extraer texto de imágenes
- Divide el contenido en fragmentos manejables (chunks)

### 2. Agente de Análisis ([agente_analisis.py](cci:7://file:///c:/Users/PC/Desktop/Proyecto%20IA/proyecto-ia-apuntes/src/agentes/agente_analisis.py:0:0-0:0))

**Responsabilidad**: Procesa y analiza el texto extraído.

- Genera embeddings del texto usando modelos pre-entrenados
- Almacena y gestiona los vectores de los documentos
- Realiza búsquedas semánticas para encontrar información relevante
- Utiliza el modelo `all-MiniLM-L6-v2` por defecto para generar embeddings

### 3. Agente de Respuesta ([agente_respuesta.py](cci:7://file:///c:/Users/PC/Desktop/Proyecto%20IA/proyecto-ia-apuntes/src/agentes/agente_respuesta.py:0:0-0:0))

**Responsabilidad**: Genera respuestas a las consultas de los usuarios.

- Utiliza Google's Gemini para generar respuestas
- Combina la pregunta del usuario con los fragmentos relevantes
- Proporciona respuestas contextuales basadas en los documentos
- Incluye manejo de errores para preguntas fuera de contexto

### Módulos Core

#### [chunking.py](cci:7://file:///c:/Users/PC/Desktop/Proyecto%20IA/proyecto-ia-apuntes/src/core/chunking.py:0:0-0:0)
- Divide el texto en fragmentos más pequeños con solapamiento
- Limpia y normaliza el texto
- Permite configurar el tamaño de los chunks y el solapamiento

#### `embeddings.py`
- Maneja la generación de embeddings de texto
- Soporta diferentes modelos de embeddings
- Optimizado para procesamiento por lotes

#### `vector_store.py`
- Almacena y gestiona vectores de documentos
- Implementa búsqueda por similitud de coseno
- Soporta actualizaciones incrementales

## Flujo de Trabajo

1. **Carga de Documentos**:
   - Los documentos se colocan en la carpeta [data/](cci:7://file:///c:/Users/PC/Desktop/Proyecto%20IA/proyecto-ia-apuntes/data:0:0-0:0)
   - El Agente de Extracción procesa los archivos y extrae el texto

2. **Procesamiento**:
   - El texto se divide en chunks manejables
   - Se generan embeddings para cada chunk
   - Los vectores se almacenan en el VectorStore

3. **Consulta**:
   - El usuario realiza una pregunta
   - El sistema encuentra los chunks más relevantes
   - El Agente de Respuesta genera una respuesta basada en el contexto

## Requisitos del Sistema

- Python 3.8+
- Tesseract OCR instalado en el sistema
- API Key de Google AI (para Gemini)
- Dependencias listadas en [requirements.txt](cci:7://file:///c:/Users/PC/Desktop/Proyecto%20IA/proyecto-ia-apuntes/requirements.txt:0:0-0:0)

## Configuración

1. Copiar [.env.example](cci:7://file:///c:/Users/PC/Desktop/Proyecto%20IA/proyecto-ia-apuntes/.env.example:0:0-0:0) a [.env](cci:7://file:///c:/Users/PC/Desktop/Proyecto%20IA/proyecto-ia-apuntes/.env:0:0-0:0)
2. Configurar la variable `GOOGLE_API_KEY` con tu clave de API
3. Instalar dependencias: `pip install -r requirements.txt`

## Configuración y Uso

### Configuración de la API Key

1. **Configuración en PowerShell**:
   ```powershell
   # Establecer la variable de entorno
   $env:GOOGLE_API_KEY = "AIzaSyBEGvAqR1uvUipZCRSwuBoBLZ7_yG0UzlU"

   # Verificar que se configuró correctamente
   echo $env:GOOGLE_API_KEY

   # Navegar a la carpeta del proyecto (ajusta la ruta según sea necesario)
   cd "C:\Users\PC\Desktop\Proyecto IA\proyecto-ia-apuntes"