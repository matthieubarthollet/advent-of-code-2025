#!/usr/bin/env python3

from bisect import bisect_right
from typing import List, Tuple


def parse_input(path: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    """
    Lit le fichier d'entrée.
    Format attendu :

        <ranges>
        a-b
        c-d
        ...

        <ligne vide>

        <ids>
        x
        y
        ...

    Retourne :
    - ranges: liste de (start, end)
    - ids: liste d'entiers
    """
    with open(path, "r", encoding="utf-8") as f:
        # strip() enlève espaces, \n, \r...
        lines = [line.strip() for line in f]

    ranges: List[Tuple[int, int]] = []
    ids: List[int] = []

    parsing_ranges = True

    for line in lines:
        if line == "":
            parsing_ranges = False
            continue

        if parsing_ranges:
            # Ligne de type "start-end"
            if "-" in line:
                parts = line.split("-")
                if len(parts) == 2:
                    start_str, end_str = parts[0].strip(), parts[1].strip()
                    if start_str.isdigit() and end_str.isdigit():
                        ranges.append((int(start_str), int(end_str)))
                    # sinon on ignore la ligne silencieusement
        else:
            # Partie IDs : une valeur par ligne
            s = line.strip()
            if s.isdigit():
                ids.append(int(s))
            # sinon on ignore la ligne

    return ranges, ids


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Fusionne les intervalles qui se chevauchent ou se touchent.

    Exemple :
        [(3, 5), (10, 14), (16, 20), (12, 18)]
    =>    [(3, 5), (10, 20)]
    """
    if not ranges:
        return []

    ranges.sort(key=lambda r: r[0])

    merged: List[Tuple[int, int]] = []
    current_start, current_end = ranges[0]

    for start, end in ranges[1:]:
        if start <= current_end + 1:  # chevauchement ou adjacent
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    merged.append((current_start, current_end))
    return merged


def build_search_struct(merged: List[Tuple[int, int]]):
    """
    Prépare une structure pour la recherche avec bisect.
    """
    starts = [s for s, _ in merged]
    return starts, merged


def is_fresh_fast(x: int, starts: List[int], merged: List[Tuple[int, int]]) -> bool:
    """
    Vérifie si x est dans un intervalle fusionné, en O(log n).
    """
    if not merged:
        return False

    idx = bisect_right(starts, x) - 1
    if idx < 0:
        return False

    start, end = merged[idx]
    return start <= x <= end


def count_fresh_ids_fast(ranges: List[Tuple[int, int]], ids: List[int]) -> int:
    """
    Version optimisée : merge + recherche binaire.
    """
    merged = merge_ranges(ranges)
    starts, merged = build_search_struct(merged)

    count = 0
    for x in ids:
        if is_fresh_fast(x, starts, merged):
            count += 1
    return count


def count_fresh_ids_naive(ranges: List[Tuple[int, int]], ids: List[int]) -> int:
    """
    Version naïve : pour chaque ID, on parcourt tous les ranges.
    O(N * M), mais très bien pour debug / fichiers ~1000 lignes.
    """
    def is_fresh_naive(x: int) -> bool:
        for start, end in ranges:
            if start <= x <= end:
                return True
        return False

    return sum(1 for x in ids if is_fresh_naive(x))


def main():
    ranges, ids = parse_input("inputs.txt")

    # Calcul naïf (de référence)
    naive_result = count_fresh_ids_naive(ranges, ids)
    print(f"Résultat naïf      (lent mais sûr) : {naive_result}")

    # Calcul optimisé
    fast_result = count_fresh_ids_fast(ranges, ids)
    print(f"Résultat optimisé (merge + bisect) : {fast_result}")


if __name__ == "__main__":
    main()
