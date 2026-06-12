#  Pipeline de Datos: Análisis del Catálogo de Netflix

Este proyecto implementa un pipeline de datos (ETL) automatizado en Python para la ingesta, limpieza, validación y carga del catálogo de películas y series de Netflix. El objetivo es transformar datos brutos en un conjunto de datos consistente, limpio y listo para el análisis de negocio.

##  Integrantes
* Ignacio Meneses
* Julian Valencia
* Angelo Medina

---

##  Arquitectura y Flujo del Pipeline

El pipeline está diseñado siguiendo una arquitectura modular por etapas consecutivas, garantizando la trazabilidad de los datos y el manejo controlado de anomalías.

[Datos Brutos] -> 1. ingesta.py (Guarda en /data/raw/) -> 2. limpieza.py (Guarda en /data/clean/) -> 3. validacion.py (Separa en /validated/ o /errors/) -> 4. carga.py (Guarda en /data/validated/)

###  Estructura del Proyecto
* **ingesta.py**: Conecta a la fuente de datos externa o simula la recepción del archivo original, guardándolo directamente en la zona de aterrizaje (`/data/raw/`).
* **limpieza.py**: Trata valores faltantes, elimina duplicados, estandariza formatos de fechas y limpia campos de texto. Exporta a `/data/clean/`.
* **validacion.py**: Ejecuta reglas de calidad de datos (Data Quality Checks). Si un registro no cumple los criterios lógicos o de tipo, se desvía a `/data/errors/` para su auditoría; los registros correctos pasan a `/data/validated/`.
* **carga.py**: Toma los datos consolidados y los prepara para su consumo final por herramientas de analítica o almacenamiento definitivo.

---

##  Instrucciones de Ejecución

Para correr el pipeline completo de principio a fin, asegúrate de tener instaladas las dependencias necesarias (`pandas`, etc.) y ejecuta los scripts en el orden del flujo de datos:

1. Etapa de Ingesta: `python ingesta.py`
2. Etapa de Limpieza: `python limpieza.py`
3. Etapa de Validación: `python validacion.py`
4. Etapa de Carga Final: `python carga.py`

---

##  Decisiones Técnicas y Justificaciones

1. **Modularidad Estricta:** Separar el pipeline en 4 scripts independientes facilita el mantenimiento del código, el aislamiento de errores y permite escalar o modificar cada fase de manera independiente en el futuro sin afectar el resto del sistema.
2. **Estrategia de Aislamiento de Datos (/data/):** Al mantener las carpetas raw, clean, validated y errors totalmente separadas, nos aseguramos de no corromper la fuente original de los datos y mantenemos un registro histórico claro de qué filas fallaron y por qué.
3. **Manejo de Errores Mediante Logs:** Cada módulo escribe eventos clave en archivos .log. Esto permite monitorear la salud del pipeline en entornos de producción sin necesidad de revisar el código internamente o depender de impresiones temporales en consola.
