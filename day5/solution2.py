#!/usr/bin/env python3

from typing import List, Tuple


def parse_ranges_only(path: str) -> List[Tuple[int, int]]:
    """
    Lit uniquement la première section du fichier (les ranges),
    jusqu'à la première ligne vide.
    Chaque ligne doit être de la forme 'start-end'.
    """
    ranges: List[Tuple[int, int]] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                # On s'arrête à la première ligne vide
                break

            if "-" not in line:
                continue

            parts = line.split("-")
            if len(parts) != 2:
                continue

            start_str, end_str = parts[0].strip(), parts[1].strip()
            if not start_str.isdigit() or not end_str.isdigit():
                continue

            start = int(start_str)
            end = int(end_str)
            ranges.append((start, end))

    return ranges


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Fusionne les intervalles qui se chevauchent ou se touchent.

    Exemple :
        [(3, 5), (10, 14), (16, 20), (12, 18)]
    devient :
        [(3, 5), (10, 20)]
    """
    if not ranges:
        return []

    # Trier par début
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


def count_total_fresh_ids(ranges: List[Tuple[int, int]]) -> int:
    """
    Compte le nombre total d'IDs couverts par l'union des ranges.
    """
    merged = merge_ranges(ranges)
    total = 0
    for start, end in merged:
        total += (end - start + 1)
    return total


def main():
    # Adapte le nom du fichier si besoin : "inputs.txt" ou "input.txt"
    ranges = parse_ranges_only("inputs.txt")
    result = count_total_fresh_ids(ranges)
    print(result)


if __name__ == "__main__":
    main()
