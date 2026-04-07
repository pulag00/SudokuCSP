"""
utils/validacion.py
───────────────────
Funciones de validación y búsqueda compartidas por los tres solvers.
"""


def es_valido(tablero: list[list[int]], fila: int, col: int, num: int) -> bool:
    """
    Verifica si 'num' puede colocarse en (fila, col) sin violar las
    restricciones de fila, columna y subcuadrícula 3×3.
    """
    # Restricción de fila
    if num in tablero[fila]:
        return False

    # Restricción de columna
    if num in [tablero[r][col] for r in range(9)]:
        return False

    # Restricción de subcuadrícula 3×3
    box_fila = (fila // 3) * 3
    box_col  = (col  // 3) * 3
    for r in range(box_fila, box_fila + 3):
        for c in range(box_col, box_col + 3):
            if tablero[r][c] == num:
                return False

    return True


def encontrar_vacio(tablero: list[list[int]]) -> tuple[int, int] | None:
    """Devuelve la posición (fila, col) de la primera celda vacía (valor 0)."""
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                return i, j
    return None
