# modulos/generador_descripciones.py
# Módulo para generar descripciones de imágenes usando Ollama.

import os
import json
import base64
import requests
import config
import logging

def generate_descriptions_for_doc(doc_artifact_path: str):
    """
    Genera descripciones para las imágenes optimizadas que aún no la tienen.
    Guarda el progreso incrementalmente después de cada imagen.
    """
    logging.info("  [Paso 3] Generando descripciones con Ollama...")
    metadata_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["METADATA"])

    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"    No se pudo leer o decodificar el archivo de metadatos: {e}")
        return False

    images_to_describe = [img for img in metadata["images"] if img.get("optimized_path") and not img.get("description")]
    if not images_to_describe:
        logging.info("    -> No hay imágenes nuevas que describir.")
        return True

    logging.info(f"    -> {len(images_to_describe)} imágenes para describir con {config.OLLAMA_CONFIG['MODEL_NAME']}.")

    for image_meta in images_to_describe:
        optimized_full_path = os.path.join(doc_artifact_path, image_meta["optimized_path"])
        description = None
        try:
            with open(optimized_full_path, "rb") as img_file:
                image_bytes = img_file.read()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')

            payload = {
                "model": config.OLLAMA_CONFIG["MODEL_NAME"],
                "stream": False,
                "messages": [{
                    "role": "user",
                    "content": config.PROMPTS["DESCRIBE_IMAGE_ES"],
                    "images": [base64_image]
                }]
            }

            response = requests.post(
                config.OLLAMA_CONFIG["API_ENDPOINT_CHAT"],
                json=payload,
                timeout=config.OLLAMA_CONFIG["REQUEST_TIMEOUT"]
            )
            response.raise_for_status()
            response_data = response.json()
            description = response_data.get("message", {}).get("content")

            if description and "no puedo ver la imagen" not in description.lower():
                description = description.strip()
                logging.info(f"      -> ÉXITO para {image_meta['id']}")
            else:
                description = "No se pudo generar una descripción válida."
                logging.warning(f"      -> FALLO para {image_meta['id']}: Descripción no válida.")

        except FileNotFoundError:
            description = f"Error: Archivo de imagen no encontrado en {optimized_full_path}"
            logging.error(f"    {description}")
        except requests.exceptions.RequestException as e:
            description = f"Error de API: {e}"
            logging.error(f"    Error de API para {image_meta['id']}: {e}")
        except Exception as e:
            description = f"Error inesperado: {e}"
            logging.error(f"    Error inesperado para {image_meta['id']}: {e}")
        
        # --- Guardado Incremental ---
        if description:
            try:
                with open(metadata_path, "r+", encoding="utf-8") as f:
                    # Recargar por si acaso, aunque en este flujo no es estrictamente necesario
                    current_metadata = json.load(f)
                    # Encontrar y actualizar la imagen correcta
                    for img in current_metadata.get("images", []):
                        if img["id"] == image_meta["id"]:
                            img["description"] = description
                            break
                    # Sobrescribir el archivo
                    f.seek(0)
                    json.dump(current_metadata, f, indent=4)
                    f.truncate()
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.error(f"    FALLO CRÍTICO al guardar incrementalmente para {image_meta['id']}: {e}")
                # Si no podemos guardar, detener este proceso para no perder más tiempo/recursos
                return False

    logging.info("  [Paso 3] Generación de descripciones completada.")
    return True
