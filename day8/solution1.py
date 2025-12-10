#!/usr/bin/env python3

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

Point = Tuple[int, int, int]


def read_points(path: str) -> List[Point]:
    points: List[Point] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 3:
                raise ValueError(f"Ligne invalide : {line!r}")
            x, y, z = map(int, parts)
            points.append((x, y, z))
    return points


def pair_dist2(a: Point, b: Point) -> int:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx * dx + dy * dy + dz * dz


def k_smallest_edges(points: List[Point], k: int) -> List[Tuple[int, int, int]]:
    """
    Retourne les k arêtes les plus courtes sous forme (dist2, i, j),
    ordonnées par distance croissante.
    """
    import heapq

    def generate_edges() -> Iterable[Tuple[int, int, int]]:
        n = len(points)
        for i in range(n):
            for j in range(i + 1, n):
                yield pair_dist2(points[i], points[j]), i, j

    # heapq.nsmallest garde un tas de taille k, sans stocker toutes les arêtes.
    edges = heapq.nsmallest(k, generate_edges(), key=lambda e: e[0])
    # Elles sont déjà triées par distance ascendante.
    return edges


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def product_of_top3(sizes: List[int]) -> int:
    sizes_sorted = sorted(sizes, reverse=True)
    while len(sizes_sorted) < 3:
        sizes_sorted.append(1)
    return sizes_sorted[0] * sizes_sorted[1] * sizes_sorted[2]


def solve(path: str, connections: int = 1000) -> int:
    points = read_points(path)
    if not points:
        return 0

    edges = k_smallest_edges(points, connections)
    dsu = DSU(len(points))

    # On applique les arêtes dans l'ordre croissant des distances.
    for _, i, j in edges:
        dsu.union(i, j)

    # Tailles finales des circuits.
    sizes: Dict[int, int] = {}
    for i in range(len(points)):
        r = dsu.find(i)
        sizes[r] = dsu.size[r]

    return product_of_top3(list(sizes.values()))


def main() -> None:
    # Pour l'énoncé réel : 1000 plus courtes connexions.
    print(solve("test_inputs.txt", connections=1000))


if __name__ == "__main__":
    main()
