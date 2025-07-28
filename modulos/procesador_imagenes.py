# modulos/procesador_imagenes.py
# Módulo para optimizar imágenes y actualizar metadatos.

import os
import json
import io
from PIL import Image
import config

def optimize_images_for_doc(doc_artifact_path: str):
    """
    Encuentra las imágenes originales, las optimiza y actualiza los metadatos.
    """
    print("  [Paso 2] Optimizando imágenes...")
    metadata_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["METADATA"])
    
    try:
        with open(metadata_path, "r+", encoding="utf-8") as f:
            metadata = json.load(f)
            
            images_to_process = [img for img in metadata["images"] if not img.get("optimized_path")]
            if not images_to_process:
                print("    -> No hay imágenes nuevas que optimizar.")
                return True

            print(f"    -> {len(images_to_process)} imágenes para optimizar.")

            for image_meta in images_to_process:
                original_full_path = os.path.join(doc_artifact_path, os.path.dirname(image_meta["original_path"]), os.path.basename(image_meta["original_path"])) # Reconstrucción de la ruta completa
                optimized_relative_path = os.path.join(config.ARTIFACT_SUBDIRS["OPTIMIZED_IMAGES"], os.path.basename(image_meta["original_path"])) # Ruta relativa para guardar
                optimized_full_path = os.path.join(doc_artifact_path, optimized_relative_path)

                try:
                    with open(original_full_path, "rb") as img_file:
                        original_bytes = img_file.read()
                    
                    image = Image.open(io.BytesIO(original_bytes))
                    max_dim = config.IMAGE_PROCESSING_CONFIG["MAX_DIMENSION"]
                    
                    if image.width > max_dim or image.height > max_dim:
                        image.thumbnail((max_dim, max_dim))
                    
                    output_buffer = io.BytesIO()
                    image.save(output_buffer, format=config.IMAGE_PROCESSING_CONFIG["OPTIMIZED_FORMAT"])
                    optimized_bytes = output_buffer.getvalue()

                    with open(optimized_full_path, "wb") as opt_img_file:
                        opt_img_file.write(optimized_bytes)
                    
                    # Actualizar metadatos
                    image_meta["optimized_path"] = optimized_relative_path

                except FileNotFoundError:
                    print(f"    ERROR: No se encontró el archivo de imagen original: {original_full_path}")
                    continue
                except Exception as e:
                    print(f"    ERROR: No se pudo optimizar la imagen {image_meta['id']}. Razón: {e}")
                    continue

            # Volver al inicio del archivo para sobrescribir
            f.seek(0)
            json.dump(metadata, f, indent=4)
            f.truncate()

    except FileNotFoundError:
        print(f"    ERROR: No se encontró el archivo de metadatos en {doc_artifact_path}")
        return False
    except json.JSONDecodeError:
        print(f"    ERROR: El archivo de metadatos en {doc_artifact_path} está corrupto.")
        return False

    print("  [Paso 2] Optimización completada.")
    return True
