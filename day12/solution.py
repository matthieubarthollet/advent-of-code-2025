#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Tuple, Set


# ======================
# CONFIG (change ici)
# ======================
INPUT_PATH = "inputs.txt"
# ======================


Coord = Tuple[int, int]


@dataclass(frozen=True)
class ShapeVariant:
    cells: Tuple[Coord, ...]   # coords normalisées (minx=miny=0)
    w: int
    h: int


def parse_input(path: str) -> Tuple[List[List[str]], List[Tuple[int, int, List[int]]]]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]

    shapes: List[List[str]] = []
    regions: List[Tuple[int, int, List[int]]] = []

    i = 0
    # Parse shapes until a region-like line WxH:
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # region?
        if ":" in line:
            left = line.split(":", 1)[0].strip()
            if "x" in left:
                break

        # shape header like "0:"
        if line.endswith(":") and line[:-1].strip().isdigit():
            i += 1
            rows: List[str] = []
            while i < len(lines) and lines[i].strip():
                rows.append(lines[i].strip())
                i += 1
            shapes.append(rows)
        else:
            i += 1

    # Parse regions
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or ":" not in line:
            continue
        left, right = line.split(":", 1)
        left = left.strip()
        right = right.strip()
        if "x" not in left:
            continue
        w_str, h_str = left.split("x")
        W, H = int(w_str), int(h_str)
        counts = [int(x) for x in right.split()] if right else []
        regions.append((W, H, counts))

    return shapes, regions


def shape_to_cells(shape_rows: List[str]) -> List[Coord]:
    cells: List[Coord] = []
    for y, row in enumerate(shape_rows):
        for x, ch in enumerate(row):
            if ch == "#":
                cells.append((x, y))
    return cells


def normalize(cells: List[Coord]) -> Tuple[Tuple[Coord, ...], int, int]:
    minx = min(x for x, _ in cells)
    miny = min(y for _, y in cells)
    norm = [(x - minx, y - miny) for x, y in cells]
    maxx = max(x for x, _ in norm)
    maxy = max(y for _, y in norm)
    return tuple(sorted(norm)), maxx + 1, maxy + 1


def rot90(cells: List[Coord]) -> List[Coord]:
    return [(y, -x) for x, y in cells]


def flip_x(cells: List[Coord]) -> List[Coord]:
    return [(-x, y) for x, y in cells]


def all_unique_variants(cells: List[Coord]) -> List[ShapeVariant]:
    seen: Set[Tuple[Coord, ...]] = set()
    variants: List[ShapeVariant] = []

    cur = cells
    for _ in range(4):
        for do_flip in (False, True):
            cand = flip_x(cur) if do_flip else cur
            norm_cells, w, h = normalize(cand)
            if norm_cells not in seen:
                seen.add(norm_cells)
                variants.append(ShapeVariant(norm_cells, w, h))
        cur = rot90(cur)

    return variants


def placement_masks_for_variant(W: int, H: int, v: ShapeVariant) -> List[int]:
    if v.w > W or v.h > H:
        return []
    masks: List[int] = []
    for oy in range(H - v.h + 1):
        for ox in range(W - v.w + 1):
            m = 0
            for (x, y) in v.cells:
                idx = (oy + y) * W + (ox + x)
                m |= 1 << idx
            masks.append(m)
    return masks


def build_placements(W: int, H: int, shapes: List[List[str]]) -> Tuple[List[List[int]], List[int]]:
    """
    placements[s] = all placements (bitmasks) for shape s (all rotations/flips)
    areas[s] = number of # in shape s
    """
    placements: List[List[int]] = []
    areas: List[int] = []
    for shape_rows in shapes:
        base_cells = shape_to_cells(shape_rows)
        areas.append(len(base_cells))
        variants = all_unique_variants(base_cells)

        ms: List[int] = []
        seen_m: Set[int] = set()
        for v in variants:
            for m in placement_masks_for_variant(W, H, v):
                if m not in seen_m:
                    seen_m.add(m)
                    ms.append(m)

        placements.append(ms)
    return placements, areas


def can_pack_region(W: int, H: int, placements: List[List[int]], counts: List[int], areas: List[int]) -> bool:
    n = len(placements)
    if len(counts) < n:
        counts = counts + [0] * (n - len(counts))
    if len(counts) > n:
        return False

    board_area = W * H
    needed_area = sum(counts[s] * areas[s] for s in range(n))
    if needed_area > board_area:
        return False

    for s, c in enumerate(counts):
        if c > 0 and not placements[s]:
            return False

    counts_t = tuple(counts)

    @lru_cache(maxsize=None)
    def dfs(occupied: int, remaining: Tuple[int, ...]) -> bool:
        if all(c == 0 for c in remaining):
            return True

        # MRV: pick shape with fewest valid placements
        best_s = -1
        best_opts: List[int] | None = None
        best_len = 10**18

        for s, c in enumerate(remaining):
            if c == 0:
                continue
            opts = [pm for pm in placements[s] if (pm & occupied) == 0]
            if not opts:
                return False
            if len(opts) < best_len:
                best_len = len(opts)
                best_s = s
                best_opts = opts
                if best_len == 1:
                    break

        assert best_s != -1 and best_opts is not None

        new_remaining = list(remaining)
        new_remaining[best_s] -= 1
        new_remaining_t = tuple(new_remaining)

        for pm in best_opts:
            if dfs(occupied | pm, new_remaining_t):
                return True

        return False

    return dfs(0, counts_t)


def main():
    shapes, regions = parse_input(INPUT_PATH)

    ok = 0
    for (W, H, counts) in regions:
        placements, areas = build_placements(W, H, shapes)
        if can_pack_region(W, H, placements, counts, areas):
            ok += 1

    print(ok)


if __name__ == "__main__":
    main()
