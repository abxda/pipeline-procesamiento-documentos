# modulos/utils_fs.py
# Utilidades para la gestión del sistema de archivos.

import os
import shutil

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

    Args:
        obra_path (str): La ruta a la carpeta de la obra (ej. '.../corpus_nahuatl/1').

    Returns:
        dict: Un diccionario con las rutas a los archivos de texto e imágenes, o None si no se encuentran.
    """
    sources = {"text": [], "image": []}
    
    # Definir rutas de las posibles fuentes
    ocr_docx_path = os.path.join(obra_path, 'ocr_docx')
    ocr_pdf_path = os.path.join(obra_path, 'ocr_pdf')
    img_pdf_path = os.path.join(obra_path, 'img_pdf')

    # Lógica de selección de fuente de TEXTO
    if os.path.isdir(ocr_docx_path) and os.listdir(ocr_docx_path):
        sources["text"] = sorted([os.path.join(ocr_docx_path, f) for f in os.listdir(ocr_docx_path) if f.endswith('.docx')])
    elif os.path.isdir(ocr_pdf_path) and os.listdir(ocr_pdf_path):
        sources["text"] = sorted([os.path.join(ocr_pdf_path, f) for f in os.listdir(ocr_pdf_path) if f.endswith('.pdf')])
    elif os.path.isdir(img_pdf_path) and os.listdir(img_pdf_path):
        sources["text"] = sorted([os.path.join(img_pdf_path, f) for f in os.listdir(img_pdf_path) if f.endswith('.pdf')])

    # Lógica de selección de fuente de IMÁGENES (siempre img_pdf si existe)
    if os.path.isdir(img_pdf_path) and os.listdir(img_pdf_path):
        sources["image"] = sorted([os.path.join(img_pdf_path, f) for f in os.listdir(img_pdf_path) if f.endswith('.pdf')])
    else:
        # Si no hay img_pdf, las imágenes vendrán de la misma fuente que el texto
        sources["image"] = sources["text"]

    if not sources["text"] or not sources["image"]:
        return None
        
    return sources
