#!/usr/bin/env python3

from typing import List, Tuple


def read_input_file(path: str) -> List[str]:
    """
    Lit le fichier d'entrée et retourne une liste de lignes
    en conservant les espaces (on enlève seulement le '\n').
    """
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def split_into_blocks(lines: List[str]) -> List[List[str]]:
    """
    Sépare le fichier en blocs (worksheets) séparés par
    au moins une ligne vide.
    """
    blocks: List[List[str]] = []
    current: List[str] = []

    for line in lines:
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)

    if current:
        blocks.append(current)

    return blocks


def parse_worksheet(lines: List[str]) -> Tuple[List[int], int]:
    """
    Analyse une seule "worksheet" (une grille).

    Chaque "problème" est un bloc de colonnes non vides, séparé par
    au moins une colonne de spaces. La dernière ligne du bloc contient
    l'opération (+ ou *), les lignes au-dessus contiennent les nombres.
    """

    # On enlève d'éventuelles lignes vides en bas du bloc
    while lines and lines[-1].strip() == "":
        lines.pop()

    if not lines:
        return [], 0

    # Normaliser les lignes (même longueur, padding avec des espaces)
    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]
    rows, cols = len(grid), width

    # Trouver les blocs de colonnes correspondant à chaque problème
    blocks = []
    in_block = False
    start = None

    for c in range(cols):
        col_is_empty = all(grid[r][c] == " " for r in range(rows))
        if col_is_empty:
            if in_block:
                blocks.append((start, c - 1))
                in_block = False
        else:
            if not in_block:
                start = c
                in_block = True

    if in_block:
        blocks.append((start, cols - 1))

    results: List[int] = []
    grand_total = 0

    # La dernière ligne est celle des opérations
    op_row = rows - 1

    for c1, c2 in blocks:
        # Opération sur la dernière ligne du bloc
        op_segment = grid[op_row][c1 : c2 + 1].strip()
        if not op_segment:
            continue
        op = op_segment[0]

        # Lire les nombres (toutes les lignes sauf la dernière)
        nums: List[int] = []
        for r in range(rows - 1):
            seg = grid[r][c1 : c2 + 1].strip()
            if seg:  # si non vide, c'est un nombre
                # En cas de caractères bizarres, ça lèvera une ValueError
                nums.append(int(seg))

        if not nums:
            continue

        if op == "+":
            value = sum(nums)
        elif op == "*":
            value = 1
            for n in nums:
                value *= n
        else:
            raise ValueError(f"Opération inconnue : {op!r} (bloc colonnes {c1}-{c2})")

        results.append(value)
        grand_total += value

    return results, grand_total


def main():
    # Adapte le nom du fichier si besoin
    lines = read_input_file("inputs.txt")

    # On gère le cas où il y aurait plusieurs grilles dans le même fichier
    worksheets = split_into_blocks(lines)

    all_results: List[int] = []
    global_total = 0

    for ws_index, ws_lines in enumerate(worksheets):
        results, total = parse_worksheet(ws_lines)
        all_results.extend(results)
        global_total += total

    # Pour AoC généralement on ne veut que le total final :
    print(global_total)

    # Si tu veux débugguer, tu peux décommenter :
    # print("Résultats individuels :", all_results)
    # print("Grand total global :", global_total)


if __name__ == "__main__":
    main()
