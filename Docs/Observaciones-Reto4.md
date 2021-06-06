# Análisis

## Autores :writing_hand:
* Hernán Buitrago
  * hf.buitrago10@uniandes.edu.co
  * 201512807

## Máquina :gear:

| | Máquina |
| --- | --- |
| Procesador | 2.6 GHz Dual-Core Intel Core i5 |
| Memoria | 8 GB 1600 MHz DDR3 |
| OS | MacOS Big Sur 11.3.1 |

## Tiempo :stopwatch:
Para la recolección de datos se promedió el tiempo de ejecución para cada requerimiento después de ser ejecutados 5 veces. La siguiente tabla muestra los resultados de las pruebas.

|  | Tiempo |
| --- | --- |
| __Carga de datos__ | 7231.251 [ms] |
| __Requerimiento 1__ | 965.693 [ms] |
| __Requerimiento 2__ | 217.302 [ms] |
| __Requerimiento 3__ | 982.437 [ms] |
| __Requerimiento 4__ | 1561.942 [ms] |
| __Requerimiento 5__ | 173.321 [ms] |

## Memoria :file_folder:
Para la recolección de datos se promedió la memoria asignada para cada requerimiento después de ser ejecutado 5 veces. La siguiente tabla muestra los resultados de las pruebas.

|  | Memoria |
| --- | --- |
| __Carga de datos__ | 12798.045 [kB] |
| __Requerimiento 1__ | 2765.181 [kB] |
| __Requerimiento 2__ | 135.532 [kB] |
| __Requerimiento 3__ | 2195.437 [kB] |
| __Requerimiento 4__ | 2379.815 [kB] |
| __Requerimiento 5__ | 1779.631 [kB] |

## Complejidad :chart_with_upwards_trend:
Se realizó un análisis de complejidad en el peor caso para cada requerimiento. La siguiente tabla muestra la complejidad temporal de cada requerimiento.

|  | Reto 4 |
| --- | --- |
| __Requerimiento 1__ | O(V + E) |
| __Requerimiento 2__ | O(V) |
| __Requerimiento 3__ | O(E log V) |
| __Requerimiento 4__ | O(E log V) |
| __Requerimiento 5__ | O(n) |
