#!/usr/bin/env python3
import sys

# ------------------------------------------------------------
# Lecture des points rouges
# ------------------------------------------------------------

def read_red_points(path: str):
    pts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x_str, y_str = line.split(",")
            pts.append((int(x_str), int(y_str)))
    return pts

# ------------------------------------------------------------
# Construction des arêtes du polygone
# ------------------------------------------------------------

def build_edges(red_points):
    """
    Construit les arêtes du polygone reliant les points rouges dans l'ordre.
    Retourne:
      - edges: liste de (x1, y1, x2, y2)
      - vertical_edges: liste de (x, y1, y2) avec y1 < y2
      - horizontal_edges: liste de (x1, x2, y) avec x1 < x2
    """
    n = len(red_points)
    edges = []
    vertical_edges = []
    horizontal_edges = []

    for i in range(n):
        x1, y1 = red_points[i]
        x2, y2 = red_points[(i + 1) % n]

        edges.append((x1, y1, x2, y2))

        if x1 == x2:  # vertical
            if y1 < y2:
                vertical_edges.append((x1, y1, y2))
            else:
                vertical_edges.append((x1, y2, y1))
        elif y1 == y2:  # horizontal
            if x1 < x2:
                horizontal_edges.append((x1, x2, y1))
            else:
                horizontal_edges.append((x2, x1, y1))
        else:
            # L'énoncé garantit que ce n'est pas censé arriver :
            raise ValueError(
                f"Arête non axis-alignée entre {red_points[i]} et {red_points[(i+1)%n]}"
            )

    return edges, vertical_edges, horizontal_edges

# ------------------------------------------------------------
# Test point sur le bord du polygone
# ------------------------------------------------------------

def point_on_boundary(x, y, edges):
    """
    Retourne True si (x,y) est exactement sur une arête du polygone
    (y compris aux sommets).
    """
    for (x1, y1, x2, y2) in edges:
        if x1 == x2:  # vertical
            if x == x1 and min(y1, y2) <= y <= max(y1, y2):
                return True
        elif y1 == y2:  # horizontal
            if y == y1 and min(x1, x2) <= x <= max(x1, x2):
                return True
    return False

# ------------------------------------------------------------
# Test point dans polygone (inside ou sur le bord)
# ------------------------------------------------------------

def build_point_in_polygon_fn(edges, vertical_edges):
    """
    Construit une fonction is_inside(x, y) qui teste si (x,y) est dans
    le polygone ou sur son bord.

    On sépare:
      - test "sur le bord" (vertical + horizontal),
      - test "inside" par ray casting utilisant seulement les arêtes verticales.
    """

    def is_inside(x, y, cache):
        # cache est un dict {(x,y): bool}
        key = (x, y)
        if key in cache:
            return cache[key]

        # 1) Sur le bord ?
        if point_on_boundary(x, y, edges):
            cache[key] = True
            return True

        # 2) Ray casting vers +infini en x, en utilisant les arêtes verticales
        crossings = 0
        for vx, vy1, vy2 in vertical_edges:
            if vy1 <= y < vy2 and vx > x:
                crossings += 1

        inside = (crossings % 2 == 1)
        cache[key] = inside
        return inside

    return is_inside

# ------------------------------------------------------------
# Test si le rectangle croise le bord du polygone (vraie intersection)
# ------------------------------------------------------------

