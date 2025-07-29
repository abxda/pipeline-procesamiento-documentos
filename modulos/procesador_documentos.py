# modulos/procesador_documentos.py
# Módulo para interactuar con la librería Docling y extraer artefactos.

import os
import json
import gc
import base64
import config
import logging
from docling.document_converter import DocumentConverter, PdfFormatOption, WordFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, PipelineOptions

def create_artifact_structure_for_doc(output_dir: str, doc_basename: str) -> str:
    """Crea la estructura de directorios para los artefactos de un documento."""
    artifacts_base_path = os.path.join(output_dir, config.OUTPUT_DIRS["ARTIFACTS"])
    doc_artifact_path = os.path.join(artifacts_base_path, doc_basename)
    
    os.makedirs(os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["ORIGINAL_IMAGES"]), exist_ok=True)
    os.makedirs(os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["OPTIMIZED_IMAGES"]), exist_ok=True)
    os.makedirs(os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["TABLES"]), exist_ok=True)
    
    return doc_artifact_path

def extract_artifacts_from_corpus(sources: dict, output_dir: str, obra_name: str) -> str | None:
    """
    Usa Docling para extraer artefactos de un conjunto de fuentes de corpus.
    Procesa cada archivo individualmente y agrega los resultados.
    """
    print(f"  [Paso 1] Extrayendo artefactos de fuentes híbridas...")

    try:
        doc_artifact_path = create_artifact_structure_for_doc(output_dir, obra_name)
    except OSError as e:
        print(f"    ERROR: No se pudo crear la estructura de directorios para {obra_name}. Razón: {e}")
        return None

    # --- Configurar Docling --- 
    pdf_pipeline_options = PdfPipelineOptions(generate_picture_images=True)
    docx_pipeline_options = PipelineOptions(generate_picture_images=True)
    format_options = {
        InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_pipeline_options),
        InputFormat.DOCX: WordFormatOption(pipeline_options=docx_pipeline_options)
    }
    converter = DocumentConverter(format_options=format_options)

    # --- Procesar y agregar resultados ---
    full_text = ""
    all_pictures = []

    # Procesar TEXTO de la mejor fuente
    print(f"    -> Procesando {len(sources['text'])} archivo(s) para TEXTO.")
    for text_file in sources['text']:
        try:
            result = converter.convert(text_file)
            full_text += result.document.export_to_markdown() + "\n\n---\n\n"
        except Exception as e:
            print(f"    ADVERTENCIA: Docling falló al procesar el archivo de texto '{os.path.basename(text_file)}'. Razón: {e}")

    # Procesar IMÁGENES de la mejor fuente
    print(f"    -> Procesando {len(sources['image'])} archivo(s) para IMÁGENES.")
    for image_file in sources['image']:
        try:
            result = converter.convert(image_file)
            all_pictures.extend(result.document.pictures)
        except Exception as e:
            print(f"    ADVERTENCIA: Docling falló al procesar el archivo de imagen '{os.path.basename(image_file)}'. Razón: {e}")

    del converter
    gc.collect()

    metadata = {"source_files": sources, "images": [], "tables": []}

    # Guardar el texto agregado
    text_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["TEXT"])
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"    -> Texto agregado guardado en: {config.ARTIFACT_SUBDIRS['TEXT']}")

    # Guardar las imágenes agregadas
    images_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["ORIGINAL_IMAGES"])
    for i, picture in enumerate(all_pictures):
        img_filename = f"img_{i+1:03d}.png"
        img_filepath = os.path.join(images_path, img_filename)
        try:
            header, base64_data = str(picture.image.uri).split(',', 1)
            image_bytes = base64.b64decode(base64_data)
            with open(img_filepath, "wb") as f:
                f.write(image_bytes)

            metadata["images"].append({
                "id": f"img_{i+1:03d}",
                "original_path": os.path.join(config.ARTIFACT_SUBDIRS["ORIGINAL_IMAGES"], img_filename),
                "optimized_path": None,
                "description": None
            })
        except Exception as e:
            print(f"    ADVERTENCIA: No se pudo guardar la imagen {i+1}. Razón: {e}")
    print(f"    -> {len(all_pictures)} imágenes guardadas en: {config.ARTIFACT_SUBDIRS['ORIGINAL_IMAGES']}")

    metadata_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["METADATA"])
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"    -> Metadatos iniciales guardados en: {config.ARTIFACT_SUBDIRS['METADATA']}")

    print("  [Paso 1] Extracción híbrida completada.")
    return doc_artifact_path

def regenerate_text_artifact(sources: dict, doc_artifact_path: str) -> bool:
    """
    Procesa únicamente la mejor fuente de texto y sobrescribe el artefacto de texto existente.
    No toca las imágenes ni los metadatos.
    """
    # --- Configurar Docling ---
    pdf_pipeline_options = PdfPipelineOptions(generate_picture_images=False) # No necesitamos imágenes aquí
    docx_pipeline_options = PipelineOptions(generate_picture_images=False)
    format_options = {
        InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_pipeline_options),
        InputFormat.DOCX: WordFormatOption(pipeline_options=docx_pipeline_options)
    }
    converter = DocumentConverter(format_options=format_options)

    # --- Procesar y agregar texto ---
    full_text = ""
    logging.info(f"    -> Procesando {len(sources['text'])} archivo(s) para TEXTO.")
    for text_file in sources['text']:
        try:
            result = converter.convert(text_file)
            full_text += result.document.export_to_markdown() + "\n\n---\n\n"
        except Exception as e:
            logging.warning(f"    Docling falló al procesar el archivo de texto '{os.path.basename(text_file)}'. Razón: {e}")

    del converter
    gc.collect()

    # --- Sobrescribir el artefacto de texto ---
    if not full_text:
        logging.error("    No se extrajo ningún texto. La regeneración falló.")
        return False

    text_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["TEXT"])
    try:
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        logging.info(f"    -> Texto regenerado y guardado en: {config.ARTIFACT_SUBDIRS['TEXT']}")
    except IOError as e:
        logging.error(f"    No se pudo escribir el artefacto de texto regenerado. Razón: {e}")
        return False

    return True


