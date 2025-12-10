#!/usr/bin/env python3

from __future__ import annotations

from collections import deque
from typing import List, Tuple


def parse_machine(line: str) -> Tuple[int, int, List[int]]:
    """
    Retourne (nb_lumières, masque_cible, liste_masks_boutons).
    Le texte dans {} est ignoré comme demandé.
    """
    line = line.strip()
    if not line:
        raise ValueError("Ligne vide inattendue")

    start = line.index("[")
    end = line.index("]", start)
    indicator = line[start + 1 : end]
    n = len(indicator)

    target_mask = 0
    for i, c in enumerate(indicator):
        if c == "#":
            target_mask |= 1 << i

    # Tous les schémas de boutons sont dans des parenthèses.
    buttons: List[int] = []
    tmp = line[end + 1 :]
    while True:
        left = tmp.find("(")
        if left == -1:
            break
        right = tmp.find(")", left)
        if right == -1:
            break
        content = tmp[left + 1 : right].strip()
        mask = 0
        if content:
            for val in content.split(","):
                val = val.strip()
                if val:
                    idx = int(val)
                    mask |= 1 << idx
        buttons.append(mask)
        tmp = tmp[right + 1 :]

    return n, target_mask, buttons


def min_presses(num_lights: int, target: int, buttons: List[int]) -> int:
    """
    BFS sur les états (bitmask) pour trouver le nombre minimal de pressions.
    Chaque bouton est un toggle (XOR) appliqué au masque courant.
    """
    if target == 0:
        return 0

    max_state = 1 << num_lights
    dist = [-1] * max_state
    dist[0] = 0

    queue: deque[int] = deque([0])
    while queue:
        state = queue.popleft()
        current = dist[state]

        for button in buttons:
            nxt = state ^ button
            if dist[nxt] != -1:
                continue
            next_cost = current + 1
            if nxt == target:
                return next_cost
            dist[nxt] = next_cost
            queue.append(nxt)

    return -1  # non atteignable, improbable avec les données fournies


def solve(path: str) -> int:
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            num_lights, target, buttons = parse_machine(line)
            presses = min_presses(num_lights, target, buttons)
            if presses == -1:
                raise ValueError(f"Configuration impossible pour la ligne : {line!r}")
            total += presses
    return total


def main() -> None:
    print(solve("inputs.txt"))


if __name__ == "__main__":
    main()
