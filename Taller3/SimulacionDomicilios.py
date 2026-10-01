import random
import threading
import time

NUM_PEDIDOS = 400      # cuantos pedidos simulamos
ESPERA = 0.05          # lo que tarda cada consulta al servicio (50 milisegundos)
MAX_CONSULTAS = 8      # el servicio solo aguanta 8 consultas al tiempo

# Punto de referencia (latitud, longitud) de cada zona del sur de Cali
ZONAS = {
    "Valle del Lili": (3.37085, -76.52066),
    "El Caney": (3.38324, -76.51847),
    "Capri": (3.38705, -76.53924),
    "Limonar": (3.39827, -76.53871),
    "Ciudad Jardín": (3.36136, -76.53133),
    "Pance": (3.32834, -76.63865),
}


# ---------------------------------------------------------------
# Datos de prueba (inventados)
# ---------------------------------------------------------------
def crear_pedidos(cantidad):
    azar = random.Random(7)   # semilla fija: siempre salen los mismos pedidos
    pedidos = []
    for i in range(cantidad):
        zona = azar.choice(list(ZONAS))
        direccion = "Carrera " + str(azar.randint(60, 125)) + " # " + \
                    str(azar.randint(1, 40)) + "-" + str(azar.randint(1, 99)) + \
                    ", " + zona + ", Cali"
        pedidos.append((direccion, zona))
    return pedidos


def geocodificar(direccion, zona):
    # Simula la consulta al servicio de mapas: espera y devuelve coordenadas
    time.sleep(ESPERA)
    azar = random.Random(direccion)   # la misma direccion da siempre lo mismo
    lat_base, lon_base = ZONAS[zona]
    lat = lat_base + azar.uniform(-0.005, 0.005)
    lon = lon_base + azar.uniform(-0.005, 0.005)
    return lat, lon


# ---------------------------------------------------------------
# MAP: lo que hace cada hilo con su grupo de pedidos
# ---------------------------------------------------------------
def map_function(grupo, resultados, posicion, semaforo):
    sumas = {}   # para cada zona: cuantos pedidos, suma de latitudes, suma de longitudes
    for direccion, zona in grupo:
        with semaforo:   # maximo 8 hilos consultando al tiempo
            lat, lon = geocodificar(direccion, zona)
        if zona not in sumas:
            sumas[zona] = {"cantidad": 0, "suma_lat": 0.0, "suma_lon": 0.0}
        sumas[zona]["cantidad"] += 1
        sumas[zona]["suma_lat"] += lat
        sumas[zona]["suma_lon"] += lon
    # Cada hilo guarda su resultado en SU propio puesto de la lista,
    # asi nunca dos hilos escriben en el mismo lugar.
    resultados[posicion] = sumas


# ---------------------------------------------------------------
# REDUCE: junta las sumas de todos los hilos
# ---------------------------------------------------------------
def reduce_function(lista_de_sumas):
    total = {}
    for sumas in lista_de_sumas:
        for zona, datos in sumas.items():
            if zona not in total:
                total[zona] = {"cantidad": 0, "suma_lat": 0.0, "suma_lon": 0.0}
            total[zona]["cantidad"] += datos["cantidad"]
            total[zona]["suma_lat"] += datos["suma_lat"]
            total[zona]["suma_lon"] += datos["suma_lon"]
    return total


def calcular_centros(total):
    # Promedio = suma / cantidad
    centros = {}
    for zona, datos in total.items():
        centros[zona] = {
            "lat": datos["suma_lat"] / datos["cantidad"],
            "lon": datos["suma_lon"] / datos["cantidad"],
            "pedidos": datos["cantidad"],
        }
    return centros


# ---------------------------------------------------------------
# Las dos formas de correr el programa
# ---------------------------------------------------------------
def sin_hilos(pedidos):
    resultados = [None]
    map_function(pedidos, resultados, 0, threading.Semaphore(1))
    return calcular_centros(reduce_function(resultados))


def con_hilos(pedidos, num_hilos):
    # 1. Partir los pedidos en grupos del mismo tamano
    tamano = len(pedidos) // num_hilos
    grupos = []
    for i in range(num_hilos):
        grupos.append(pedidos[i * tamano:(i + 1) * tamano])
    grupos[-1].extend(pedidos[num_hilos * tamano:])   # lo que sobre va al ultimo grupo

    # 2. Crear y arrancar un hilo por grupo
    semaforo = threading.Semaphore(MAX_CONSULTAS)
    resultados = [None] * num_hilos
    hilos = []
    for i in range(num_hilos):
        hilo = threading.Thread(target=map_function,
                                args=(grupos[i], resultados, i, semaforo))
        hilos.append(hilo)
        hilo.start()

    # 3. Esperar a que todos terminen antes de juntar los resultados
    for hilo in hilos:
        hilo.join()

    return calcular_centros(reduce_function(resultados))


def son_iguales(a, b):
    for zona in a:
        if round(a[zona]["lat"], 6) != round(b[zona]["lat"], 6):
            return False
        if round(a[zona]["lon"], 6) != round(b[zona]["lon"], 6):
            return False
        if a[zona]["pedidos"] != b[zona]["pedidos"]:
            return False
    return True


# ---------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------
def main():
    pedidos = crear_pedidos(NUM_PEDIDOS)
    print(NUM_PEDIDOS, "pedidos en el sur de Cali")
    print("Cada consulta tarda", int(ESPERA * 1000), "ms y el servicio aguanta",
          MAX_CONSULTAS, "consultas al tiempo\n")

    inicio = time.perf_counter()
    referencia = sin_hilos(pedidos)
    tiempo_sin_hilos = time.perf_counter() - inicio

    print("Version             Tiempo (s)   Veces mas rapido   Mismo resultado")
    print("Sin hilos           %8.2f            1.00            -" % tiempo_sin_hilos)

    for num_hilos in (2, 4, 8, 16):
        inicio = time.perf_counter()
        centros = con_hilos(pedidos, num_hilos)
        tiempo = time.perf_counter() - inicio
        print("%2d hilos            %8.2f         %6.2f            %s" %
              (num_hilos, tiempo, tiempo_sin_hilos / tiempo,
               "Si" if son_iguales(referencia, centros) else "NO"))

    print("\nCentro sugerido para el punto de despacho de cada zona:")
    print("Zona              Latitud     Longitud    Pedidos")
    for zona in sorted(centros):
        c = centros[zona]
        print("%-15s %9.5f   %10.5f   %6d" % (zona, c["lat"], c["lon"], c["pedidos"]))


if __name__ == "__main__":
    main()
