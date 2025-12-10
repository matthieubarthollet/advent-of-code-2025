#!/usr/bin/env python3

from __future__ import annotations

import re
from fractions import Fraction
from typing import List, Tuple


def parse_machine(line: str) -> Tuple[List[List[int]], List[int], List[int]]:
    """
    Retourne (matrix, target, buttons) pour un automate.
    matrix : liste de lignes, chaque colonne correspond à un bouton (0/1).
    target : vecteur des exigences de tension.
    buttons : liste de listes d'indices de compteurs pour chaque bouton.
    """
    line = line.strip()
    if not line:
        raise ValueError("Ligne vide")

    # Schéma des compteurs à atteindre
    match_target = re.search(r"\{([^}]*)\}", line)
    if not match_target:
        raise ValueError(f"Exigences manquantes dans la ligne : {line!r}")
    target = [int(x.strip()) for x in match_target.group(1).split(",") if x.strip()]
    n = len(target)

    # Boutons
    buttons: List[List[int]] = []
    for m in re.finditer(r"\(([^)]*)\)", line):
        content = m.group(1).strip()
        if not content:
            idxs: List[int] = []
        else:
            idxs = [int(x.strip()) for x in content.split(",") if x.strip()]
        buttons.append(idxs)

    m_cols = len(buttons)
    matrix: List[List[int]] = [[0] * m_cols for _ in range(n)]
    for j, idxs in enumerate(buttons):
        for idx in idxs:
            if idx < 0 or idx >= n:
                raise ValueError(f"Bouton {j} référence un compteur invalide : {idx}")
            matrix[idx][j] = 1

    return matrix, target, buttons


def rref(matrix: List[List[int]], target: List[int]):
    """Retourne la matrice augmentée réduite et les colonnes pivots, ou lève en cas d'incohérence."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    mat = [list(map(Fraction, matrix[i])) + [Fraction(target[i])] for i in range(rows)]

    pivot_cols: List[int] = []
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if mat[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        mat[r], mat[pivot] = mat[pivot], mat[r]
        pivot_val = mat[r][c]
        mat[r] = [x / pivot_val for x in mat[r]]

        for i in range(rows):
            if i == r:
                continue
            factor = mat[i][c]
            if factor == 0:
                continue
            mat[i] = [mat[i][k] - factor * mat[r][k] for k in range(cols + 1)]

        pivot_cols.append(c)
        r += 1

    for i in range(rows):
        if all(mat[i][c] == 0 for c in range(cols)) and mat[i][-1] != 0:
            raise ValueError("Système sans solution.")

    return mat, pivot_cols


def to_int(frac: Fraction) -> int:
    if frac.denominator != 1:
        raise ValueError("Solution non entière rencontrée.")
    return int(frac.numerator)


def build_solution_family(mat, pivot_cols, num_vars: int):
    """Construit base et coefficients (x = base + coeff * free) à partir de la RREF."""
    free_cols = [c for c in range(num_vars) if c not in pivot_cols]
    free_pos = {c: i for i, c in enumerate(free_cols)}
    f = len(free_cols)

    base: List[Fraction] = [Fraction(0) for _ in range(num_vars)]
    coeff: List[List[Fraction]] = [[Fraction(0) for _ in range(f)] for _ in range(num_vars)]

    for free_col, k in free_pos.items():
        coeff[free_col][k] = Fraction(1)

    for row_idx, pivot_col in enumerate(pivot_cols):
        rhs = mat[row_idx][-1]
        base[pivot_col] = rhs
        for free_col, k in free_pos.items():
            coeff[pivot_col][k] = -mat[row_idx][free_col]

    return base, coeff, free_cols


def compute_bounds(
    base: List[int],
    coeff: List[List[int]],
    free_cols: List[int],
    max_press: List[int],
) -> List[Tuple[int, int]]:
    """Borne triviale : [0, max_press] pour chaque variable libre."""
    return [(0, max_press[free_var]) for free_var in free_cols]


def min_presses(matrix: List[List[int]], target: List[int], buttons: List[List[int]]) -> int:
    """
    Résout min somme(x_j) avec A x = target, x_j >= 0 (entiers).
    On exploite le fait qu'il y a peu de variables libres (<= 3 d'après les données).
    """
    if not matrix:
        return 0

    mat_rref, pivot_cols = rref(matrix, target)
    num_vars = len(buttons)
    base, coeff, free_cols = build_solution_family(mat_rref, pivot_cols, num_vars)

    f = len(free_cols)
    if f == 0:
        if any(v < 0 for v in base):
            raise ValueError("Solution négative trouvée.")
        return sum(base)

    # Borne de pressions pour chaque bouton : il est impossible d'appuyer
    # plus que la plus petite exigence des compteurs affectés par ce bouton.
    max_press = []
    for idxs in buttons:
        max_press.append(min(target[i] for i in idxs) if idxs else 0)

    bounds = compute_bounds(base, coeff, free_cols, max_press)

    # Coefficients pour la fonction coût : total = base_total + sum cost_coeff[k] * t_k
    base_total: Fraction = sum(base)
    cost_coeff: List[Fraction] = [Fraction(0) for _ in range(f)]
    for k in range(f):
        total = Fraction(0)
        for var_idx in range(num_vars):
            total += coeff[var_idx][k]
        cost_coeff[k] = total

    best: int | None = None
    current: List[Fraction] = base[:]
    assigned: List[int] = [0] * f

    def dfs(idx: int, partial_cost: int) -> None:
        nonlocal best
        if idx == f:
            if any(v < 0 for v in current):
                return
            if any(v.denominator != 1 for v in current):
                return
            presses_int = sum(int(v) for v in current)
            if best is None or presses_int < best:
                best = presses_int
            return

        # Optimistic borne pour pruner : on peut réduire le coût si le coefficient est négatif.
        optimistic: Fraction = partial_cost
        for k2 in range(idx, f):
            if cost_coeff[k2] < 0:
                optimistic += cost_coeff[k2] * bounds[k2][1]
        if best is not None and optimistic >= best:
            return

        lb, ub = bounds[idx]
        free_var = free_cols[idx]
        for val in range(lb, ub + 1):
            assigned[idx] = val
            # Met à jour les variables en fonction de cette valeur.
            for var_idx in range(num_vars):
                current[var_idx] += coeff[var_idx][idx] * val

            # Prune simple : si une variable est déjà négative et qu'aucune
            # variable libre restante ne peut l'augmenter, on arrête ici.
            invalid = False
            for var_idx in range(num_vars):
                if current[var_idx] < 0:
                    can_fix = any(
                        coeff[var_idx][k] > 0 for k in range(idx + 1, f)
                    )
                    if not can_fix:
                        invalid = True
                        break
            if not invalid:
                new_cost = partial_cost + cost_coeff[idx] * val
                dfs(idx + 1, new_cost)

            # Backtrack
            for var_idx in range(num_vars):
                current[var_idx] -= coeff[var_idx][idx] * val

    dfs(0, base_total)
    if best is None:
        raise ValueError("Impossible de configurer cette machine.")
    return best


def solve(path: str) -> int:
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            matrix, target, buttons = parse_machine(line)
            total += min_presses(matrix, target, buttons)
    return total


def main() -> None:
    print(solve("inputs.txt"))


if __name__ == "__main__":
    main()
