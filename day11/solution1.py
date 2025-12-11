#!/usr/bin/env python3
import sys
from functools import lru_cache


def read_graph(path: str):
    """
    Lit un fichier de lignes du type :
    aaa: you hhh
    you: bbb ccc
    ...
    et renvoie un dict { 'aaa': ['you', 'hhh'], ... }
    """
    graph = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # format: "source: dest1 dest2 dest3"
            left, right = line.split(":")
            src = left.strip()
            if right.strip() == "":
                targets = []
            else:
                targets = right.strip().split()
            graph[src] = targets
    return graph


def count_paths(graph, start="you", end="out"):
    """
    Compte le nombre de chemins distincts de start à end
    dans le graphe dirigé donné par 'graph'.
    """

    @lru_cache(maxsize=None)
    def dfs(node):
        # Arrivé à la sortie -> 1 chemin
        if node == end:
            return 1

        # Si le noeud n'a pas de sorties et n'est pas 'end'
        if node not in graph:
            return 0

        total = 0
        for nxt in graph[node]:
            total += dfs(nxt)
        return total

    return dfs(start)


def main():
    # Si aucun argument, on lit "input.txt" par défaut
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "inputs.txt"

    graph = read_graph(path)
    result = count_paths(graph, start="you", end="out")
    print(result)


if __name__ == "__main__":
    main()
