# Tutorial y Manual de Usuario del Pipeline de Procesamiento de Documentos

## 1. Propósito del Proyecto

Este pipeline es un sistema automatizado para procesar grandes volúmenes de documentos. Su principal objetivo es extraer texto e imágenes, generar descripciones de las imágenes mediante un modelo de IA (a través de Ollama), y ensamblar los resultados en archivos Markdown bien estructurados.

El sistema está diseñado para ser:
- **Robusto y Resiliente:** Maneja errores y permite la reanudación de trabajos interrumpidos.
- **Modular:** El código está separado en componentes lógicos, facilitando su mantenimiento y extensión.
- **Flexible:** Puede procesar tanto directorios simples de documentos como corpus complejos con estructuras de carpetas anidadas.

## 2. Instalación del Entorno

El pipeline requiere Python y una serie de librerías específicas. La forma más limpia de instalar estas dependencias es usando un entorno virtual.

### Prerrequisitos

- **Python 3.10+**
- **pip** (el gestor de paquetes de Python)
- **Ollama** instalado y en ejecución, con un modelo multimodal descargado (ej. `ollama pull qwen2.5vl:7b`).

### Pasos de Instalación

1.  **Clonar o descargar el repositorio:** Asegúrate de tener todos los archivos del proyecto (`main_corpus.py`, `requirements.txt`, etc.) en una carpeta.

2.  **Crear un Entorno Virtual:**
    Navega a la carpeta del proyecto en tu terminal y ejecuta:
    ```bash
    python -m venv venv
    ```
    Esto creará una carpeta `venv` que contendrá todas las librerías del proyecto, aislándolas del resto de tu sistema.

3.  **Activar el Entorno Virtual:**
    - En **Linux/macOS**:
      ```bash
      source venv/bin/activate
      ```
    - En **Windows**:
      ```bash
      .\venv\Scripts\activate
      ```
    Sabrás que el entorno está activo porque tu prompt de la terminal cambiará para mostrar `(venv)`.

4.  **Instalar las Dependencias:**
    Con el entorno activo, instala todas las librerías necesarias con un solo comando:
    ```bash
    pip install -r requirements.txt
    ```
    Este comando leerá el archivo `requirements.txt` e instalará las versiones exactas de las librerías que se usaron para desarrollar y probar el pipeline, garantizando la compatibilidad.

¡La instalación está completa! Ahora estás listo para usar las herramientas del pipeline.

## 3. Manual de Uso

El pipeline ofrece varios scripts, cada uno con un propósito específico. Todos deben ser ejecutados desde la raíz del proyecto, con el entorno virtual activado.

### 3.1. `main_corpus.py` (Procesamiento Inicial)

- **Propósito:** Realizar el primer procesamiento de un corpus complejo estructurado en carpetas.
- **Uso:**
  ```bash
  python pipeline_documentos/main_corpus.py <ruta_al_directorio_del_corpus>
  ```
- **Ejemplo:**
  ```bash
  python pipeline_documentos/main_corpus.py /ruta/a/corpus_nahuatl
  ```
- **Funcionamiento:**
  - Creará un nuevo directorio de trabajo (ej. `corpus_nahuatl_processed_01`).
  - Identificará la mejor fuente de texto e imágenes para cada obra.
  - Extraerá los artefactos, optimizará las imágenes, generará las descripciones y ensamblará los archivos Markdown finales.

### 3.2. `resume_pipeline.py` (Reanudar Trabajo)

- **Propósito:** Continuar un trabajo de procesamiento que fue interrumpido o que necesita procesar obras nuevas añadidas al corpus original.
- **Uso:**
  ```bash
  python pipeline_documentos/resume_pipeline.py <ruta_corpus_original> <ruta_trabajo_existente>
  ```
- **Ejemplo:**
  ```bash
  python pipeline_documentos/resume_pipeline.py /ruta/a/corpus_nahuatl /ruta/a/corpus_nahuatl_processed_01
  ```
- **Funcionamiento:**
  - Escaneará el corpus original y lo comparará con los resultados en el directorio de trabajo.
  - Omitirá las obras que ya tienen un Markdown final.
  - Procesará únicamente las obras nuevas o faltantes.

### 3.3. `repair_missing_text.py` (Reparar Texto Faltante)

- **Propósito:** Reparar obras cuyo Markdown final se generó sin texto debido a un error previo en la extracción.
- **Uso:**
  ```bash
  python pipeline_documentos/repair_missing_text.py <ruta_corpus_original> <ruta_trabajo_existente> <IDs_obras>
  ```
- **Ejemplo (para reparar obras 1 y 2):**
  ```bash
  python pipeline_documentos/repair_missing_text.py /ruta/a/corpus_nahuatl /ruta/a/corpus_nahuatl_processed_01 1,2
  ```
- **Funcionamiento:**
  - No toca las imágenes ni las descripciones existentes.
  - Re-extrae únicamente el texto para las obras especificadas.
  - Re-ensambla el archivo Markdown final, combinando el nuevo texto con las descripciones existentes.

### 3.4. `retry_descriptions.py` (Reintentar Descripciones)

- **Propósito:** Encontrar y reintentar la generación de descripciones de imágenes que fallaron previamente (ej. por errores de red o de la API).
- **Uso:**
  ```bash
  python pipeline_documentos/retry_descriptions.py <ruta_trabajo_existente>
  ```
- **Ejemplo:**
  ```bash
  python pipeline_documentos/retry_descriptions.py /ruta/a/corpus_nahuatl_processed_01
  ```
- **Funcionamiento:**
  - Escanea los archivos `metadatos.json` de todas las obras en el directorio de trabajo.
  - Busca descripciones que contengan mensajes de error.
  - Si encuentra alguna, vuelve a llamar a la API de Ollama solo para esas imágenes.
  - Si obtiene nuevas descripciones, re-ensambla el Markdown final de la obra correspondiente.

