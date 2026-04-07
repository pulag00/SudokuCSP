"""
utils/tablero.py
────────────────
Lectura, copia y visualización del tablero de Sudoku.
"""

import copy
import os
import re


# Tablero por defecto (usado si no se proporciona un archivo)
TABLERO_DEFAULT = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0],
]


def leer_tablero_desde_archivo(ruta: str) -> list[list[int]]:
    """
    Lee un tablero de Sudoku desde un archivo .txt con formato de matriz Python.

    Formato esperado (una fila por línea, con corchetes):
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        ...

    Los ceros representan celdas vacías.
    Retorna la matriz 9×9 o lanza un error si el archivo no es válido.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: '{ruta}'")

    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()

    filas_encontradas = re.findall(r'\[([0-9,\s]+)\]', contenido)

    tablero = []
    for fila_str in filas_encontradas:
        numeros = [int(n.strip()) for n in fila_str.split(",") if n.strip()]
        if len(numeros) == 9:
            if any(v < 0 or v > 9 for v in numeros):
                raise ValueError(f"Valor fuera del rango 0-9 en: {numeros}")
            tablero.append(numeros)

    if len(tablero) != 9:
        raise ValueError(
            f"Se esperaban 9 filas en el archivo, pero se encontraron {len(tablero)}.\n"
            f"  Formato requerido por fila: [0, 0, 3, 0, 2, 0, 6, 0, 0],"
        )

    return tablero


def cargar_tablero(ruta_archivo: str | None = None) -> list[list[int]]:
    """
    Devuelve el tablero a usar:
      - Si se proporciona una ruta, lo lee desde el archivo.
      - Si no, usa el tablero por defecto.
    """
    if ruta_archivo:
        print(f"\n  Leyendo tablero desde: {ruta_archivo}")
        tablero = leer_tablero_desde_archivo(ruta_archivo)
        print("  Archivo leído correctamente.")
        return tablero

    print("\n  ℹ  No se proporcionó archivo. Usando tablero por defecto.")
    return copy.deepcopy(TABLERO_DEFAULT)


def imprimir_tablero(tablero: list[list[int]], titulo: str = "Tablero") -> None:
    """Imprime el tablero con separadores visuales para subcuadrículas."""
    print(f"\n{'═'*37}")
    print(f"  {titulo}")
    print(f"{'═'*37}")
    for i, fila in enumerate(tablero):
        if i % 3 == 0 and i != 0:
            print("  ------+-------+------")
        fila_str = "  "
        for j, val in enumerate(fila):
            if j % 3 == 0 and j != 0:
                fila_str += "| "
            fila_str += (str(val) if val != 0 else ".") + " "
        print(fila_str)
    print(f"{'═'*37}\n")


def copiar_tablero(tablero: list[list[int]]) -> list[list[int]]:
    """Devuelve una copia profunda del tablero."""
    return copy.deepcopy(tablero)
