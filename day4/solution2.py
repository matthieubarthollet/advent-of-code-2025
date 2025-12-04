def read_input_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def simulate_removals(grid_lines):
    grid = [list(row) for row in grid_lines]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1),
    ]

    total_removed = 0

    while True:
        to_remove = []

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
                    to_remove.append((i, j))

        if not to_remove:
            break  # plus rien à enlever

        # enlever tous les rouleaux trouvés à ce tour
        for i, j in to_remove:
            grid[i][j] = '.'  # rouleau retiré

        total_removed += len(to_remove)

    final_grid = ["".join(row) for row in grid]
    return total_removed, final_grid


def main():
    grid = read_input_file("inputs.txt")
    total_removed, final_grid = simulate_removals(grid)

    print("Total rolls removed:", total_removed)


if __name__ == "__main__":
    main()
