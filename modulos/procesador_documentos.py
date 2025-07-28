# modulos/procesador_documentos.py
# Módulo para interactuar con la librería Docling y extraer artefactos.

import os
import json
import gc
import base64
import config
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

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
    Extrae texto de la mejor fuente de texto e imágenes de la mejor fuente de imágenes.
    """
    print(f"  [Paso 1] Extrayendo artefactos de fuentes híbridas...")

    try:
        doc_artifact_path = create_artifact_structure_for_doc(output_dir, obra_name)
    except OSError as e:
        print(f"    ERROR: No se pudo crear la estructura de directorios para {obra_name}. Razón: {e}")
        return None

    # --- Configurar Docling --- 
    pipeline_options = PdfPipelineOptions(generate_picture_images=True)
    format_options = {
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
        InputFormat.DOCX: PdfFormatOption(pipeline_options=pipeline_options)
    }
    converter = DocumentConverter(format_options=format_options)

    # --- Procesar fuente de TEXTO ---
    try:
        print(f"    -> Procesando {len(sources['text'])} archivo(s) para TEXTO.")
        text_result = converter.convert(sources['text'])
        text_doc = text_result.document
    except Exception as e:
        print(f"    ERROR: Docling falló al procesar la fuente de texto. Razón: {e}")
        return None

    # --- Procesar fuente de IMÁGENES ---
    try:
        print(f"    -> Procesando {len(sources['image'])} archivo(s) para IMÁGENES.")
        image_result = converter.convert(sources['image'])
        image_doc = image_result.document
    except Exception as e:
        print(f"    ERROR: Docling falló al procesar la fuente de imagen. Razón: {e}")
        # No es fatal, podemos continuar solo con el texto.
        image_doc = text_doc # Usar el doc de texto como fallback

    del converter, text_result, image_result
    gc.collect()

    metadata = {"source_files": sources, "images": [], "tables": []}

    # Guardar el texto de la mejor fuente
    text_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["TEXT"])
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text_doc.export_to_markdown())
    print(f"    -> Texto guardado en: {config.ARTIFACT_SUBDIRS['TEXT']}")

    # Guardar las imágenes de la mejor fuente
    images_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["ORIGINAL_IMAGES"])
    for i, picture in enumerate(image_doc.pictures):
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
    print(f"    -> {len(image_doc.pictures)} imágenes guardadas en: {config.ARTIFACT_SUBDIRS['ORIGINAL_IMAGES']}")

    metadata_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["METADATA"])
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"    -> Metadatos iniciales guardados en: {config.ARTIFACT_SUBDIRS['METADATA']}")
    
    print("  [Paso 1] Extracción híbrida completada.")
    return doc_artifact_path

