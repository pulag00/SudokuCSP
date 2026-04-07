"""
utils/
──────
Módulos de soporte compartidos por los tres solvers.

  tablero    – lectura, copia e impresión del tablero
  validacion – es_valido() y encontrar_vacio()
"""

from .tablero import (
    TABLERO_DEFAULT,
    leer_tablero_desde_archivo,
    cargar_tablero,
    imprimir_tablero,
    copiar_tablero,
)
from .validacion import es_valido, encontrar_vacio

__all__ = [
    "TABLERO_DEFAULT",
    "leer_tablero_desde_archivo",
    "cargar_tablero",
    "imprimir_tablero",
    "copiar_tablero",
    "es_valido",
    "encontrar_vacio",
]
