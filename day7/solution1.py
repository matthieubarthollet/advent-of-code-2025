#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Set, Tuple

Grid = List[str]


def read_grid(path: str) -> Grid:
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def find_start(grid: Grid) -> Tuple[int, int]:
    for r, line in enumerate(grid):
        c = line.find("S")
        if c != -1:
            return r, c
    raise ValueError("Impossible de trouver S dans la grille")


def simulate_splits(grid: Grid) -> int:
    """
    Parcourt la grille ligne par ligne et compte les fois où un faisceau
    rencontre un splitter (^). Quand un splitter est rencontré, le faisceau
    s'arrête et deux nouveaux faisceaux partent immédiatement à gauche et à
    droite de ce splitter.
    """

    start_row, start_col = find_start(grid)
    height = len(grid)
    width = len(grid[0])

    # Ensemble des colonnes où un faisceau entre dans la ligne courante.
    active_cols: Set[int] = {start_col}
    split_count = 0

    # Le faisceau démarre sous le S, donc on commence à la ligne suivante.
    for row in range(start_row + 1, height):
        next_active: Set[int] = set()

        for col in active_cols:
            # Un faisceau qui sort du tableau disparaît.
            if col < 0 or col >= width:
                continue

            cell = grid[row][col]
            if cell == "^":
                split_count += 1  # un événement de split
                next_active.add(col - 1)
                next_active.add(col + 1)
            else:
                next_active.add(col)

        active_cols = next_active

        # Plus de faisceaux actifs : on peut sortir tôt.
        if not active_cols:
            break

    return split_count


def main() -> None:
    grid = read_grid("inputs.txt")
    print(simulate_splits(grid))


if __name__ == "__main__":
    main()
