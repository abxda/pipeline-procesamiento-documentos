# modulos/ensamblador_markdown.py
# Módulo para construir el archivo Markdown final.

import os
import json
import config

def assemble_markdown_for_doc(doc_artifact_path: str, output_dir: str):
    """
    Ensambla el archivo Markdown final a partir de los artefactos generados.
    """
    print("  [Paso 4] Ensamblando el archivo Markdown final...")
    doc_basename = os.path.basename(doc_artifact_path)
    metadata_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["METADATA"])
    text_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["TEXT"])
    final_md_path = os.path.join(output_dir, config.OUTPUT_DIRS["FINAL_MARKDOWN"], f"{doc_basename}.md")

    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        
        with open(text_path, "r", encoding="utf-8") as f:
            base_markdown = f.read()

    except FileNotFoundError as e:
        print(f"    ERROR: No se encontró un archivo necesario ({e.filename}). No se puede ensamblar el Markdown.")
        return False

    final_markdown = base_markdown
    images_metadata = metadata.get("images", [])

    for image_meta in images_metadata:
        # La ruta en el markdown debe ser relativa al propio markdown
        # Ej: ../02_artefactos_extraidos/documento/imagenes_originales/img_01.png
        relative_image_path = os.path.join(
            "..",
            config.OUTPUT_DIRS["ARTIFACTS"],
            doc_basename,
            image_meta["original_path"]
        )

        description = image_meta.get("description", "Descripción no disponible.")
        model_name = config.OLLAMA_CONFIG["MODEL_NAME"]

        replacement_text = (
            f"\n![{description[:100]}]({relative_image_path})\n"
            f"> **Descripción ({model_name}):** {description}\n"
        )

        # Reemplazar el primer placeholder disponible
        final_markdown = final_markdown.replace("<!-- image -->", replacement_text, 1)

    try:
        with open(final_md_path, "w", encoding="utf-8") as f:
            f.write(final_markdown)
        print(f"    -> Archivo final guardado en: {final_md_path}")
    except IOError as e:
        print(f"    ERROR: No se pudo escribir el archivo Markdown final. Razón: {e}")
        return False

    print("  [Paso 4] Ensamblaje completado.")
    return True
