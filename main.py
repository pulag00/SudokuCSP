"""
=============================================================
  Introducción a la Inteligencia Artificial - Proyecto 2
  Tema: Problema de Satisfacción de Restricciones (CSP)
  Problema: Solución de Sudoku
=============================================================
  Estrategias implementadas:
    1. Fuerza Bruta
    2. Backtracking básico
    3. Backtracking con Forward Checking (+ heurística MRV)
=============================================================

Uso:
    python main.py                  → tablero por defecto
    python main.py mi_sudoku.txt    → lee tablero desde archivo
"""

import copy
import sys
import time

from solvers import solve_sudoku_FB, solve_sudoku_BT, solve_sudoku_FC
from utils import cargar_tablero, copiar_tablero, imprimir_tablero, TABLERO_DEFAULT


def ejecutar_solver(nombre: str, funcion, tablero_base: list[list[int]]) -> tuple[float, int]:
    """
    Ejecuta un solver, mide el tiempo y cuenta los nodos explorados.

    Retorna:
        (tiempo, nodos)
    """
    tablero = copiar_tablero(tablero_base)
    stats = {"nodos": 0}  # 🔥 contador limpio

    print(f"\n  Ejecutando: {nombre}")

    inicio = time.perf_counter()
    resultado = funcion(tablero, stats)  # 👈 ahora recibe stats
    fin = time.perf_counter()

    elapsed = fin - inicio

    if resultado:
        imprimir_tablero(tablero, f"Solución – {nombre}")
        print(f"   Tiempo: {elapsed:.6f} segundos")
        print(f"   Nodos explorados: {stats['nodos']}")
    else:
        print(f"   No se encontró solución  ({elapsed:.6f} s)")

    return elapsed, stats["nodos"]


def main() -> None:
    ruta_archivo = sys.argv[1] if len(sys.argv) > 1 else None

    print("\n" + "="*50)
    print("   SUDOKU CSP – Comparación de Estrategias")
    print("="*50)

    try:
        tablero_original = cargar_tablero(ruta_archivo)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n   Error al leer el tablero: {e}")
        print("  Se usará el tablero por defecto.\n")
        tablero_original = copy.deepcopy(TABLERO_DEFAULT)

    imprimir_tablero(tablero_original, "Tablero Inicial")

    solvers = [
        ("Fuerza Bruta",                          solve_sudoku_FB),
        ("Backtracking Básico",                   solve_sudoku_BT),
        ("Backtracking + Forward Checking (MRV)", solve_sudoku_FC),
    ]

    resultados = {
        nombre: ejecutar_solver(nombre, funcion, tablero_original)
        for nombre, funcion in solvers
    }

    # ── Resumen comparativo ───────────────────────────────────────────────
    print("\n" + "="*50)
    print("   RESUMEN COMPARATIVO")
    print("="*50)
    print(f"  {'Estrategia':<38} {'Tiempo (s)':>12} {'Nodos':>12}")
    print(f"  {'-'*38} {'-'*12} {'-'*12}")

    for nombre, (tiempo, nodos) in resultados.items():
        print(f"  {nombre:<38} {tiempo:>12.6f} {nodos:>12}")

    # Comparación por tiempo
    mas_rapido = min(resultados, key=lambda x: resultados[x][0])
    mas_lento = max(resultados, key=lambda x: resultados[x][0])

    factor = (
        resultados[mas_lento][0] / resultados[mas_rapido][0]
        if resultados[mas_rapido][0] > 0 else float("inf")
    )

    print(f"\n  Más rápido (tiempo): {mas_rapido}")
    print(f"  Más lento  (tiempo): {mas_lento}")

    print(f"  Factor de mejora (tiempo): {factor:.1f}×")

    print("="*50 + "\n")


if __name__ == "__main__":
    main()
