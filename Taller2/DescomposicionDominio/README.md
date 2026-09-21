# Procesamiento de Imágenes: Secuencial vs. Descomposición por Dominio

Este proyecto compara dos formas de convertir un conjunto de imágenes a escala de
grises: una implementación **secuencial** y una implementación **paralela** basada
en **descomposición por dominio** (usando `multiprocessing.Pool`).

## Estructura del proyecto

```
.
├── DescomposicionSecuencial.py   # Procesa las imágenes una por una
├── DescomposicionDominio.py      # Procesa las imágenes en paralelo (Pool.map)
└── imagenes_prueba/              # Directorio con las imágenes de entrada
    ├── imagen1.png
    ├── imagen1 copy.png
    ├── imagen1 copy 2.png
    ├── ...
    └── imagen1 copy 18.png
```

## Requisitos

- Python 3.x
- Pillow

```bash
pip install Pillow
```

## Ejecución

**Versión secuencial:**

```bash
python DescomposicionSecuencial.py
```

**Versión paralela (descomposición por dominio):**

```bash
python DescomposicionDominio.py
```

Cada script mide y muestra en consola el tiempo total de procesamiento, para poder
compararlos entre sí.

## ⚠️ Importante: limpieza entre ejecuciones

Ambos scripts guardan la imagen resultante **en el mismo directorio** de la imagen
original (`imagenes_prueba/`), agregando el sufijo `_gris` al nombre del archivo
(ej. `imagen1_gris.png`), ya que **no se implementó el guardado en un directorio de
salida separado**.

Esto significa que, después de correr cualquiera de los dos scripts, el directorio
`imagenes_prueba/` quedará mezclado con:

- Las imágenes originales (`imagen1.png`, `imagen1 copy.png`, etc.)
- Las imágenes generadas (`imagen1_gris.png`, `imagen1 copy_gris.png`, etc.)

Si no se eliminan las imágenes `_gris` generadas antes de volver a ejecutar un
script (o antes de ejecutar el otro para comparar tiempos), pueden ocurrir dos
problemas:

1. **Se vuelven a procesar** las imágenes `_gris` ya generadas en ejecuciones
   posteriores (porque quedan dentro de `imagenes_prueba/` y el script las vuelve a
   listar), aumentando artificialmente el número de imágenes procesadas y
   distorsionando la comparación de tiempos.
2. **Se generan imágenes gris de imágenes gris** (ej. `imagen1_gris_gris.png`), lo
   cual ensucia el directorio.

### Cómo limpiar antes de cada prueba

En Windows (PowerShell), desde la carpeta `imagenes_prueba`:

```powershell
Remove-Item *_gris*
```

En Linux/Mac:

```bash
rm imagenes_prueba/*_gris*
```

**Recomendación:** ejecutar este comando de limpieza antes de cada corrida (o antes
de alternar entre la versión secuencial y la paralela) para asegurar que ambos
scripts procesen exactamente el mismo conjunto de imágenes de entrada y la
comparación de tiempos sea justa.
