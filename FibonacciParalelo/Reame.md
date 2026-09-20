# Fibonacci en paralelo

Este programa calcula los primeros 20 números de Fibonacci usando
`concurrent.futures` para repartir el trabajo entre varios hilos o
procesos.

## Cómo correrlo

```
python3 fibonacci_paralelo.py
```

Se ejecuta primero con `ThreadPoolExecutor` y luego con
`ProcessPoolExecutor`, para poder comparar los tiempos.

## ¿Qué parte se paraleliza?

El ciclo que manda a calcular cada número de Fibonacci sí se puede
paralelizar, porque calcular `fibonacci(3)` no depende para nada de
calcular `fibonacci(7)`. Son cálculos independientes, así que se pueden
repartir entre varios hilos/procesos sin problema. Para esto usé
`executor.map()`, que además tiene la ventaja de devolver los
resultados en el mismo orden en que se pidieron.

## ¿Qué parte NO se paraleliza?

La impresión de los resultados. Si cada hilo imprimiera su resultado
apenas termina, el orden saldría mezclado (los números chicos se
calculan más rápido que los grandes, entonces saldrían primero aunque
no sean los primeros de la lista). Por eso primero se guardan todos los
resultados y al final se imprimen todos juntos, en orden, de una sola
vez.

Un error común (que casi cometo) es usar `as_completed()` junto con
`enumerate()` para ir guardando los resultados. Eso suena bien pero en
realidad numera los resultados según el orden en que van *terminando*
las tareas, no según el número que se les pidió calcular. Con pocos
números no se nota mucho, pero la lista puede salir desordenada.
`executor.map()` evita ese problema.

## Threads vs Procesos

Con N = 20 me dio esto:

- ThreadPoolExecutor: ~0.002 s
- ProcessPoolExecutor: ~0.009 s
