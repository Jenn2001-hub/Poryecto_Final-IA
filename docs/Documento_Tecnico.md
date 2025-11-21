# Documento Técnico – Asistente Multiagente de Búsqueda de Apuntes

## 1. Introducción

Este proyecto presenta el desarrollo de un **asistente inteligente** capaz de realizar búsquedas semánticas dentro de apuntes y documentos utilizando un enfoque moderno de **Inteligencia Artificial**.  
El sistema implementa **extracción de texto**, **procesamiento OCR**, **chunking**, **embeddings**, **búsqueda vectorial**, y una **arquitectura multiagente** coordinada mediante LangChain.  
Además, integra un modelo generativo (Gemini) para producir respuestas contextualizadas basadas en la información recuperada.

Este proyecto fue desarrollado como trabajo final para la asignatura **Introducción a la Inteligencia Artificial**, dentro del programa **Tecnología en Desarrollo de Software**.

**Objetivo General:**  
Desarrollar un sistema RAG completo que permita realizar búsquedas en lenguaje natural dentro de apuntes personales, utilizando técnicas de IA modernas y una arquitectura de agentes.

---

## 2. Problema a Resolver

Los estudiantes suelen manejar grandes cantidades de apuntes distribuidos en múltiples formatos: PDF, TXT e imágenes (fotos de tablero).  
Buscar una definición, concepto o explicación se vuelve lento e ineficiente.

### Problemas del enfoque tradicional:
- La búsqueda por palabras clave **no entiende significados ni sinónimos**.
- Explorar manualmente documentos largos **consume tiempo**.
- Los apuntes en imágenes **no pueden buscarse** si no se aplica OCR.
- No existe una forma integrada de **preguntar en lenguaje natural**.

### Solución Propuesta

Desarrollar un **asistente RAG multiagente** capaz de:

1. Extraer texto desde PDF, TXT e imágenes con OCR.  
2. Dividir el contenido en fragments (chunks) con solapamiento.  
3. Generar embeddings semánticos con modelos sentence-transformers.  
4. Guardarlos en una base vectorial persistente.  
5. Recuperar los fragmentos más relevantes por similitud de coseno.  
6. Generar una respuesta coherente usando **Google Gemini**.  
7. Orquestar todo el flujo mediante un sistema **multiagente con LangChain**.

---

## 3. Metodología

El sistema sigue el pipeline típico de un sistema **RAG**:

Documentos → Extracción → Chunking → Embeddings → VectorStore
↓
Búsqueda
↓
Agente de Respuesta
↓
Respuesta final


### 3.1 Extracción de Datos  
**Archivo:** `src/agentes/agente_extraccion.py`

- Lee documentos `.pdf` con PyPDF2.  
- Lee archivos `.txt` directamente.  
- Procesa imágenes (`.png`, `.jpg`, `.jpeg`) mediante **pytesseract**.  
- Normaliza saltos de línea y caracteres especiales.  
- Devuelve un texto limpio y unificado por archivo.

### 3.2 Chunking  
**Archivo:** `src/core/chunking.py`

- Divide cada documento en fragmentos de ~300 palabras.  
- Usa un overlap de 50 palabras para mantener continuidad semántica.  
- Cada chunk contiene:
  - texto  
  - id del chunk  
  - ruta del documento origen

### 3.3 Generación de Embeddings  
**Archivo:** `src/core/embeddings.py`

Modelo utilizado:

- `all-MiniLM-L6-v2` (sentence-transformers)
- 384 dimensiones
- basado en transformers
- rápido y eficiente en CPU

Cada chunk se convierte en un vector numérico que captura su significado.

### 3.4 VectorStore  
**Archivo:** `src/core/vector_store.py`

Características:

- Almacena embeddings como listas normalizadas.  
- Permite realizar búsquedas mediante **cosine_similarity**.  
- Guarda y carga el índice automáticamente:
data/vector_store.pkl

- Escala bien para cientos o miles de chunks.

### 3.5 Agente de Análisis  
**Archivo:** `src/agentes/agente_analisis.py`

