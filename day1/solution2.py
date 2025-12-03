import argparse

def read_file_split_letters_numbers(filepath):
    letters = []
    numbers = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            letter = line[0]
            number = int(line[1:])
            letters.append(letter)
            numbers.append(number)

    return letters, numbers

def get_new_position(lastPosition, letter, number):
    if letter == 'L':
        if lastPosition == 0:
            return lastPosition-number+100
        return lastPosition-number
    return lastPosition+number

def get_solution(letters, numbers):
    position=50

    solution = 0

    for i in range(len(letters)):
        position = get_new_position(position, letters[i], numbers[i]%100)

        if numbers[i]//100 > 0:
            solution+=numbers[i]//100

        print(letters[i], numbers[i])
        print("position",position)

        if position == 0:
            solution+=1
        if position > 99:
            solution+=1
            position=position%100
        if position <0:
            solution+=1
            position=(position+100)%100
        print("real position",position)

        print("solution", solution)
    
    return solution


def main():
    letters, numbers = read_file_split_letters_numbers("inputs.txt")

    print(get_solution(letters, numbers))


if __name__ == "__main__":
    main()
