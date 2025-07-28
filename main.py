# main.py
# Orquestador principal del pipeline de procesamiento de documentos.

import os
import sys
import config
from modulos import utils_fs, procesador_documentos, procesador_imagenes, generador_descripciones, ensamblador_markdown

def main(input_directory: str):
    """
    Función principal que orquesta todo el pipeline.
    """
    print(f"--- INICIANDO PIPELINE PARA: {input_directory} ---")

    # 1. Validar que el directorio de entrada existe
    if not os.path.isdir(input_directory):
        print(f"ERROR: El directorio de entrada no existe: {input_directory}")
        sys.exit(1)

    # 2. Configurar el directorio de salida principal
    output_dir = utils_fs.setup_main_output_dir(input_directory, config.OUTPUT_DIRS)
    print(f"Directorio de trabajo configurado en: {output_dir}")

    # 3. Bucle principal de procesamiento por documento
    for filename in sorted(os.listdir(input_directory)):
        source_doc_path = os.path.join(input_directory, filename)
        doc_basename, doc_ext = os.path.splitext(filename)

        # Omitir archivos que no sean documentos soportados
        if doc_ext.lower() not in config.SUPPORTED_EXTENSIONS:
            print(f"Omitiendo archivo no soportado: {filename}")
            continue

        print(f"\n{'='*60}\nProcesando: {filename}\n{'='*60}")

        # --- Lógica de reanudación ---
        final_md_path = os.path.join(output_dir, config.OUTPUT_DIRS["FINAL_MARKDOWN"], f"{doc_basename}.md")
        if os.path.exists(final_md_path):
            print(f"  RESULTADO FINAL YA EXISTE. Saltando procesamiento de {filename}.")
            continue

        # --- Copiar documento original (Paso 0) ---
        utils_fs.copy_original_document(source_doc_path, output_dir, config)
        print(f"Copiado a la carpeta de originales: {filename}")

        # --- Paso 1: Extracción de Artefactos ---
        doc_artifact_path = procesador_documentos.extract_artifacts(source_doc_path, output_dir)
        if not doc_artifact_path:
            print(f"  FALLO CRÍTICO: No se pudieron extraer los artefactos para {filename}. Saltando al siguiente documento.")
            continue

        # --- Paso 2: Optimización de Imágenes ---
        if not procesador_imagenes.optimize_images_for_doc(doc_artifact_path):
            print(f"  FALLO CRÍTICO: No se pudieron optimizar las imágenes para {filename}. Saltando al siguiente documento.")
            continue

        # --- Paso 3: Generación de Descripciones ---
        if not generador_descripciones.generate_descriptions_for_doc(doc_artifact_path):
            print(f"  FALLO CRÍTICO: No se pudieron generar las descripciones para {filename}. Saltando al siguiente documento.")
            continue

        # --- Paso 4: Ensamblaje del Markdown ---
        if not ensamblador_markdown.assemble_markdown_for_doc(doc_artifact_path, output_dir):
            print(f"  FALLO CRÍTICO: No se pudo ensamblar el Markdown para {filename}. Saltando al siguiente documento.")
            continue
        
        print(f"  PROCESAMIENTO COMPLETADO CON ÉXITO PARA: {filename}")

    print("\n--- PIPELINE COMPLETADO ---")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <ruta_al_directorio_de_entrada>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    main(input_path)
