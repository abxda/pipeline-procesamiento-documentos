# Pipeline de Procesamiento de Documentos con IA v1.0

![Licencia](https://img.shields.io/badge/License-Apache_2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Framework](https://img.shields.io/badge/Framework-Ollama-lightgrey)

Este repositorio contiene un pipeline modular y resiliente para el procesamiento por lotes de grandes corpus de documentos. El sistema extrae texto e imágenes, utiliza modelos de IA multimodales a través de Ollama para generar descripciones de las imágenes, y ensambla los resultados en archivos Markdown enriquecidos.

Fue diseñado con una filosofía de **ingeniería de software robusta**, priorizando la trazabilidad, la capacidad de recuperación ante fallos y la mantenibilidad a largo plazo.

---

## Características Principales

- **Procesamiento Híbrido Inteligente:** Identifica automáticamente la mejor fuente de contenido, usando archivos DOCX para obtener texto de alta fidelidad y los PDF originales para extraer imágenes de máxima calidad.
- **Arquitectura Basada en Artefactos:** Cada paso del proceso genera archivos intermedios, permitiendo una depuración y re-ejecución granular.
- **Resiliencia y Reanudación:** Los trabajos largos pueden ser interrumpidos y reanudados sin perder el progreso. El guardado incremental de las descripciones de IA protege contra fallos de red o de la API.
- **Herramientas de Mantenimiento:** Incluye scripts dedicados para:
  - `resume_pipeline.py`: Continuar trabajos interrumpidos.
  - `repair_missing_text.py`: Realizar reparaciones "quirúrgicas" en artefactos de texto corruptos.
  - `retry_descriptions.py`: Reintentar de forma inteligente solo las descripciones de imágenes que fallaron.
- **Flexibilidad:** Capaz de procesar corpus con diversas estructuras de directorios, desde carpetas simples hasta esquemas complejos y anidados.
- **Documentación Completa:** Incluye un tutorial de uso, un manual de arquitectura y un registro de cambios detallado.

## Estado del Proyecto (v1.0)

Esta es la primera versión estable del pipeline. Ha sido probada con éxito en un corpus complejo de varios miles de páginas e imágenes.

**Limitaciones Conocidas / Próximos Pasos:**
- El sistema no procesa actualmente archivos comprimidos (`.zip`). La implementación de la descompresión automática es el siguiente paso planificado.

## Guía de Inicio Rápido

Para poner en marcha el pipeline, sigue estos pasos.

### 1. Prerrequisitos

- **Python 3.10+**
- **Ollama** instalado y en ejecución.
- Un modelo multimodal de Ollama descargado, ej: `ollama pull qwen2.5vl:7b`

### 2. Instalación

```bash
# 1. Clona este repositorio
# git clone https://github.com/abxda/pipeline-procesamiento-documentos.git
# cd pipeline-procesamiento-documentos

# 2. Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate  # En Linux/macOS
# .\venv\Scripts\activate   # En Windows

# 3. Instala las dependencias
pip install -r requirements.txt
```

### 3. Uso Básico

El script principal para procesar un corpus es `main_corpus.py`.

```bash
# Ejecuta el pipeline en tu directorio de corpus
python pipeline_documentos/main_corpus.py /ruta/a/tu/corpus
```

El sistema creará un nuevo directorio `corpus_processed_01` con todos los resultados.

Para conocer el uso de las demás herramientas (`resume`, `repair`, `retry`), consulta el [**TUTORIAL.md**](./TUTORIAL.md).

## Arquitectura

El sistema está diseñado con una arquitectura modular desacoplada. Para una explicación detallada de cada componente, sus responsabilidades y el flujo de datos, consulta el documento de [**ARQUITECTURA.md**](./ARQUITECTURA.md).

## Licencia

Este proyecto está licenciado bajo la Licencia Apache 2.0. Consulta el archivo [LICENSE](./LICENSE) para más detalles.
