import argparse

def parse_numbers_from_file(filepath):
    numbers = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            numbers.append(line)

    return numbers

def start_analysing(numbers):
    length = len(numbers)

    count = 0

    for i in range(length):
        count += analysing(numbers[i])

    return count

def analysing(bank):
    """
    bank : chaîne de chiffres, ex. "987654321111111"
    retourne le plus grand nombre à deux chiffres possible
    obtenu en choisissant deux positions i < j.
    """
    if len(bank) < 2:
        raise ValueError("La banque doit contenir au moins deux chiffres.")

    max_first_digit = int(bank[0])
    best = -1

    for i in range(1, len(bank)):
        d = int(bank[i])

        # nombre formé avec le meilleur premier chiffre vu jusque-là
        candidate = 10 * max_first_digit + d
        if candidate > best:
            best = candidate

        # mettre à jour le meilleur premier chiffre possible
        if d > max_first_digit:
            max_first_digit = d

    return best

def main():
    numbers = parse_numbers_from_file("inputs.txt")

    print(start_analysing(numbers))


if __name__ == "__main__":
    main()
