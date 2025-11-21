# Crear entorno virtual
py -m venv venv

# Activar entorno (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# Si aparece error de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# Luego vuelve a activar
.\venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

copy .env.example .env

# Si hay errores al instalar los requirements, borrar la carpeta venv y volver a crear el entorno virtual

# Desde la carpeta del proyecto
Remove-Item -Recurse -Force .\venv

python run_app.py

# Para ejecutar Streamlit
# 1. Estar en la caroeta raiz y ejecutar:

$env:PYTHONPATH = (Get-Location).Path
python -m streamlit run src/streamlit_app.py
# o
$env:PYTHONPATH = (Get-Location).Path; streamlit run src/streamlit_app.py
