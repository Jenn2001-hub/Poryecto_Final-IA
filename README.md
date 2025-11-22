# Asistente Multiagente de Búsqueda de Apuntes  
**Proyecto Final – Introducción a la Inteligencia Artificial**

Este proyecto implementa un **asistente inteligente y moderno** que permite buscar información dentro de apuntes o documentos (PDF, TXT, imágenes) utilizando técnicas de **Inteligencia Artificial**, **embeddings semánticos**, **búsqueda vectorial**, **OCR** y **orquestación multiagente con LangChain**.  
El sistema aplica un enfoque **RAG (Retrieval-Augmented Generation)** para encontrar fragmentos relevantes y generar respuestas precisas mediante **Google Gemini**.

## Características principales

- ✅ Extracción inteligente de texto: **PDF, TXT, PNG, JPG/JPEG**
- ✅ **OCR integrado** con Tesseract para procesamiento de imágenes
- ✅ **Segmentación inteligente** con chunks y overlap
- ✅ **Embeddings semánticos** con `sentence-transformers` (`all-MiniLM-L6-v2`)
- ✅ Búsqueda por **similitud de coseno**
- ✅ **Base de datos vectorial** con persistencia automática (`vector_store.pkl`)
- ✅ **Orquestación con LangChain:** SearchTool + AnswerTool
- ✅ Respuestas con **Google Generative AI (Gemini)**
- ✅ Interfaz **CLI** e interfaz **web con Streamlit**

## Arquitectura

### 3 Agentes Principales

1. **Agente de Extracción** (`src/agentes/agente_extraccion.py`)
   - Lee PDF, TXT, imágenes con OCR  
   - Limpia y normaliza texto  

2. **Agente de Análisis** (`src/agentes/agente_analisis.py`)
   - Realiza chunking  
   - Genera embeddings semánticos  
   - Gestiona VectorStore con persistencia automática  

3. **Agente de Respuesta** (`src/agentes/agente_respuesta.py`)
   - Recupera fragmentos relevantes  
   - Construye el prompt contextual  
   - Genera respuestas con Gemini  

### Orquestación LangChain (`src/langchain_orquestador.py`)
- SearchTool + AnswerTool coordinados  
- Métodos principales: `indexar()` y `consultar()`  

## Instalación Rápida

```bash
# 1. Crear y activar entorno
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar .env
copy .env.example .env
# Editar .env: GOOGLE_API_KEY=tu_clave

# 4. (Opcional) Instalar Tesseract
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Ubuntu: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
```

## 🚀 Uso

### CLI Interactiva para pruebas rapidas
```bash
python run_langchain.py
# O: python run_langchain.py --data data/apuntes/ --api_key TU_CLAVE
```

### Interfaz Web (Streamlit)
```bash
streamlit run src/streamlit_app.py
# Abre http://localhost:8501
```

## Estructura

```
proyecto-ia-apuntes/
├── data/apuntes/                # Documentos (TXT, PDF, IMG)
├── data/vector_store.pkl        # Índice vectorial persistido
├── src/
│   ├── app.py                   # CLI principal
│   ├── streamlit_app.py         # UI web
│   ├── langchain_orquestador.py # Orquestador LangChain
│   ├── agentes/                 # Agentes del sistema
│   └── core/                    # Chunking, embeddings, vector store
├── docs/
│   └── Documento_Tecnico.md     # Documentación completa
├── .env.example
├── requirements.txt
└── run_langchain.py

```

## Datos de Ejemplo

Incluye 3 documentos en `data/apuntes/`:
- **introduccion_ia.txt** (~1200 palabras)
- **redes_neuronales.txt** (~1400 palabras)  
- **aprendizaje_automatico.txt** (~1200 palabras)

Para agregar más, copia archivos `.txt` o `.pdf` en `data/apuntes/`.

## Documentación Técnica
 Leer: docs/Documento_Tecnico.md

Incluye:
- Problema a resolver
- Metodología y flujo de datos
- Arquitectura de agentes
- Tecnologías y justificación
- Resultados y aprendizajes

## Configuración Avanzada

### Cambiar Modelo de Embeddings
```bash
python run_langchain.py --modelo all-mpnet-base-v2
```

### Ajustar Tamaño de Chunks
```bash
python run_langchain.py --chunk 200  # Chunks pequeños
python run_langchain.py --chunk 500  # Chunks grandes
```

### Variables de Entorno (.env)
```bash
GOOGLE_API_KEY=tu_clave_aquí
VECTOR_STORE_PATH=./data/vector_store.pkl
TESSERACT_CMD=/usr/bin/tesseract  # Opcional
```

## Solución de Problemas

**P: "No se encuentra GOOGLE_API_KEY"**  
R: Crea `.env` o pasa `--api_key TU_CLAVE`

**P: "Tesseract no encontrado"**  
R: Instala según tu SO (ver sección Instalación)

**P: "Respuestas genéricas"**  
R: Verifica documentos, reduce chunks, aumenta top_k

## Rendimiento

| Operación           | Tiempo     |
| ------------------- | ---------- |
| Indexación (50 ch)  | ~3–5 seg   |
| Búsqueda            | ~0.1–0.2 s |
| Generación (Gemini) | ~1–2 s     |
| Total consulta      | ~2–3 s     |


## Contribución
Las contribuciones son bienvenidas. Abre un issue primero.

## Licencia
Licencia MIT.

---

**Proyecto Final:** Introducción a la Inteligencia Artificial  
**Institución:** Universidad Tecnologica de Pereira
**Carrera:** Tecnología en Desarrollo de Software  
**Estudiantes:** Julián David Calderón, Juan José Betancourt, Jennifer Hincapie
**Noviembre 2025**
