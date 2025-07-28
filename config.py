# config.py
# Este archivo centraliza toda la configuración del pipeline de procesamiento de documentos.

import os

# --- Configuración del Modelo de Lenguaje (Ollama) ---
OLLAMA_CONFIG = {
    "MODEL_NAME": "qwen2.5vl:7b",
    "API_ENDPOINT_CHAT": "http://localhost:11434/api/chat",
    "API_ENDPOINT_GENERATE": "http://localhost:11434/api/generate",
    "REQUEST_TIMEOUT": 600,  # Segundos antes de considerar que la petición falló
}

# --- Configuración de Procesamiento de Imágenes ---
IMAGE_PROCESSING_CONFIG = {
    "MAX_DIMENSION": 1024,  # El lado más largo de la imagen se redimensionará a este valor
    "OPTIMIZED_FORMAT": "PNG",
}

# --- Prompts para la IA ---
PROMPTS = {
    "DESCRIBE_IMAGE_ES": "Describe esta imagen en detalle y en español. Explica su propósito y contenido dentro de un documento técnico.",
    # Aquí se pueden añadir más prompts en el futuro, ej. para extraer tablas o resumir texto.
}

# --- Estructura de Directorios de Salida ---
# Nombres de las carpetas que se crearán dentro del directorio de salida principal.
OUTPUT_DIRS = {
    "LOGS": "00_log",
    "ORIGINALS": "01_documentos_originales",
    "ARTIFACTS": "02_artefactos_extraidos",
    "FINAL_MARKDOWN": "03_markdown_final",
}

# --- Nombres de Subdirectorios de Artefactos ---
# Nombres para las carpetas dentro de cada directorio de documento específico.
ARTIFACT_SUBDIRS = {
    "TEXT": "texto_extraido.txt",
    "ORIGINAL_IMAGES": "imagenes_originales",
    "OPTIMIZED_IMAGES": "imagenes_optimizadas",
    "TABLES": "tablas_extraidas",
    "METADATA": "metadatos.json",
}

# --- Configuración del Log ---
LOG_CONFIG = {
    "FILENAME": "bitacora_procesamiento.log",
    "LEVEL": "INFO", # Nivel de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
}

# --- Extensiones de Archivo Soportadas ---
SUPPORTED_EXTENSIONS = ['.pdf', '.docx']
