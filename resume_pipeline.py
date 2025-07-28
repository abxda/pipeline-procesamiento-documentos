# resume_pipeline.py
# Script para reanudar un trabajo de pipeline existente.

import os
import sys
import logging
import config
from modulos import procesador_documentos, procesador_imagenes, generador_descripciones, ensamblador_markdown, utils_fs

def main(corpus_dir: str, existing_work_dir: str):
    """
    Función principal que reanuda un pipeline existente.
    """
    utils_fs.setup_logging(os.path.join(existing_work_dir, config.OUTPUT_DIRS["LOGS"]), config.LOG_CONFIG)
    logging.info(f"--- REANUDANDO PIPELINE EN: {existing_work_dir} ---")
    logging.info(f"--- USANDO CORPUS ORIGINAL DE: {corpus_dir} ---")

    if not os.path.isdir(corpus_dir):
        logging.error(f"El directorio del corpus original no existe: {corpus_dir}")
        sys.exit(1)

    # Bucle principal: itera sobre las carpetas de obra del corpus original
    for obra_dir_name in sorted(os.listdir(corpus_dir)):
        obra_path = os.path.join(corpus_dir, obra_dir_name)
        if not os.path.isdir(obra_path):
            continue

        # Lógica de reanudación: Comprobar si el markdown final ya existe
        final_md_path = os.path.join(existing_work_dir, config.OUTPUT_DIRS["FINAL_MARKDOWN"], f"{obra_dir_name}.md")
        if os.path.exists(final_md_path):
            logging.info(f"\n{'='*60}\nObra: {obra_dir_name} ya completada. Saltando.\n{'='*60}")
            continue

        logging.info(f"\n{'='*60}\nProcesando Obra Faltante: {obra_dir_name}\n{'='*60}")

        # --- Paso 1: Encontrar las mejores fuentes para la obra ---
        sources = utils_fs.find_best_sources(obra_path)
        if not sources:
            logging.warning(f"  ADVERTENCIA: No se encontraron fuentes válidas para la obra {obra_dir_name}. Saltando.")
            continue

        # --- Paso 2: Extracción de Artefactos Híbridos ---
        doc_artifact_path = procesador_documentos.extract_artifacts_from_corpus(sources, existing_work_dir, obra_dir_name)
        if not doc_artifact_path:
            logging.error(f"  FALLO CRÍTICO: No se pudieron extraer los artefactos para {obra_dir_name}.")
            continue

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
    if len(sys.argv) != 3:
        print("Uso: python resume_pipeline.py <ruta_al_directorio_del_corpus_original> <ruta_al_directorio_de_trabajo_existente>")
        sys.exit(1)
    
    corpus_path = sys.argv[1]
    work_path = sys.argv[2]
    main(corpus_path, work_path)
