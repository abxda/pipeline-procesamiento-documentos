# modulos/generador_descripciones.py
# Módulo para generar descripciones de imágenes usando Ollama.

import os
import json
import base64
import requests
import config

def generate_descriptions_for_doc(doc_artifact_path: str):
    """
    Genera descripciones para las imágenes optimizadas que aún no la tienen.
    """
    print("  [Paso 3] Generando descripciones con Ollama...")
    metadata_path = os.path.join(doc_artifact_path, config.ARTIFACT_SUBDIRS["METADATA"])

    try:
        with open(metadata_path, "r+", encoding="utf-8") as f:
            metadata = json.load(f)

            images_to_describe = [img for img in metadata["images"] if img.get("optimized_path") and not img.get("description")]
            if not images_to_describe:
                print("    -> No hay imágenes nuevas que describir.")
                return True

            print(f"    -> {len(images_to_describe)} imágenes para describir con {config.OLLAMA_CONFIG['MODEL_NAME']}.")

            for image_meta in images_to_describe:
                optimized_full_path = os.path.join(doc_artifact_path, image_meta["optimized_path"])
                
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
                        image_meta["description"] = description.strip()
                        print(f"      -> ÉXITO para {image_meta['id']}")
                    else:
                        image_meta["description"] = "No se pudo generar una descripción válida."
                        print(f"      -> FALLO para {image_meta['id']}")

                except FileNotFoundError:
                    print(f"    ERROR: No se encontró el archivo de imagen optimizada: {optimized_full_path}")
                    continue
                except requests.exceptions.RequestException as e:
                    print(f"    ERROR de API para {image_meta['id']}: {e}")
                    image_meta["description"] = f"Error de API: {e}"
                    continue
                except Exception as e:
                    print(f"    ERROR inesperado para {image_meta['id']}: {e}")
                    image_meta["description"] = f"Error inesperado: {e}"
                    continue

            f.seek(0)
            json.dump(metadata, f, indent=4)
            f.truncate()

    except FileNotFoundError:
        print(f"    ERROR: No se encontró el archivo de metadatos en {doc_artifact_path}")
        return False
    except json.JSONDecodeError:
        print(f"    ERROR: El archivo de metadatos en {doc_artifact_path} está corrupto.")
        return False

    print("  [Paso 3] Generación de descripciones completada.")
    return True
