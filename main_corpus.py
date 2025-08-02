# main_corpus.py
# Orquestador especializado para procesar corpus estructurados por carpetas.

import os
import sys
import config
from modulos import utils_fs, procesador_documentos, procesador_imagenes, generador_descripciones, ensamblador_markdown
import logging

def main(corpus_directory: str):
    """
    Función principal que orquesta el pipeline para un corpus estructurado.
    """
    output_dir = utils_fs.setup_main_output_dir(corpus_directory, config.OUTPUT_DIRS)
    utils_fs.setup_logging(os.path.join(output_dir, config.OUTPUT_DIRS["LOGS"]), config.LOG_CONFIG)
    logging.info(f"Directorio de trabajo configurado en: {output_dir}")

    # ... (resto del código con logging en lugar de print)


    # Bucle principal: itera sobre las carpetas de obra (ej. '1', '2', '11')
    for obra_dir_name in sorted(os.listdir(corpus_directory)):
        obra_path = os.path.join(corpus_directory, obra_dir_name)
        if not os.path.isdir(obra_path):
            continue

        print(f"\n{'='*60}\nProcesando Obra: {obra_dir_name}\n{'='*60}")

        # Lógica de reanudación
        final_md_path = os.path.join(output_dir, config.OUTPUT_DIRS["FINAL_MARKDOWN"], f"{obra_dir_name}.md")
        if os.path.exists(final_md_path):
            print(f"  RESULTADO FINAL YA EXISTE. Saltando obra {obra_dir_name}.")
            continue

        # --- Paso 1: Encontrar las mejores fuentes para la obra ---
        sources = utils_fs.find_best_sources(obra_path)
        if not sources:
            print(f"  ADVERTENCIA: No se encontraron fuentes válidas para la obra {obra_dir_name}. Saltando.")
            continue

        # --- Paso 2: Extracción de Artefactos Híbridos ---
        doc_artifact_path = procesador_documentos.extract_artifacts_from_corpus(sources, output_dir, obra_dir_name)
        if not doc_artifact_path:
            print(f"  FALLO CRÍTICO: No se pudieron extraer los artefactos para {obra_dir_name}. Saltando.")
            continue

        # --- Paso 3: Optimización de Imágenes ---
        if not procesador_imagenes.optimize_images_for_doc(doc_artifact_path):
            print(f"  FALLO CRÍTICO: No se pudieron optimizar las imágenes para {obra_dir_name}. Saltando.")
            continue

        # --- Paso 4: Generación de Descripciones ---
        if not generador_descripciones.generate_descriptions_for_doc(doc_artifact_path):
            print(f"  FALLO CRÍTICO: No se pudieron generar las descripciones para {obra_dir_name}. Saltando.")
            continue

        # --- Paso 5: Ensamblaje del Markdown ---
        if not ensamblador_markdown.assemble_markdown_for_doc(doc_artifact_path, output_dir):
            print(f"  FALLO CRÍTICO: No se pudo ensamblar el Markdown para {obra_dir_name}. Saltando.")
            continue
        
        print(f"  PROCESAMIENTO COMPLETADO CON ÉXITO PARA: {obra_dir_name}")

    print("\n--- PIPELINE DE CORPUS COMPLETADO ---")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main_corpus.py <ruta_al_directorio_del_corpus>")
        sys.exit(1)
    
    corpus_path = sys.argv[1]
    main(corpus_path)
