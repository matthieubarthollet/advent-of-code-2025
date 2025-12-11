#!/usr/bin/env python3
import sys
from functools import lru_cache


START_NODE = "svr"
END_NODE = "out"
MUST_VISIT_1 = "dac"
MUST_VISIT_2 = "fft"


def read_graph(path: str):
    """
    Lit un fichier de lignes du type :
      aaa: bbb ccc
      svr: aaa bbb
    et renvoie un dict:
      { 'aaa': ['bbb', 'ccc'], 'svr': ['aaa', 'bbb'], ... }
    """
    graph = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Couper une seule fois sur ":"
            parts = line.split(":", 1)
            if len(parts) != 2:
                continue  # ligne invalide, on ignore
            left, right = parts
            src = left.strip()
            targets = right.strip().split() if right.strip() else []
            graph[src] = targets

    return graph


def count_paths(graph):
    """
    Retourne (total_paths, good_paths) où :
      - total_paths = nombre de chemins de START_NODE à END_NODE
      - good_paths  = parmi eux, ceux qui passent par MUST_VISIT_1 et MUST_VISIT_2
    """

    # bitmask : bit 0 pour MUST_VISIT_1, bit 1 pour MUST_VISIT_2
    special_index = {
        MUST_VISIT_1: 0,
        MUST_VISIT_2: 1,
    }
    ALL_MASK = (1 << len(special_index)) - 1  # ici 0b11

    @lru_cache(maxsize=None)
    def dfs(node: str, mask: int):
        # Mettre à jour le masque si on est sur un noeud spécial
        if node in special_index:
            mask |= (1 << special_index[node])

        # arrivé à la sortie
        if node == END_NODE:
            total = 1
            good = 1 if mask == ALL_MASK else 0
            return total, good

        # pas de sorties
        if node not in graph:
            return 0, 0

        total_paths = 0
        good_paths = 0

        for nxt in graph[node]:
            t, g = dfs(nxt, mask)
            total_paths += t
            good_paths += g

        return total_paths, good_paths

    return dfs(START_NODE, 0)

def main():
    input_path = "inputs.txt"  

    graph = read_graph(input_path)

    total, good = count_paths(graph)

    print(total)
    print(good)


if __name__ == "__main__":
    main()
