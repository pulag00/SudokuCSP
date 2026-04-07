"""
solvers/forward_checking.py
────────────────────────────
Estrategia 3 – Backtracking + Forward Checking + Heurística MRV.

Al asignar un valor propaga la restricción hacia los vecinos (elimina
el valor de sus dominios). Si algún dominio queda vacío, la rama se
descarta sin explorarla. La heurística MRV elige siempre la celda con
menos opciones disponibles, maximizando la poda.

MODIFICACIÓN:
Se añade un contador de nodos (stats["nodos"]) que incrementa cada vez
que se intenta asignar un valor a una celda. Esto permite medir el tamaño
del espacio de búsqueda explorado por el algoritmo.
"""

from utils.validacion import es_valido


# ─── Inicialización de dominios ───────────────────────────────────────────

def inicializar_dominios(tablero: list[list[int]]) -> dict:
    """
    Construye el diccionario de dominios: para cada celda (i, j) calcula
    el conjunto de valores [1-9] posibles dado el estado actual del tablero.
    Las celdas ya asignadas tienen un dominio unitario con su valor fijo.
    """
    dominios = {}
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                dominios[(i, j)] = {
                    num for num in range(1, 10)
                    if es_valido(tablero, i, j, num)
                }
            else:
                dominios[(i, j)] = {tablero[i][j]}
    return dominios


# ─── Vecindad ─────────────────────────────────────────────────────────────

def obtener_vecinos(fila: int, col: int) -> set[tuple[int, int]]:
    """
    Devuelve el conjunto de celdas que comparten fila, columna o
    subcuadrícula con (fila, col), excluyendo la celda misma.
    """
    vecinos: set[tuple[int, int]] = set()

    for k in range(9):
        if k != col:
            vecinos.add((fila, k))
        if k != fila:
            vecinos.add((k, col))

    box_f = (fila // 3) * 3
    box_c = (col // 3) * 3
    for r in range(box_f, box_f + 3):
        for c in range(box_c, box_c + 3):
            if (r, c) != (fila, col):
                vecinos.add((r, c))

    return vecinos


# ─── Heurística MRV ───────────────────────────────────────────────────────

def seleccionar_variable_mrv(
    dominios: dict, tablero: list[list[int]]
) -> tuple[int, int] | None:
    """
    Heurística MRV (Minimum Remaining Values): selecciona la celda vacía
    con el dominio más pequeño para reducir el factor de ramificación.
    """
    celdas_vacias = [
        (celda, len(dom))
        for celda, dom in dominios.items()
        if tablero[celda[0]][celda[1]] == 0
    ]
    if not celdas_vacias:
        return None
    return min(celdas_vacias, key=lambda x: x[1])[0]


# ─── Propagación de restricciones ─────────────────────────────────────────

def forward_checking(
    dominios: dict, fila: int, col: int, num: int
) -> tuple[bool, list]:
    """
    Después de asignar 'num' a (fila, col), elimina 'num' del dominio de
    todos sus vecinos no asignados.

    Retorna (éxito, modificados):
      - éxito      : False si algún dominio queda vacío (rama inviable).
      - modificados: lista de (celda, num) para poder deshacer los cambios.
    """
    modificados = []
    for vecino in obtener_vecinos(fila, col):
        if num in dominios[vecino]:
            dominios[vecino].discard(num)
            modificados.append((vecino, num))
            if len(dominios[vecino]) == 0:
                return False, modificados  # Dominio vacío → rama sin solución
    return True, modificados


def deshacer_forward_checking(dominios: dict, modificados: list) -> None:
    """Restaura los dominios eliminados durante un forward checking fallido."""
    for celda, num in modificados:
        dominios[celda].add(num)


# ─── Solver principal ─────────────────────────────────────────────────────

def solve_sudoku_FC(
    tablero: list[list[int]],
    stats: dict,
    dominios: dict | None = None
) -> bool:
    """
    Resuelve el Sudoku con Backtracking + Forward Checking + MRV.

    Al asignar un valor propaga la restricción a los vecinos y descarta
    la rama si algún dominio queda vacío. Usa MRV para elegir siempre
    la celda con menos opciones, maximizando la poda.

    Retorna True si encontró solución (tablero y dominios modificados
    in-place), False si no hay solución.
    """
    if dominios is None:
        dominios = inicializar_dominios(tablero)

    celda = seleccionar_variable_mrv(dominios, tablero)
    if celda is None:
        return True  # Todas las celdas asignadas → solución

    fila, col = celda

    for num in list(dominios[(fila, col)]):
        # Conteo de nodos (intentos de asignación)
        stats["nodos"] += 1

        if es_valido(tablero, fila, col, num):
            # Asignar
            tablero[fila][col] = num
            dominio_original = dominios[(fila, col)].copy()
            dominios[(fila, col)] = {num}

            # Propagar restricciones
            exito, modificados = forward_checking(dominios, fila, col, num)

            if exito and solve_sudoku_FC(tablero, stats, dominios):
                return True

            # Deshacer (backtrack)
            deshacer_forward_checking(dominios, modificados)
            dominios[(fila, col)] = dominio_original
            tablero[fila][col] = 0

    return False
