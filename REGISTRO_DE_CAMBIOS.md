# Registro de Cambios y Ejecuciones del Pipeline

## Desarrollo del Pipeline

*   **2025-08-02 | Commit: (pendiente)**: **Corrección de Bug en `main_corpus.py`**. Se corrige un `NameError` al mover la importación del módulo `logging` al encabezado del archivo, asegurando su disponibilidad en todo el script.
*   **2025-07-28 | Commit: `f527902`**: **Implementación del Pipeline Híbrido para Corpus.** Se añade un nuevo orquestador (`main_corpus.py`) y se modifica el core del pipeline para procesar corpus complejos. El sistema ahora puede:
    *   Identificar la "mejor fuente" para texto (DOCX > OCR PDF > Imagen PDF) e imágenes (Imagen PDF).
    *   Procesar obras fragmentadas en múltiples archivos como una sola unidad.
    *   Extraer artefactos de fuentes híbridas para maximizar la calidad del resultado.
*   **2025-07-28 | Commit: `98df37c`**: Implementa el ensamblador de Markdown y la lógica de reanudación.
*   **2025-07-28 | Commit: `2475d74`**: Implementa el módulo de generación de descripciones con Ollama.
*   **2025-07-28 | Commit: `a07ce31`**: Implementa el módulo de optimización de imágenes.
*   **2025-07-28 | Commit: `7e4db84`**: Implementa el módulo de extracción de artefactos con Docling.
*   **2025-07-28 | Commit: `65bc590`**: Implementa esqueleto del orquestador y utilidades de FS.
*   **2025-07-28 | Commit: `c594fc4`**: Añade configuración centralizada para el pipeline.
*   **2025-07-28 | Commit: `a4aa17c`**: Creación de la estructura inicial del proyecto, configuración y lógica de reanudación en `main.py`.

## Historial de Ejecuciones

*   **2025-08-02 | Ejecución del Corpus de Actividades de Coaching**
    *   **Resultado:** Éxito Parcial. Se procesó un corpus de 28 entregas de actividades de liderazgo.
    *   **Hitos Logrados:**
        *   Se validó el pipeline con un nuevo tipo de corpus, demostrando su flexibilidad.
        *   Se identificó y corrigió un bug de importación en `main_corpus.py`.
        *   Se documentó el entorno de Conda funcional para el proyecto: `docling_env` en `/home/abxda/miniforge3/envs/docling_env`.
    *   **Limitaciones Identificadas:**
        *   **Fallo Persistente en API:** La generación de descripciones para una imagen en la obra `Equipo 2 H` falló repetidamente con un error 500 del servidor de Ollama, indicando un posible problema con el modelo o el servidor que requiere investigación.

*   **2025-07-29 | Versión 1.0: Corte Estable para Publicación**
    *   **Resultado:** Se finaliza la primera versión funcional y robusta del pipeline.
    *   **Capacidades Incluidas:**
        *   Procesamiento de corpus con estructuras de directorios flexibles (`main_corpus.py`).
        *   Herramienta de reanudación de trabajos interrumpidos (`resume_pipeline.py`).
        *   Herramienta de reparación de texto para resultados parciales (`repair_missing_text.py`).
        *   Herramienta de reintento para descripciones de imágenes fallidas (`retry_descriptions.py`).
        *   Generación de `requirements.txt` y `TUTORIAL.md` para la reproducibilidad y uso del proyecto.
    *   **Estado:** El proyecto está listo para ser publicado en un repositorio de control de versiones como GitHub.

*   **2025-07-29 | Creación de Herramientas de Soporte y Documentación**
    *   **Resultado:** Éxito. Se crearon herramientas adicionales y documentación para mejorar la usabilidad y mantenibilidad del proyecto.
    *   **Hitos Logrados:**
        *   Se creó el script `retry_descriptions.py` para reintentar de forma inteligente solo las descripciones de imágenes que fallaron.
        *   Se generó un archivo `requirements.txt` a partir del entorno de Conda para permitir una instalación reproducible con `pip`.
        *   Se redactó un manual de usuario completo (`TUTORIAL.md`) que detalla la instalación y el uso de todos los scripts del pipeline.

*   **2025-07-29 | Ejecución de Reparación (`repair_missing_text.py`)**
    *   **Resultado:** Éxito. Se repararon las obras `1` y `2` del directorio `corpus_nahuatl_processed_02`.
    *   **Hitos Logrados:**
        *   Se creó una herramienta de reparación (`repair_missing_text.py`) capaz de regenerar artefactos específicos sin afectar a los demás.
        *   Se re-extrajo con éxito el texto de los archivos DOCX que fallaron en la ejecución inicial.
        *   Se re-ensamblaron los archivos `1.md` y `2.md`, combinando el texto recién extraído con las descripciones de imágenes previamente generadas.
    *   **Confirmación:** Se valida la robustez de la arquitectura de artefactos, que permite la recuperación y reparación de trabajos fallidos.

*   **2025-07-28 | Ejecución del Corpus Náhuatl (`corpus_nahuatl_processed_02`)**
    *   **Resultado:** Éxito Parcial. Se procesaron todas las obras con formatos de archivo directos (PDF, DOCX), incluyendo las obras complejas (`1`, `2`) y las simples (`11`, `12`, `13`, `15`, `17`, `18`, `26`, `27`, `29`).
    *   **Hitos Logrados:**
        *   El pipeline demostró ser flexible, manejando diversas estructuras de directorios.
        *   El sistema de reanudación funcionó, omitiendo las obras ya procesadas en ejecuciones anteriores.
        *   Se confirmó el uso de la GPU (`cuda:0`) para la aceleración del OCR.
        *   El guardado incremental de metadatos demostró ser resiliente, manejando errores de la API de Ollama sin detener el proceso completo.
    *   **Limitaciones Identificadas y Próximos Pasos:**
        *   **Archivos ZIP:** La obra `28` fue omitida porque el pipeline no puede procesar archivos `.zip`. El siguiente paso es implementar la descompresión automática.
        *   **Carpetas Vacías:** Las obras `24` y `25` fueron omitidas correctamente por estar vacías.
        *   **Descripciones Fallidas:** Algunas imágenes no obtuvieron una descripción debido a errores intermitentes de la API. Se necesita un script de `retry_descriptions.py` para reintentar solo estas imágenes fallidas de manera eficiente.