Responsabilidades:

- Coordinar chunking + embeddings.  
- Agregar los vectores al VectorStore.  
- Cargar el índice existente o crear uno nuevo.  
- Realizar búsquedas vectoriales top-k.

### 3.6 Agente de Respuesta  
**Archivo:** `src/agentes/agente_respuesta.py`

- Recibe la pregunta y los fragmentos recuperados.  
- Construye un prompt estructurado:  
- Contexto (chunks relevantes)  
- Instrucciones  
- Pregunta del usuario  
- Utiliza **Google Gemini** para generar una respuesta.  
- Si no hay API key, muestra los fragmentos relevantes (modo fallback).

### 3.7 Orquestador LangChain  
**Archivo:** `src/langchain_orquestador.py`

- Implementa Tools:
- **SearchTool** (búsqueda vectorial)
- **AnswerTool** (respuesta con LLM)
- Simplifica:
- `indexar()`  
- `consultar(pregunta)`  
- Coordina los agentes como una única interfaz.

---
## 4. Arquitectura de Agentes

El sistema se divide en tres agentes principales:

| Agente     | Función               | Entrada              | Salida    |
|------------|-----------------------|----------------------|-----------|
| Extracción | Extrae y limpia texto | Archivos PDF/TXT/IMG | Texto  |
| Análisis   | Chunking, embeddings, vector store | Texto | Vectores + búsqueda |
| Respuesta  | Genera respuesta final| Pregunta + fragmentos| Respuesta generada |

### Flujo Completo
Usuario → Pregunta
→ Agente de Análisis → Fragmentos relevantes
→ Agente de Respuesta → Gemini → Respuesta final


---

## 5. Tecnologías y Herramientas

| Componente | Tecnología | Razón |
|------------|------------|--------|
| Extracción PDF | PyPDF2 | Ligero y funcional |
| OCR | Tesseract + pytesseract | Extrae texto de imágenes |
| Embeddings | sentence-transformers | Alta precisión y velocidad |
| DL Backend | PyTorch | Requerido por embeddings |
| Búsqueda | scikit-learn | cosine_similarity |
| UI Web | Streamlit | Sencillo y rápido |
| Orquestación | LangChain | Multiagencia y Tools |
| LLM | Google Gemini | Respuestas precisas |

---

## 6. Resultados y Conclusiones

### 6.1 Resultados Obtenidos

- Se logró indexar documentos PDF, TXT e imágenes.  
- El sistema genera respuestas contextualizadas y coherentes.  
- La búsqueda semántica funciona con alta precisión.  
- La interfaz CLI y la web permiten interacción fluida.  
- El índice vectorial persiste automáticamente.

### 6.2 Conclusiones

- Los sistemas RAG permiten búsquedas inteligentes mucho mejores que la búsqueda por palabras clave.  
- La arquitectura multiagente facilita mantenimiento y escalabilidad.  
- Gemini mejora significativamente la calidad de las respuestas.  
- El uso de embeddings pequeños como MiniLM es ideal para estudiantes.

### 6.3 Limitaciones

- Dependencia de API externa (Gemini).  
- OCR depende de la calidad de las imágenes.  
- La base vectorial simple no está optimizada para millones de vectores.

---

## 7. Trabajo Futuro

- Integración con FAISS o Qdrant.  
- Implementación de LLMs locales (modo offline).  
- Agente adicional de análisis semántico.  
- Sistema de resumen automático.  
- Historial de conversación.  
- Panel visual de chunks, embeddings y vector store.

---

## 8. Referencias

- Sentence-BERT: https://arxiv.org/abs/1908.10084  
- LangChain: https://python.langchain.com/  
- Google Gemini: https://ai.google.dev  
- RAG Architecture: https://arxiv.org/abs/2005.11401  
- Tesseract OCR: https://github.com/tesseract-ocr/tesseract  

---

**Documento Técnico – Proyecto Final (Noviembre 2025)**  
**Programa:** Tecnología en Desarrollo de Software  

