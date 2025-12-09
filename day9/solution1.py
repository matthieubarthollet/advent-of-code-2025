#!/usr/bin/env python3
import sys


def read_points(path: str):
    """Lit les points 'x,y' ligne par ligne depuis un fichier."""
    points = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # chaque ligne est de la forme "7,1"
            x_str, y_str = line.split(",")
            points.append((int(x_str), int(y_str)))
    return points


def max_rectangle_area(points):
    """
    Calcule l'aire maximale d'un rectangle dont deux coins opposés
    sont des tuiles rouges (points de la liste).
    
    Aire = (|x1 - x2| + 1) * (|y1 - y2| + 1)
    (on compte les tuiles, donc bornes inclusives)
    """
    max_area = 0
    best_pair = None

    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]

            # Largeur et hauteur en nombre de tuiles (inclusives)
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height

            if area > max_area:
                max_area = area
                best_pair = (points[i], points[j])

    return max_area, best_pair


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "inputs.txt"

    points = read_points(path)
    if not points:
        print("Aucun point trouvé dans le fichier.")
        return

    max_area, best_pair = max_rectangle_area(points)

    # Pour le puzzle, tu peux ne garder que l'aire si tu veux.
    print(max_area)
    # Si tu veux aussi voir quels coins donnent cette aire, décommente :
    # print("Meilleurs coins :", best_pair)


if __name__ == "__main__":
    main()
