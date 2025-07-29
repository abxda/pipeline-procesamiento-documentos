# repair_missing_text.py
# Script para re-extraer el texto y re-ensamblar el Markdown de obras específicas.

import os
import sys
import logging
import config
from modulos import utils_fs, procesador_documentos, ensamblador_markdown

def main(corpus_dir: str, work_dir: str, obra_ids: list[str]):
    """
    Función principal que orquesta la reparación.
    """
    log_dir = os.path.join(work_dir, config.OUTPUT_DIRS["LOGS"])
    utils_fs.setup_logging(log_dir, config.LOG_CONFIG)
    logging.info(f"--- INICIANDO REPARACIÓN DE TEXTO EN: {work_dir} ---")
    logging.info(f"--- Obras a reparar: {', '.join(obra_ids)} ---")

    for obra_id in obra_ids:
        logging.info(f"\n{'='*60}\nReparando Obra: {obra_id}\n{'='*60}")

        obra_path_original = os.path.join(corpus_dir, obra_id)
        doc_artifact_path = os.path.join(work_dir, config.OUTPUT_DIRS["ARTIFACTS"], obra_id)

        if not os.path.isdir(doc_artifact_path):
            logging.error(f"  No se encontró el directorio de artefactos para la obra {obra_id}. Saltando.")
            continue

        # 1. Encontrar las mejores fuentes de texto
        logging.info("  [Paso 1 de 3] Re-identificando las mejores fuentes de texto...")
        sources = utils_fs.find_best_sources(obra_path_original)
        if not sources or not sources["text"]:
            logging.error(f"  No se encontraron fuentes de texto para la obra {obra_id}. Saltando.")
            continue
        logging.info(f"    -> Fuentes de texto encontradas en: {os.path.dirname(sources['text'][0])}")

        # 2. Re-extraer y sobrescribir solo el artefacto de texto
        logging.info("  [Paso 2 de 3] Re-extrayendo el texto...")
        if not procesador_documentos.regenerate_text_artifact(sources, doc_artifact_path):
            logging.error(f"  FALLO CRÍTICO: No se pudo regenerar el texto para {obra_id}. Saltando.")
            continue

        # 3. Re-ensamblar el Markdown final
        logging.info("  [Paso 3 de 3] Re-ensamblando el archivo Markdown final...")
        if not ensamblador_markdown.assemble_markdown_for_doc(doc_artifact_path, work_dir):
            logging.error(f"  FALLO CRÍTICO: No se pudo re-ensamblar el Markdown para {obra_id}. Saltando.")
            continue

        logging.info(f"  REPARACIÓN COMPLETADA CON ÉXITO PARA: {obra_id}")

    logging.info("\n--- PROCESO DE REPARACIÓN COMPLETADO ---")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python repair_missing_text.py <ruta_corpus_original> <ruta_trabajo_existente> <IDs_obras_separados_por_coma>")
        sys.exit(1)
    
    corpus_path = sys.argv[1]
    work_path = sys.argv[2]
    obra_ids_to_repair = sys.argv[3].split(',')
    main(corpus_path, work_path, obra_ids_to_repair)
