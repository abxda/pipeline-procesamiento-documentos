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
