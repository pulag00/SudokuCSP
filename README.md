# Sudoku CSP – Comparación de Estrategias de Búsqueda

## Descripción

Este proyecto implementa y compara tres estrategias clásicas de resolución de Sudoku modelado como un **Problema de Satisfacción de Restricciones (CSP)**:

| # | Estrategia | Descripción corta |
|---|-----------|-------------------|
| 1 | **Fuerza Bruta** | Asigna valores sin filtrado previo; valida solo después |
| 2 | **Backtracking Básico** | Poda ramas inválidas de inmediato antes de profundizar |
| 3 | **Backtracking + Forward Checking + MRV** | Propaga restricciones y elige la celda más restringida |

Al finalizar se muestra un **resumen comparativo** con tiempo de ejecución y nodos explorados por cada estrategia.


## Estructura del Proyecto

```
proyecto2/
│
├── main.py                  # Punto de entrada; orquesta los tres solvers
│
├── solvers/
│   ├── fuerza_bruta.py      # Estrategia 1 – Fuerza Bruta
│   ├── backtracking.py      # Estrategia 2 – Backtracking Básico
│   └── forward_checking.py  # Estrategia 3 – Forward Checking + MRV
│
└── utils/
    ├── tablero.py           # Lectura, copia e impresión del tablero
    └── validacion.py        # Validación de restricciones CSP compartida
```

## Uso

### Tablero por defecto

```bash
python main.py
```

### Tablero personalizado desde archivo

```bash
python main.py mi_sudoku.txt
```

**Formato del archivo `.txt`** (una fila por línea, con corchetes; `0` = celda vacía):

```
[0, 0, 3, 0, 2, 0, 6, 0, 0],
[9, 0, 0, 3, 0, 5, 0, 0, 1],
[0, 0, 1, 8, 0, 6, 4, 0, 0],
[0, 0, 8, 1, 0, 2, 9, 0, 0],
[7, 0, 0, 0, 0, 0, 0, 0, 8],
[0, 0, 6, 7, 0, 8, 2, 0, 0],
[0, 0, 2, 6, 0, 9, 5, 0, 0],
[8, 0, 0, 2, 0, 3, 0, 0, 9],
[0, 0, 5, 0, 1, 0, 3, 0, 0],
```

Si el archivo no se encuentra o tiene un formato incorrecto, se usa el **tablero por defecto** automáticamente.


##  Descripción de Estrategias

### 1. Fuerza Bruta (`fuerza_bruta.py`)

Prueba los valores del 1 al 9 en cada celda vacía **sin filtrar antes de asignar**. La validación ocurre *después* de colocar el número. Es la estrategia más ineficiente porque explora ramas inválidas durante mucho tiempo antes de descartarlas.

- **Conteo de nodos:** cada intento de asignación (válido o no) incrementa el contador.

### 2. Backtracking Básico (`backtracking.py`)

Verifica la validez **antes** de continuar la recursión. Si un número viola alguna restricción (fila, columna o subcuadrícula 3×3), se descarta de inmediato sin profundizar en esa rama.

- **Conteo de nodos:** solo las asignaciones válidas incrementan el contador, representando nodos realmente expandidos en el árbol de búsqueda.

### 3. Backtracking + Forward Checking + MRV (`forward_checking.py`)

Combina tres mejoras sobre el Backtracking básico:

- **Forward Checking:** al asignar un valor, elimina ese valor del dominio de todas las celdas vecinas. Si algún dominio queda vacío, la rama se descarta sin explorarla.
- **Heurística MRV** *(Minimum Remaining Values)*: en cada paso selecciona la celda vacía con **menos valores posibles**, maximizando la poda del árbol de búsqueda.
- **Dominios dinámicos:** mantiene y propaga un diccionario de dominios para cada celda; los deshace (backtrack) cuando una rama falla.

- **Conteo de nodos:** cada intento de asignación incrementa el contador.
