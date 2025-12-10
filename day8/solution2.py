#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

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


def dist2(a: Point, b: Point) -> int:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx * dx + dy * dy + dz * dz


@dataclass
class Edge:
    d2: int
    i: int
    j: int


def all_edges(points: List[Point]) -> List[Edge]:
    n = len(points)
    edges: List[Edge] = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append(Edge(dist2(points[i], points[j]), i, j))
    edges.sort(key=lambda e: e.d2)
    return edges


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


def solve(path: str) -> int:
    points = read_points(path)
    if not points:
        return 0

    edges = all_edges(points)
    dsu = DSU(len(points))

    last_edge: Edge | None = None
    for e in edges:
        merged = dsu.union(e.i, e.j)
        if merged:
            last_edge = e
            if dsu.components == 1:
                break

    if last_edge is None:
        return 0  # rien à connecter

    # Produit des X des deux boîtes reliées par la dernière connexion.
    x1 = points[last_edge.i][0]
    x2 = points[last_edge.j][0]
    return x1 * x2


def main() -> None:
    print(solve("inputs.txt"))


if __name__ == "__main__":
    main()
