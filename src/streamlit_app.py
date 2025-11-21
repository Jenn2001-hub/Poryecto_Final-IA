# src/streamlit_app.py
import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from src.langchain_orquestador import LangChainOrquestador

load_dotenv()

# Configuración de la página
st.set_page_config(page_title="🧠 Asistente de Apuntes", layout="wide")
st.title("🧠 Asistente de Búsqueda de Apuntes")

# Sidebar para configuración
with st.sidebar:
    st.header("Configuración")
    
    # Configuración de la API Key
    api_key = st.text_input(
        "🔑 Google API Key",
        type="password",
        help="Obtén tu API key de Google AI Studio: https://aistudio.google.com/"
    )
    
    # Configuración de la carpeta de datos
    data_dir = st.text_input("📂 Carpeta con apuntes", value="data/apuntes/")
    
    # Configuración de los chunks
    tam_chunk = st.slider(
        "📏 Tamaño de los chunks (palabras)",
        min_value=100,
        max_value=1000,
        value=300,
        step=50,
        help="Tamaño de los fragmentos en que se dividirán los documentos"
    )
    
    # Modelo de embeddings
    modelo = st.selectbox(
        "🤖 Modelo de embeddings",
        ["all-MiniLM-L6-v2", "all-mpnet-base-v2"],
        help="Modelo para generar embeddings semánticos"
    )
    
    # Botón para indexar
    if st.button("🔄 Indexar apuntes", use_container_width=True):
        if not api_key:
            st.error("❌ Por favor, ingresa tu Google API Key")
            st.stop()
            
        if not os.path.exists(data_dir):
            st.error(f"❌ La carpeta {data_dir} no existe")
            st.stop()
            
        with st.spinner("🔍 Extrayendo, creando chunks e indexando con LangChain..."):
            try:
                # Crear orquestador con LangChain
                orchestrator = LangChainOrquestador(data_dir, modelo_name=modelo, api_key=api_key)
                chunks_meta = orchestrator.indexar(tam_chunk)
                
                if not chunks_meta:
                    st.warning("⚠️ No se encontraron documentos para indexar")
                    st.stop()
                
                with st.expander("📊 Estadísticas de indexación", expanded=False):
                    st.write(f"📄 Documentos procesados: {len(set(c['documento'] for c in chunks_meta))}")
                    st.write(f"🧩 Chunks creados: {len(chunks_meta)}")
                    
                    # Mostrar documentos indexados
                    docs = sorted(set(c['documento'] for c in chunks_meta))
                    st.write("📋 Documentos indexados:")
                    for doc in docs:
                        st.write(f"  - {doc}")
                
                # Guardar orquestador en sesión
                st.session_state["orchestrator"] = orchestrator
                st.success("✅ Indexado completado con LangChainOrquestador")
                
            except Exception as e:
                st.error(f"❌ Error al indexar: {str(e)}")
                st.exception(e)  # Muestra el traceback completo

# Área principal de búsqueda
st.header("🔍 Buscar en los apuntes")

# Mostrar estado actual
if "orchestrator" not in st.session_state:
    st.warning("⚠️ Por favor, indexa los apuntes primero usando el panel lateral")
    st.stop()

# Campo de búsqueda
pregunta = st.text_input(
    "Escribe tu pregunta:",
    placeholder="Ej: ¿Qué son las redes neuronales?",
    help="Escribe tu pregunta sobre el contenido de los apuntes"
)

# Botón de búsqueda
if st.button("🔍 Buscar", type="primary") and pregunta:
    with st.spinner("🤔 Procesando tu pregunta con LangChainOrquestador..."):
        try:
            orchestrator = st.session_state.get("orchestrator")
            
            # Usar el orquestador para consultar
            respuesta = orchestrator.consultar(pregunta, top_k=4)
            
            # Mostrar respuesta
            with st.container():
                st.subheader("💡 Respuesta")
                st.markdown(f"{respuesta}")
            
            # Mostrar fragmentos usados (desde el store del orquestador)
            with st.expander("📚 Ver fragmentos usados", expanded=False):
                fragmentos = orchestrator.search_tool.run(pregunta, 4)
                import json
                fragmentos_list = json.loads(fragmentos)
                for f in fragmentos_list:
                    st.markdown(f"### 📄 {f['documento']} (Chunk {f['chunk_id'] + 1})")
                    st.markdown(f"```\n{f['texto']}\n```")
                    st.write(f"Similitud: {f['score']:.2%}")
                    st.write("---")
                    
        except Exception as e:
            st.error(f"❌ Error al buscar: {str(e)}")

# Footer
st.markdown("---")
st.caption("🧠 Asistente de Apuntes - Procesamiento de lenguaje natural con Gemini")
