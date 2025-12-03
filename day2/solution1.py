import argparse

def parse_ranges_from_file(filepath):
    start_numbers = []
    end_numbers = []

    with open(filepath, "r", encoding="utf-8") as f:
        line = f.read().strip()

    # Enlever une éventuelle virgule finale
    if line.endswith(","):
        line = line[:-1]

    # Split par les virgules
    ranges = line.split(",")

    for r in ranges:
        # Chaque segment du style "start-end"
        start, end = r.split("-")
        start_numbers.append(int(start))
        end_numbers.append(int(end))

    return start_numbers, end_numbers

def start_analysing(start_numbers, end_numbers):
    length = len(start_numbers)

    count = 0

    for i in range(length):
        count += analysing(start_numbers[i],end_numbers[i])

    return count

def analysing(start, end):
    count = 0

    for i in range(start, end+1):
        if get_invalid_number_boolean(i):
            count+=i

    return count

def get_invalid_number_boolean(number):
    s = str(number)
    # doit être de longueur paire
    if len(s) % 2 != 0:
        return False
    
    mid = len(s) // 2
    return s[:mid] == s[mid:]

def main():
    start_numbers, end_numbers = parse_ranges_from_file("inputs.txt")

    print(start_analysing(start_numbers, end_numbers))


if __name__ == "__main__":
    main()
