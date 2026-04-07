"""
solvers/backtracking.py
───────────────────────
Estrategia 2 – Backtracking Básico.

Verifica la validez ANTES de continuar la recursión: si un número no
cumple las restricciones, se descarta de inmediato sin profundizar.
Significativamente más eficiente que Fuerza Bruta porque poda ramas
inválidas al instante.

MODIFICACIÓN:
Se añade un contador de nodos (stats["nodos"]) que incrementa únicamente
cuando un valor válido es asignado a una celda. Esto representa mejor
los nodos realmente explorados en el espacio de búsqueda del CSP.
"""

from utils.validacion import es_valido, encontrar_vacio


def solve_sudoku_BT(tablero: list[list[int]], stats: dict) -> bool:
    """
    Resuelve el Sudoku mediante Backtracking básico.

    Para cada celda vacía prueba los valores [1-9]; sólo avanza en la
    recursión si el valor cumple las restricciones de fila, columna y
    subcuadrícula. Si ningún valor funciona, retrocede (backtrack).


    Se incrementa stats["nodos"] únicamente cuando se realiza una
    asignación válida, lo que representa un nodo expandido en el árbol
    de búsqueda.

    Retorna True si encontró solución (tablero modificado in-place),
    False en caso contrario.
    """
    celda = encontrar_vacio(tablero)
    if celda is None:
        return True  # Tablero completo → solución encontrada

    fila, col = celda

    for num in range(1, 10):
        if es_valido(tablero, fila, col, num):  # Poda temprana
            # Conteo SOLO de asignaciones válidas
            stats["nodos"] += 1

            tablero[fila][col] = num

            if solve_sudoku_BT(tablero, stats):
                return True

            tablero[fila][col] = 0  # Deshacer (backtrack)

    return False  # Ningún número válido → retroceder
