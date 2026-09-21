import time


# Tarea 1: leer el archivo completo
def leer_archivo(ruta_entrada):
    """Lee y devuelve el contenido completo del archivo de entrada."""
    with open(ruta_entrada, 'r') as f_in:
        return f_in.read()


# Tarea 2: dividir el contenido en líneas
def dividir_en_lineas(contenido):
    """Divide el contenido del archivo en una lista de líneas."""
    return contenido.splitlines()


# Tarea 3: limpiar una línea (quitar espacios al inicio/fin)
def limpiar_linea(linea):
    """Elimina los espacios en blanco al principio y al final de una línea."""
    return linea.strip()


# Tarea 4: convertir una línea a mayúsculas
def convertir_mayusculas(linea):
    """Convierte una línea de texto a mayúsculas."""
    return linea.upper()


# Tarea 5: escribir las líneas procesadas en el archivo de salida
def escribir_archivo(ruta_salida, lineas):
    """Escribe una lista de líneas en el archivo de salida, una por renglón."""
    with open(ruta_salida, 'w') as f_out:
        for linea in lineas:
            f_out.write(linea + '\n')


def procesar_texto_funcional(ruta_entrada, ruta_salida):
    """Procesa el archivo de texto aplicando cada transformación como una tarea separada."""
    try:
        contenido = leer_archivo(ruta_entrada)
        lineas = dividir_en_lineas(contenido)

        lineas_procesadas = []
        for linea in lineas:
            linea_limpia = limpiar_linea(linea)
            linea_mayusculas = convertir_mayusculas(linea_limpia)
            lineas_procesadas.append(linea_mayusculas)

        escribir_archivo(ruta_salida, lineas_procesadas)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_entrada}")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == '__main__':
    ruta_entrada = "texto_entrada.txt"
    ruta_salida = "texto_salida_funcional.txt"

    inicio = time.time()
    procesar_texto_funcional(ruta_entrada, ruta_salida)
    fin = time.time()

    print(f"Tiempo total de procesamiento funcional: {fin - inicio:.4f} segundos")
    print(f"Archivo procesado funcionalmente guardado en {ruta_salida}")