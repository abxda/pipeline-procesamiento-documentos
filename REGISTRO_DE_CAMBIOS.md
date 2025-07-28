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

*(Aún no se han realizado ejecuciones)*
