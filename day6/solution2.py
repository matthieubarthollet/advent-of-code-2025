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


def parse_worksheet_right_to_left(lines: List[str]) -> Tuple[List[int], int]:
    """
    Version Partie 2 : on lit les colonnes de droite à gauche.

    Chaque colonne fournit un nombre (en concaténant les digits
    de haut en bas en ignorant les espaces). On groupe les colonnes
    jusqu'à tomber sur un opérateur sur la dernière ligne du bloc.
    L'opérateur rencontré s'applique à tous les nombres accumulés
    depuis la colonne de droite précédente.
    """
    while lines and lines[-1].strip() == "":
        lines.pop()

    if not lines:
        return [], 0

    width = max(len(line) for line in lines)
    grid = [line.ljust(width) for line in lines]
    op_row = len(grid) - 1

    results: List[int] = []
    grand_total = 0

    current_numbers: List[int] = []

    for col in range(width - 1, -1, -1):
        # Construire le nombre pour cette colonne
        digits = "".join(grid[r][col] for r in range(op_row) if grid[r][col] != " ")
        if digits:
            current_numbers.append(int(digits))

        # Si on tombe sur un opérateur, on clôt le problème courant
        op_char = grid[op_row][col].strip()
        if op_char:
            op = op_char[0]
            if not current_numbers:
                continue  # pas de nombres à traiter

            if op == "+":
                value = sum(current_numbers)
            elif op == "*":
                value = 1
                for n in current_numbers:
                    value *= n
            else:
                raise ValueError(f"Opération inconnue : {op!r} (colonne {col})")

            results.append(value)
            grand_total += value
            current_numbers = []

    # En théorie, il ne devrait rien rester, sinon on pourrait décider de l'ignorer
    return results, grand_total


def main():
    lines = read_input_file("inputs.txt")
    worksheets = split_into_blocks(lines)

    all_results: List[int] = []
    global_total = 0

    for ws_lines in worksheets:
        results, total = parse_worksheet_right_to_left(ws_lines)
        all_results.extend(results)
        global_total += total

    print(global_total)
    # Pour debug :
    # print("Résultats individuels :", all_results)
    # print("Grand total global :", global_total)


if __name__ == "__main__":
    main()
