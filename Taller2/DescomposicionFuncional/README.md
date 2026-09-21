# Procesamiento de un archivo de texto grande — Secuencial vs. Pipeline funcional

Este proyecto compara dos formas de procesar un archivo de texto grande aplicando
las mismas transformaciones: leer, dividir en líneas, limpiar (quitar espacios al
inicio/fin) y convertir a mayúsculas, escribiendo el resultado en un nuevo archivo.

## Archivos

| Archivo | Descripción |
|---|---|
| `procesar_secuencial.py` | Recorre el archivo una sola vez, todo inline (sin funciones propias por línea). Es la versión más rápida. |
| `procesar_funcional.py` | Descomposición funcional (pipeline): 5 tareas separadas (`leer_archivo`, `dividir_en_lineas`, `limpiar_linea`, `convertir_mayusculas`, `escribir_archivo`) orquestadas en `procesar_texto_funcional`. |
| `texto_entrada.txt` | Archivo de entrada de prueba (líneas con espacios extra y mezcla de mayúsculas/minúsculas). |
| `informe.pdf` / `informe.tex` | Informe con la explicación detallada de ambas soluciones, el análisis comparativo y las conclusiones. |

## Cómo ejecutar

Cada script se ejecuta de forma independiente y espera un archivo `texto_entrada.txt`
en el mismo directorio:

```bash
python3 procesar_secuencial.py
python3 procesar_funcional.py
```

Cada uno imprime el tiempo total de procesamiento y guarda su resultado en un
archivo de salida distinto (`texto_salida_secuencial.txt`,
`texto_salida_funcional.txt`).

## Resultados observados

Con un archivo de ~2.1 millones de líneas (~60 MB):

| Versión | Tiempo promedio | Relativo a secuencial |
|---|---|---|
| Secuencial | 0.0015 s | 1.0x |
| Pipeline (funcional) | 0.0020 s | ≈1.33x |

**Conclusión principal:** la descomposición funcional agrega un pequeño overhead
(≈13%) por las llamadas a función propias y la carga completa del archivo/listas
intermedias en memoria. Para archivos de este tamaño, esa diferencia es modesta y
puede justificarse por la mayor modularidad, legibilidad y capacidad de prueba que
ofrece separar el proceso en tareas independientes. Ver `informe.pdf` para el
análisis completo.