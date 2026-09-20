import time
import concurrent.futures


N = 20# Cantidad de números de Fibonacci a calcular


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def calcular_fibonacci_paralelo(n_elementos, executor_type):
    inicio = time.perf_counter()
    with executor_type() as executor:
   
        resultados = list(executor.map(fibonacci, range(n_elementos)))

    fin = time.perf_counter()
    tiempo_ejecucion = fin - inicio

    print(f"Fibonacci ({n_elementos} términos):")
    for i, valor in enumerate(resultados):
        print(f"  F({i}) = {valor}")

    print(f"\nExecutor: {executor_type.__name__}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")

    return resultados, tiempo_ejecucion


if __name__ == "__main__":
    print("=== ThreadPoolExecutor ===")
    calcular_fibonacci_paralelo(N, concurrent.futures.ThreadPoolExecutor)

    print("\n=== ProcessPoolExecutor ===")
    calcular_fibonacci_paralelo(N, concurrent.futures.ProcessPoolExecutor)