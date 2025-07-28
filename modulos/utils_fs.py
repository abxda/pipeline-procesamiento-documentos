# modulos/utils_fs.py
# Utilidades para la gestión del sistema de archivos.

import os
import shutil
import logging

def setup_logging(log_dir: str, config: dict):
    """
    Configura el sistema de logging para que escriba a un archivo y a la consola.
    """
    log_filename = config["FILENAME"]
    log_level = config["LEVEL"]
    log_filepath = os.path.join(log_dir, log_filename)

    # Evitar que se añadan múltiples handlers si la función se llama más de una vez
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=getattr(logging, log_level.upper(), logging.INFO),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filepath),
                logging.StreamHandler()
            ]
        )


def setup_main_output_dir(base_path: str, config: dict) -> str:
    """
    Crea el directorio de salida principal y su estructura interna.
    Maneja la numeración para evitar sobrescribir ejecuciones anteriores.

    Args:
        base_path (str): La ruta del directorio de entrada que se está procesando.
        config (dict): El diccionario de configuración (OUTPUT_DIRS).

    Returns:
        str: La ruta al directorio de salida principal que se ha creado.
    """
    base_name = os.path.basename(os.path.normpath(base_path))
    parent_dir = os.path.dirname(base_path)
    attempt = 1

    while True:
        output_dir_name = f"{base_name}_processed_{attempt:02d}"
        output_dir_path = os.path.join(parent_dir, output_dir_name)
        if not os.path.exists(output_dir_path):
            print(f"Creando directorio de salida: {output_dir_path}")
            os.makedirs(output_dir_path)
            break
        attempt += 1

    # Crear subdirectorios principales a partir de la configuración
    for dir_key, dir_name in config.items():
        os.makedirs(os.path.join(output_dir_path, dir_name), exist_ok=True)
    
    return output_dir_path

def copy_original_document(source_path: str, output_dir: str, config: dict):
    """
    Copia el documento original al directorio '01_documentos_originales'.
    """
    originals_path = os.path.join(output_dir, config["OUTPUT_DIRS"]["ORIGINALS"])
    shutil.copy(source_path, originals_path)

def find_best_sources(obra_path: str) -> dict:
    """
    Analiza la estructura de una obra y determina la mejor fuente para texto e imágenes.
    Intenta primero una estructura con subcarpetas (ocr_docx, etc.) y si no, busca
    archivos directamente en la raíz de la obra.
    """
    sources = {"text": [], "image": []}
    
    # --- Intento 1: Estructura de subcarpetas (ocr_docx, img_pdf) ---
    ocr_docx_path = os.path.join(obra_path, 'ocr_docx')
    ocr_pdf_path = os.path.join(obra_path, 'ocr_pdf')
    img_pdf_path = os.path.join(obra_path, 'img_pdf')

    if os.path.isdir(ocr_docx_path) and os.listdir(ocr_docx_path):
        sources["text"] = sorted([os.path.join(ocr_docx_path, f) for f in os.listdir(ocr_docx_path) if f.endswith('.docx')])
    elif os.path.isdir(ocr_pdf_path) and os.listdir(ocr_pdf_path):
        sources["text"] = sorted([os.path.join(ocr_pdf_path, f) for f in os.listdir(ocr_pdf_path) if f.endswith('.pdf')])
    elif os.path.isdir(img_pdf_path) and os.listdir(img_pdf_path):
        sources["text"] = sorted([os.path.join(img_pdf_path, f) for f in os.listdir(img_pdf_path) if f.endswith('.pdf')])

    if os.path.isdir(img_pdf_path) and os.listdir(img_pdf_path):
        sources["image"] = sorted([os.path.join(img_pdf_path, f) for f in os.listdir(img_pdf_path) if f.endswith('.pdf')])
    else:
        sources["image"] = sources["text"]

    # --- Intento 2: Fallback a la raíz de la obra ---
    if not sources["text"]:
        root_files_pdf = sorted([os.path.join(obra_path, f) for f in os.listdir(obra_path) if f.endswith('.pdf')])
        root_files_docx = sorted([os.path.join(obra_path, f) for f in os.listdir(obra_path) if f.endswith('.docx')])
        
        # Dar prioridad a DOCX si existen
        if root_files_docx:
            sources["text"] = root_files_docx
            sources["image"] = root_files_docx
        elif root_files_pdf:
            sources["text"] = root_files_pdf
            sources["image"] = root_files_pdf

    if not sources["text"] or not sources["image"]:
        return None
        
    return sources
