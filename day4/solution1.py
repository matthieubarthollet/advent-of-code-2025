def find_accessible_rolls(grid_lines):
    # Grille d'origine, non modifiée pendant le calcul
    grid = [list(row) for row in grid_lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1),
    ]

    accessible_positions = []  # liste des (i, j) accessibles

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != '@':
                continue

            neighbors_at = 0
            for di, dj in directions:
                ni = i + di
                nj = j + dj
                if 0 <= ni < rows and 0 <= nj < cols:
                    if grid[ni][nj] == '@':
                        neighbors_at += 1

            if neighbors_at < 4:
                accessible_positions.append((i, j))

    # Construire une copie pour marquer les x
    marked_grid = [row[:] for row in grid]
    for i, j in accessible_positions:
        marked_grid[i][j] = 'x'

    result_grid = ["".join(row) for row in marked_grid]
    return len(accessible_positions), result_grid


def read_input_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def main():
    grid = read_input_file("inputs.txt")

    count, marked = find_accessible_rolls(grid)

    print("Accessible rolls:", count)


if __name__ == "__main__":
    main()
