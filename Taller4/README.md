# Arquitecturas SMP y SIMD con Python

Taller de infraestructura paralela. Se comparan dos formas de paralelismo sobre cálculos con matrices:

- **SMP (Symmetric Multiprocessing):** varios hilos que comparten la misma memoria y se reparten el trabajo.
- **SIMD (Single Instruction, Multiple Data):** una instrucción que opera sobre varios datos a la vez (NumPy).

## Contenido

| Ejercicio | Descripción |
|---|---|
| 1. SMP | Suma de una matriz de 1000x1000 dividida en 100 bloques de 100x100, repartidos entre hilos con `ThreadPoolExecutor`. Se compara contra la versión secuencial. |
| 2. SIMD | Multiplicación de dos matrices de 1000x1000 con NumPy (`@`) frente a un bucle tradicional de tres ciclos en Python. |
| Integrador | Sistema híbrido SMP + SIMD: matriz de 10000x10000 en bloques de 1000x1000, un hilo por bloque, y dentro de cada hilo la suma se hace con NumPy. |

El notebook es `ArquitectuaSMP_SMD.ipynb`.

## Dónde ejecutarlo (importante)

**Se recomienda ejecutar el código en Visual Studio Code, en el equipo local, y no en Google Colab.**

Colab gratuito solo ofrece **2 núcleos** de CPU. Con tan pocos núcleos el paralelismo casi no se nota: en el ejercicio integrador la aceleración con hilos apenas llega a ~1.15x, mientras que en un equipo con más núcleos se observa una mejora mucho mayor (por ejemplo, cerca de 2.4x con 4 hilos). Además, los tiempos en Colab varían más entre corridas porque los núcleos se comparten con otras máquinas virtuales.

Para ver bien los beneficios del paralelismo:

1. Ejecuta el código en VS Code, en tu propio equipo.
2. Revisa cuántos núcleos tiene con `os.cpu_count()`.
3. Ajusta el número de hilos a ese valor (el máximo de aceleración teórico es igual al número de núcleos).
4. Repite cada medición varias veces y toma el mejor tiempo.

## Requisitos

- Python 3.9 o superior
- NumPy
- Matplotlib (opcional, solo si se grafica el Ejercicio 2)

## Configuración del entorno en VS Code (Linux)

```bash
cd "ruta/de/la/carpeta"
python3 -m venv .venv
source .venv/bin/activate
pip install numpy matplotlib
```

En Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install numpy matplotlib
```

En VS Code, elige el intérprete de `.venv` con `Ctrl+Shift+P` > **Python: Select Interpreter**.

## Cómo ejecutar

Cada ejercicio se puede guardar en un archivo `.py` y correr con:

```bash
python nombre_del_archivo.py
```

También se puede abrir el notebook directamente en VS Code (extensión Jupyter) y ejecutar las celdas en orden.

## Tiempos esperados

| Ejercicio | Tiempo aproximado |
|---|---|
| 1. SMP (suma con ciclos de Python puro) | menos de 1 segundo |
| 2. SIMD (bucle de Python con 1000x1000) | entre 8 y 30 minutos |
| 2. SIMD (NumPy con 1000x1000) | 1 a 3 segundos |
| Integrador | menos de 1 minuto |

El bucle del Ejercicio 2 hace mil millones de operaciones en Python puro. Para probar rápido, cambia el tamaño `n` de 1000 a 100.

## Resultados y conclusiones

- **Ejercicio 1:** los hilos no aceleran porque la suma usa ciclos de Python puro y el **GIL** permite que solo un hilo ejecute código Python a la vez.
- **Ejercicio 2:** NumPy fue unas 178 veces más rápido que el bucle (2.77 s frente a 492.70 s). El algoritmo es O(n³) en ambos casos; NumPy reduce el costo de cada operación al usar código compilado en C, datos contiguos en memoria e instrucciones vectoriales.
- **Integrador:** al usar `.sum()` de NumPy dentro de cada hilo, el GIL se libera y los hilos sí trabajan en paralelo. La aceleración depende del número de núcleos y del ancho de banda de la memoria, por eso con 2 núcleos (Colab) la mejora es pequeña.

## Notas

- Las matrices se generan sin semilla, por lo que las sumas totales cambian entre ejecuciones. Lo importante es que la versión secuencial y la paralela coincidan.
- Los bloques de la matriz son vistas de NumPy, no copias, así que no se duplica memoria.
- La matriz de 10000x10000 en `int64` ocupa unos 800 MB; revisa que tu equipo tenga memoria suficiente.
