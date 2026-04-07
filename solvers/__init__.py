"""
solvers/
────────
Los tres solvers de Sudoku como módulos independientes.

  fuerza_bruta     – solve_sudoku_FB  (sin poda)
  backtracking     – solve_sudoku_BT  (poda temprana)
  forward_checking – solve_sudoku_FC  (FC + MRV)
"""

from .fuerza_bruta     import solve_sudoku_FB
from .backtracking     import solve_sudoku_BT
from .forward_checking import solve_sudoku_FC

__all__ = ["solve_sudoku_FB", "solve_sudoku_BT", "solve_sudoku_FC"]