def build_rect_crosses_polygon_fn(vertical_edges, horizontal_edges):
    """
    Construit une fonction rect_crosses_polygon(left, right, top, bottom)
    qui teste si le rectangle [left,right] x [top,bottom] (bords compris)
    a un bord qui coupe le bord du polygone en un point strictement intérieur
    aux deux segments (les coïncidences sur les coins / le bord sont autorisées).
    """

    def rect_crosses_polygon(left, right, top, bottom):
        # On considère uniquement les croisements "vrai" entre
        # un segment vertical et un segment horizontal.
        # Les segments colinéaires ne sont pas traités comme des croisements
        # (on autorise le rectangle à être collé au bord).

        # 1) Croisements potentiels : arêtes verticales du polygone
        #    avec les bords horizontaux du rectangle (top et bottom).
        if top != bottom:
            for vx, vy1, vy2 in vertical_edges:
                if left < vx < right:
                    if vy1 < top < vy2:
                        return True
                    if vy1 < bottom < vy2:
                        return True
        else:
            # Rectangle de hauteur 1 (top == bottom): seul bord horizontal,
            # on teste aussi, même logique (croisement au milieu).
            y = top
            for vx, vy1, vy2 in vertical_edges:
                if left < vx < right and vy1 < y < vy2:
                    return True

        # 2) Croisements potentiels : arêtes horizontales du polygone
        #    avec les bords verticaux du rectangle (left et right).
        if left != right:
            for hx1, hx2, hy in horizontal_edges:
                if top < hy < bottom:
                    if hx1 < left < hx2:
                        return True
                    if hx1 < right < hx2:
                        return True
        else:
            # Rectangle de largeur 1 (left == right)
            x = left
            for hx1, hx2, hy in horizontal_edges:
                if top < hy < bottom and hx1 < x < hx2:
                    return True

        return False

    return rect_crosses_polygon

# ------------------------------------------------------------
# Calcul du plus grand rectangle
# ------------------------------------------------------------

def max_rectangle_area_red_green(red_points):
    """
    Cherche le plus grand rectangle (aire en nombre de tuiles) tel que :
      - deux coins opposés sont des tuiles rouges,
      - toutes les tuiles du rectangle sont rouges ou vertes,
        c.-à-d. le rectangle est entièrement dans le polygone formé
        par les tuiles rouges connectées dans l'ordre par des segments
        horizontaux/verticaux.
    """
    n = len(red_points)
    if n == 0:
        return 0, None

    edges, vertical_edges, horizontal_edges = build_edges(red_points)
    is_inside = build_point_in_polygon_fn(edges, vertical_edges)
    rect_crosses_polygon = build_rect_crosses_polygon_fn(vertical_edges, horizontal_edges)

    # Cache pour les tests point-in-polygon des coins C et D
    pip_cache = {}

    max_area = 0
    best_pair = None

    # Red points pour accès direct
    # On ne considère que i < j (paires non ordonnées)
    for i in range(n):
        x1, y1 = red_points[i]
        for j in range(i + 1, n):
            x2, y2 = red_points[j]

            # Aire du rectangle en nombre de tuiles (inclusif)
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height

            # Petit prune
            if area <= max_area:
                continue

            # Coins du rectangle
            # A = (x1, y1) rouge
            # B = (x2, y2) rouge
            C = (x1, y2)
            D = (x2, y1)

            # C et D doivent être dans le polygone (ou sur le bord).
            if not is_inside(C[0], C[1], pip_cache):
                continue
            if not is_inside(D[0], D[1], pip_cache):
                continue

            # Bornes du rectangle (coordonnées originales)
            left = min(x1, x2)
            right = max(x1, x2)
            top = min(y1, y2)
            bottom = max(y1, y2)

            # Vérifier qu'aucun bord du rectangle ne coupe le bord du polygone
            if rect_crosses_polygon(left, right, top, bottom):
                continue

            # Rectangle valide
            max_area = area
            best_pair = ((x1, y1), (x2, y2))

    return max_area, best_pair

# ------------------------------------------------------------
# main
# ------------------------------------------------------------

def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "inputs.txt"

    red_points = read_red_points(path)
    if not red_points:
        print("Aucun point rouge trouvé.")
        return

    max_area, best_pair = max_rectangle_area_red_green(red_points)
    print(max_area)
    # debug éventuel :
    # print("Meilleurs coins rouges :", best_pair)


if __name__ == "__main__":
    main()
