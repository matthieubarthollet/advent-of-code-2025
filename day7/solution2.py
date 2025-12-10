#!/usr/bin/env python3

from __future__ import annotations

from typing import Dict, List, Tuple

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


def count_timelines(grid: Grid) -> int:
    """
    Many-worlds : chaque splitter duplique le faisceau en deux timelines.
    On propage ligne par ligne un dictionnaire colonne -> nombre de timelines.
    Les timelines qui sortent de la grille sont comptabilisées comme terminées.
    """

    start_row, start_col = find_start(grid)
    height = len(grid)
    width = len(grid[0])

    active: Dict[int, int] = {start_col: 1}  # colonne -> nb de timelines
    finished = 0

    for row in range(start_row + 1, height):
        next_active: Dict[int, int] = {}

        for col, count in active.items():
            # Faisceaux déjà sortis de la grille.
            if col < 0 or col >= width:
                finished += count
                continue

            cell = grid[row][col]
            if cell == "^":
                # Split : la timeline se duplique à gauche et à droite.
                for dest in (col - 1, col + 1):
                    next_active[dest] = next_active.get(dest, 0) + count
            else:
                next_active[col] = next_active.get(col, 0) + count

        active = next_active

        if not active:
            break  # plus aucune timeline active

    # Toutes les timelines restantes quittent la grille vers le bas.
    finished += sum(active.values())
    return finished


def main() -> None:
    grid = read_grid("inputs.txt")
    print(count_timelines(grid))


if __name__ == "__main__":
    main()
