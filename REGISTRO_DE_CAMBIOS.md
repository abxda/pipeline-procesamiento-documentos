# Registro de Cambios y Ejecuciones del Pipeline

## Desarrollo del Pipeline

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

## Historial de Ejecuciones

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

*(Aún no se han realizado ejecuciones)*
