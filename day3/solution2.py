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
    bank : chaîne de chiffres, ex. "987654321111111..."
    retourne le plus grand nombre possible à 12 chiffres
    formé en gardant l'ordre des chiffres.
    """
    k = 12
    n = len(bank)
    if n < k:
        raise ValueError("La banque doit contenir au moins 12 chiffres.")

    drops = n - k  # nombre de chiffres qu'on a le droit de "supprimer"
    stack = []

    for ch in bank:
        # Tant qu'on peut encore supprimer des chiffres
        # et que le dernier de la pile est plus petit que le chiffre actuel,
        # on le retire pour faire de la place à un plus grand.
        while drops > 0 and stack and stack[-1] < ch:
            stack.pop()
            drops -= 1
        stack.append(ch)

    # On garde les 12 premiers chiffres de la pile (au cas où il en reste trop)
    result_digits = stack[:k]
    return int("".join(result_digits))


def main():
    numbers = parse_numbers_from_file("inputs.txt")

    print(start_analysing(numbers))


if __name__ == "__main__":
    main()
