from PIL import Image
import os
import time
from multiprocessing import Pool, cpu_count

def convertir_a_gris(ruta_imagen):
    """Convierte una imagen a escala de grises."""
    try:
        imagen = Image.open(ruta_imagen)
        imagen_gris = imagen.convert('L')  # 'L' representa escala de grises
        nombre_archivo, extension = os.path.splitext(ruta_imagen)
        ruta_gris = nombre_archivo + "_gris" + extension
        imagen_gris.save(ruta_gris)
        return f"Imagen convertida: {ruta_imagen} -> {ruta_gris}"
    except FileNotFoundError:
        return f"Error: No se encontró la imagen {ruta_imagen}"
    except Exception as e:
        return f"Error al procesar {ruta_imagen}: {e}"


def procesar_imagenes_paralelo(lista_imagenes, num_procesos=None):
    """
    Procesa una lista de imágenes en paralelo, dividiendo el
    dominio de datos (la lista de imágenes) entre varios procesos.
    """
    if num_procesos is None:
        num_procesos = cpu_count()

    with Pool(processes=num_procesos) as pool:
        # map reparte automáticamente los elementos de la lista
        # entre los procesos disponibles (descomposición por dominio)
        resultados = pool.map(convertir_a_gris, lista_imagenes)

    for resultado in resultados:
        print(resultado)


if __name__ == '__main__':
    directorio_imagenes = "imagenes_prueba"  # Reemplaza con el nombre de tu directorio
    lista_imagenes = [
        os.path.join(directorio_imagenes, f)
        for f in os.listdir(directorio_imagenes)
        if os.path.isfile(os.path.join(directorio_imagenes, f))
    ]

    inicio = time.time()
    procesar_imagenes_paralelo(lista_imagenes)
    fin = time.time()

    print(f"Tiempo total de procesamiento paralelo: {fin - inicio:.4f} segundos")