# main.py
# Orquestador principal del pipeline de procesamiento de documentos.

import os
import sys
import config
from modulos import utils_fs

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
    for filename in os.listdir(input_directory):
        source_doc_path = os.path.join(input_directory, filename)
        doc_basename, doc_ext = os.path.splitext(filename)

        # Omitir archivos que no sean documentos soportados
        if doc_ext.lower() not in config.SUPPORTED_EXTENSIONS:
            print(f"Omitiendo archivo no soportado: {filename}")
            continue

        print(f"\n{'='*60}\nProcesando: {filename}\n{'='*60}")

        # --- Lógica de reanudación (a implementar) ---
        # TODO: Comprobar si el markdown final ya existe y saltar si es así.

        # --- Copiar documento original (Paso 0) ---
        utils_fs.copy_original_document(source_doc_path, output_dir, config)
        print(f"Copiado a la carpeta de originales: {filename}")

        # --- Aquí irán los siguientes pasos del pipeline ---
        # TODO: Llamar al procesador de documentos (docling)
        # TODO: Llamar al procesador de imágenes
        # TODO: Llamar al generador de descripciones
        # TODO: Llamar al ensamblador de markdown

    print("\n--- PIPELINE COMPLETADO ---")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <ruta_al_directorio_de_entrada>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    main(input_path)
