# retry_descriptions.py
# Script para reintentar la generación de descripciones de imágenes que fallaron.

import os
import sys
import logging
import json
import config
from modulos import utils_fs, generador_descripciones, ensamblador_markdown

def main(work_dir: str):
    """
    Función principal que orquesta el reintento de descripciones.
    """
    log_dir = os.path.join(work_dir, config.OUTPUT_DIRS["LOGS"])
    utils_fs.setup_logging(log_dir, config.LOG_CONFIG)
    logging.info(f"--- INICIANDO REINTENTO DE DESCRIPCIONES EN: {work_dir} ---")

    artifacts_dir = os.path.join(work_dir, config.OUTPUT_DIRS["ARTIFACTS"])
    if not os.path.isdir(artifacts_dir):
        logging.error(f"El directorio de artefactos no existe: {artifacts_dir}")
        sys.exit(1)

    # Bucle principal: itera sobre las obras ya extraídas
    for obra_dir_name in sorted(os.listdir(artifacts_dir)):
        doc_artifact_path = os.path.join(artifacts_dir, obra_dir_name)
        if not os.path.isdir(doc_artifact_path):
            continue

        logging.info(f"\n{'='*60}\nVerificando Obra: {obra_dir_name}\n{'='*60}")

        # Verificar si hay descripciones que reintentar
        metadata_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["METADATA"])
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            
            failed_images = [img for img in metadata.get("images", []) if "Error" in str(img.get("description"))]
            if not failed_images:
                logging.info("  No hay descripciones fallidas que reintentar.")
                continue
            
            logging.info(f"  {len(failed_images)} descripciones fallidas encontradas. Reintentando...")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"  No se pudo leer o decodificar el archivo de metadatos: {e}")
            continue

        # Si hay fallos, ejecutar el generador de descripciones de nuevo.
        # La función ya es lo suficientemente inteligente para reintentar solo las que faltan.
        if not generador_descripciones.generate_descriptions_for_doc(doc_artifact_path):
            logging.error(f"  FALLO CRÍTICO: No se pudieron regenerar las descripciones para {obra_dir_name}.")
            continue

        # Re-ensamblar el Markdown para reflejar las nuevas descripciones
        logging.info("  Re-ensamblando el Markdown con las nuevas descripciones...")
        if not ensamblador_markdown.assemble_markdown_for_doc(doc_artifact_path, work_dir):
            logging.error(f"  FALLO CRÍTICO: No se pudo re-ensamblar el Markdown para {obra_dir_name}.")
            continue

        logging.info(f"  REINTENTO COMPLETADO PARA: {obra_dir_name}")

    logging.info("\n--- PROCESO DE REINTENTO COMPLETADO ---")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python retry_descriptions.py <ruta_al_directorio_de_trabajo_existente>")
        sys.exit(1)
    
    work_path = sys.argv[1]
    main(work_path)
