"""
solvers/fuerza_bruta.py
───────────────────────
Estrategia 1 – Fuerza Bruta.

Prueba todos los números del 1 al 9 en cada celda vacía SIN verificar
restricciones antes de continuar; la validación se hace después de
asignar cada valor. Es la estrategia más ineficiente porque explora
ramas inválidas durante mucho tiempo antes de descartarlas.

MODIFICACIÓN:
Se añade un contador de nodos (stats["nodos"]) que incrementa cada vez
que se intenta asignar un valor a una celda. Esto permite medir el tamaño
del espacio de búsqueda explorado por el algoritmo.
"""

from utils.validacion import encontrar_vacio


# ─── Validación post-asignación (exclusiva de Fuerza Bruta) ───────────────

def _es_valido_fb(tablero: list[list[int]], fila: int, col: int, num: int) -> bool:
    """
    Comprueba fila, columna y caja DESPUÉS de que 'num' ya fue colocado
    en tablero[fila][col], por lo que excluye la celda actual de la revisión.
    """
    # Fila (excluir celda actual)
    for c in range(9):
        if c != col and tablero[fila][c] == num:
            return False

    # Columna (excluir celda actual)
    for r in range(9):
        if r != fila and tablero[r][col] == num:
            return False

    # Subcuadrícula 3×3
    box_fila = (fila // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_fila, box_fila + 3):
        for c in range(box_col, box_col + 3):
            if (r != fila or c != col) and tablero[r][c] == num:
                return False

    return True


# ─── Solver principal ─────────────────────────────────────────────────────

def solve_sudoku_FB(tablero: list[list[int]], stats: dict) -> bool:
    """
    Resuelve el Sudoku por Fuerza Bruta.

    Itera recursivamente sobre cada celda vacía, asigna cada valor [1-9]
    sin filtrado previo y valida sólo después de la asignación.

    Retorna True si encontró solución (tablero modificado in-place),
    False en caso contrario.
    """
    celda = encontrar_vacio(tablero)
    if celda is None:
        return True  # Sin celdas vacías → tablero completo

    fila, col = celda

    for num in range(1, 10):
        # Conteo de nodos (intentos de asignación)
        stats["nodos"] += 1

        tablero[fila][col] = num  # Asigna sin validar primero

        if _es_valido_fb(tablero, fila, col, num):
            if solve_sudoku_FB(tablero, stats):
                return True

        tablero[fila][col] = 0  # Retrocede

    return False
