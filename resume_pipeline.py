# resume_pipeline.py
# Script para reanudar un trabajo de pipeline existente.

import os
import sys
import logging
import config
from modulos import procesador_imagenes, generador_descripciones, ensamblador_markdown, utils_fs

def main(existing_work_dir: str):
    """
    Función principal que reanuda un pipeline existente.
    """
    utils_fs.setup_logging(os.path.join(existing_work_dir, config.OUTPUT_DIRS["LOGS"]), config.LOG_CONFIG)
    logging.info(f"--- REANUDANDO PIPELINE EN: {existing_work_dir} ---")

    artifacts_dir = os.path.join(existing_work_dir, config.OUTPUT_DIRS["ARTIFACTS"])
    if not os.path.isdir(artifacts_dir):
        logging.error(f"El directorio de artefactos no existe: {artifacts_dir}")
        sys.exit(1)

    # Bucle principal: itera sobre las obras ya extraídas
    for obra_dir_name in sorted(os.listdir(artifacts_dir)):
        doc_artifact_path = os.path.join(artifacts_dir, obra_dir_name)
        if not os.path.isdir(doc_artifact_path):
            continue

        logging.info(f"\n{'='*60}\nReanudando Obra: {obra_dir_name}\n{'='*60}")

        # --- Paso 2: Optimización de Imágenes (resumible por naturaleza) ---
        if not procesador_imagenes.optimize_images_for_doc(doc_artifact_path):
            logging.error(f"  FALLO CRÍTICO: No se pudieron optimizar las imágenes para {obra_dir_name}.")
            continue

        # --- Paso 3: Generación de Descripciones (ahora incremental) ---
        if not generador_descripciones.generate_descriptions_for_doc(doc_artifact_path):
            logging.error(f"  FALLO CRÍTICO: No se pudieron generar las descripciones para {obra_dir_name}.")
            continue

        # --- Paso 4: Ensamblaje del Markdown ---
        if not ensamblador_markdown.assemble_markdown_for_doc(doc_artifact_path, existing_work_dir):
            logging.error(f"  FALLO CRÍTICO: No se pudo ensamblar el Markdown para {obra_dir_name}.")
            continue
        
        logging.info(f"  PROCESAMIENTO COMPLETADO CON ÉXITO PARA: {obra_dir_name}")

    logging.info("\n--- PIPELINE REANUDADO COMPLETADO ---")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python resume_pipeline.py <ruta_al_directorio_de_trabajo_existente>")
        sys.exit(1)
    
    work_path = sys.argv[1]
    main(work_path)
