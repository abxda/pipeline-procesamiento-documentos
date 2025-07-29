# Arquitectura del Pipeline de Procesamiento de Documentos

## 1. Filosofía y Diseño General

Este proyecto está diseñado como un pipeline de procesamiento por lotes, modular y resiliente. La filosofía principal es la separación de responsabilidades y la creación de artefactos intermedios. Esto significa que cada paso del proceso (extracción, optimización, descripción) es un módulo independiente que crea o modifica archivos específicos en una estructura de directorios predecible.

Esta arquitectura permite:
- **Reanudación:** Si el proceso falla, puede ser reanudado sin tener que empezar desde cero.
- **Reparación:** Pasos específicos pueden ser re-ejecutados sobre los artefactos para corregir errores sin afectar el resto del pipeline.
- **Mantenibilidad:** Cada módulo tiene una única responsabilidad, haciendo que el código sea más fácil de entender, depurar y extender.
- **Trazabilidad:** La estructura de directorios y los logs proporcionan un rastro claro de lo que ha ocurrido en cada ejecución.

## 2. Estructura de Directorios de Salida

Por cada ejecución, el pipeline crea un directorio de trabajo principal (ej. `corpus_nahuatl_processed_01`) que contiene la siguiente estructura:

- **`00_log/`**: Contiene los archivos de log detallados de la ejecución.
- **`01_documentos_originales/`**: (Opcional, usado por `main.py`) Una copia de los documentos originales que se están procesando.
- **`02_artefactos_extraidos/`**: El corazón del pipeline. Contiene una subcarpeta por cada obra procesada.
  - **`{id_de_la_obra}/`**:
    - **`imagenes_originales/`**: Imágenes extraídas de los documentos en su calidad original.
    - **`imagenes_optimizadas/`**: Versiones redimensionadas de las imágenes, listas para ser enviadas a la IA.
    - **`tablas_extraidas/`**: (Reservado para futuro uso) Contendrá tablas extraídas en formato CSV.
    - **`metadatos.json`**: Un archivo crucial que guarda toda la información sobre la obra: rutas a los archivos, descripciones de imágenes, etc.
    - **`texto_extraido.txt`**: El contenido de texto completo de la obra, extraído por Docling.
- **`03_markdown_final/`**: Contiene los archivos `.md` finales, un producto ensamblado de los artefactos.

## 3. Componentes de Software (Archivos Python)

A continuación se detalla cada archivo `.py` del proyecto.

### 3.1. Archivos de Configuración y Orquestadores

#### `config.py`
- **Propósito:** Centraliza toda la configuración global del pipeline.
- **Funciones Principales:**
  - Define los parámetros de conexión a la API de Ollama (`OLLAMA_CONFIG`).
  - Establece las configuraciones para el procesamiento de imágenes (`IMAGE_PROCESSING_CONFIG`).
  - Almacena los prompts que se envían a la IA (`PROMPTS`).
  - Define la estructura de nombres para los directorios de salida y los artefactos (`OUTPUT_DIRS`, `ARTIFACT_SUBDIRS`).
  - Configura los parámetros del sistema de logging (`LOG_CONFIG`).

#### `main.py` (Orquestador Genérico - Obsoleto)
- **Propósito:** Fue el primer orquestador, diseñado para procesar un directorio simple de documentos. Ha sido reemplazado en gran medida por `main_corpus.py`.
- **Flujo de Trabajo:** Itera sobre archivos individuales en una carpeta, los procesa uno por uno y genera los artefactos y el Markdown final.

#### `main_corpus.py` (Orquestador Principal)
- **Propósito:** Es el punto de entrada principal para procesar un corpus complejo con una estructura de directorios anidada.
- **Funciones Principales:**
  - `main(corpus_directory)`: Itera sobre las carpetas de las obras en el directorio del corpus. Llama a `utils_fs.find_best_sources` para determinar qué archivos procesar y luego orquesta la ejecución de los módulos de procesamiento en secuencia.

### 3.2. Scripts de Utilidad y Mantenimiento

#### `resume_pipeline.py`
- **Propósito:** Reanudar un trabajo de procesamiento interrumpido o procesar obras nuevas añadidas a un corpus ya procesado.
- **Funciones Principales:**
  - `main(corpus_dir, existing_work_dir)`: Compara el corpus original con un directorio de trabajo existente. Si un archivo Markdown final ya existe para una obra, la omite. De lo contrario, ejecuta el pipeline completo para esa obra faltante.

#### `repair_missing_text.py`
- **Propósito:** Realizar una reparación "quirúrgica" en obras cuyo texto no se extrajo correctamente en una ejecución anterior.
- **Funciones Principales:**
  - `main(corpus_dir, work_dir, obra_ids)`: Para una lista de IDs de obras específicas, re-ejecuta únicamente la extracción de texto y el re-ensamblaje del Markdown, preservando las imágenes y descripciones existentes.

#### `retry_descriptions.py`
- **Propósito:** Reintentar la generación de descripciones de imágenes que fallaron en ejecuciones anteriores.
- **Funciones Principales:**
  - `main(work_dir)`: Escanea los archivos `metadatos.json` en un directorio de trabajo. Si encuentra una descripción que contiene un mensaje de error, llama a `generador_descripciones.py` con un indicador de `force_retry` para volver a procesar solo esas imágenes.

### 3.3. Módulos del Pipeline (`modulos/`)

#### `modulos/utils_fs.py`
- **Propósito:** Contiene funciones de ayuda para interactuar con el sistema de archivos y configurar el logging.
- **Funciones Principales:**
  - `setup_logging()`: Configura el sistema de logging para la ejecución.
  - `setup_main_output_dir()`: Crea la estructura de directorios de salida para una nueva ejecución.
  - `find_best_sources()`: Lógica clave que inspecciona una carpeta de obra y determina la mejor fuente para texto e imágenes, manejando tanto estructuras simples como complejas.

#### `modulos/procesador_documentos.py`
- **Propósito:** Interactuar con la librería `docling` para extraer el contenido de los documentos.
- **Funciones Principales:**
  - `extract_artifacts_from_corpus()`: Orquesta la extracción. Configura `docling` y procesa una lista de archivos de texto e imágenes, agregando los resultados.
  - `regenerate_text_artifact()`: Una función especializada, usada por el script de reparación, que solo re-extrae el texto de una obra.

#### `modulos/procesador_imagenes.py`
- **Propósito:** Manejar la optimización de imágenes.
- **Funciones Principales:**
  - `optimize_images_for_doc()`: Itera sobre las imágenes en la carpeta `imagenes_originales`, las redimensiona usando la librería Pillow, y guarda el resultado en `imagenes_optimizadas`. Actualiza el `metadatos.json` con la ruta a la nueva imagen.

#### `modulos/generador_descripciones.py`
- **Propósito:** Interactuar con la API de Ollama para generar descripciones de imágenes.
- **Funciones Principales:**
  - `generate_descriptions_for_doc()`: Itera sobre las imágenes que necesitan una descripción. Envía cada imagen optimizada a la API de Ollama y guarda la descripción resultante en el `metadatos.json`. Implementa un guardado incremental para ser resiliente a fallos.

#### `modulos/ensamblador_markdown.py`
- **Propósito:** Construir el archivo Markdown final.
- **Funciones Principales:**
  - `assemble_markdown_for_doc()`: Lee el `texto_extraido.txt` y el `metadatos.json`. Reemplaza los placeholders de imagen en el texto con el código Markdown correspondiente que incluye la imagen y su descripción, creando el archivo `.md` final.
