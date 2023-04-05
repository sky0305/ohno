import random 
from copy import deepcopy
import os
import sys
import time

def showout(any_matrix):
    matrix_side = len(any_matrix)
    xy_label = [str(i) for i in range(1, matrix_side + 1)]
    print("  |", "  ".join(xy_label))
    print("-" * (3 * (len(xy_label) + 1) + 1))
    print("\n  |\n".join([xy_label[i] + " | " + "  ".join(map(str, any_matrix[i])) for i in range(matrix_side)]))
    print("  |\n")

def create_random_matrix(side):
    OX_random_matrix = [["X"] * side for i in range(side)]
    quantity_O = 0
    for i in range(side):
        for j in range(side):
            OX_random_matrix[i][j] = random.choices(["X", "O"], weights = [37, 63], k = 1)[0]
            if OX_random_matrix[i][j] == "O":
                quantity_O += 1

    quantity_X = side ** 2 - quantity_O
    return OX_random_matrix

def generate_answer_matrix(init_matrix, loop_times = 1):
    pre_answer_matrix = [[0] * len(init_matrix) for i in range(len(init_matrix))]

    # count x axis value
    # value = 0
    for y in range(len(init_matrix)):
        for x in range(len(init_matrix)):
            if init_matrix[y][x] == "X":
                pre_answer_matrix[y][x] = 0
                continue

            offset_x = 1
            if x == 0 or init_matrix[y][x - 1] == "X":
                value = 0
                while x + offset_x != len(init_matrix):
                    if init_matrix[y][x + offset_x] == "O":
                        value += 1
                    else:
                        break
                    offset_x += 1
            pre_answer_matrix[y][x] += value

    # count y axis value
    # value = 0
    for x in range(len(init_matrix)):
        for y in range(len(init_matrix)):
            if init_matrix[y][x] == "X":
                pre_answer_matrix[y][x] = 0
                continue

            offset_y = 1
            if y == 0 or init_matrix[y - 1][x] == "X":
                value = 0
                while y + offset_y != len(init_matrix):
                    if init_matrix[y + offset_y][x] == "O":
                        value += 1
                    else:
                        break
                    offset_y += 1
            pre_answer_matrix[y][x] += value
            if pre_answer_matrix[y][x] > len(init_matrix):
                loop_times += 1
                init_matrix = create_random_matrix(len(init_matrix))
                return generate_answer_matrix(init_matrix, loop_times)

    answer_matrix = deepcopy(pre_answer_matrix)
    for x in range(len(init_matrix)):
        for y in range(len(init_matrix)):
            if pre_answer_matrix[y][x] == 0:
                answer_matrix[y][x] = "X"
    # showout(answer_matrix)
    # print(loop_times)
    return answer_matrix, loop_times

def generate_question_matrix(answer_matrix):
    question_matrix = deepcopy(answer_matrix)
    for y in range(len(answer_matrix)):
        for x in range(len(answer_matrix)):
            if answer_matrix[y][x] == 1:
                question_matrix[y][x] = random.choices([" ", answer_matrix[y][x]], weights = [20, 80], k = 1)[0]
            else:
                question_matrix[y][x] = random.choices([" ", answer_matrix[y][x]], weights = [40, 60], k = 1)[0]
    # showout(question_matrix)
    return question_matrix

def generate_locked_question_matrix(question_matrix):
    locked_matrix = deepcopy(question_matrix)
    for y in range(len(question_matrix)):
        for x in range(len(question_matrix)):
            if question_matrix[y][x] != " ":
                locked_matrix[y][x] = "L"
    # showout(locked)     
    return locked_matrix

def generate_check_matrix(locked_matrix, answer_matrix):
    check_matrix = deepcopy(answer_matrix)
    for y in range(len(answer_matrix)):
        for x in range(len(answer_matrix)):
            if locked_matrix[y][x] == "L":
                continue
            if check_matrix[y][x] != "X":
                check_matrix[y][x] = "O"
    # showout(check_matrix)
    return check_matrix

def print_one_by_one(text):
    # sys.stdout.write("\r" + " " * 60 + "\r")
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        if i == "\n":
            time.sleep(0.5)
        else:
            time.sleep(0.1)
    # sys.stdout.flush()
    print()


rule = '''每
個'''

print_one_by_one(rule)

os.system("cls")
while True:
    side = input("Please choose a level from 1-5: ").strip()
    os.system("cls")
    if side.isdigit():
        side = int(side) + 4
        if 5 <= side <= 9:
            break

    print("Please enter a number from 1-5. ")

# start = time.time()
random_matrix = create_random_matrix(side)

answer_matrix, loop_times = generate_answer_matrix(random_matrix)

question_matrix = generate_question_matrix(answer_matrix)

locked_matrix = generate_locked_question_matrix(question_matrix)

check_matrix = generate_check_matrix(locked_matrix, answer_matrix)

player_matrix = deepcopy(question_matrix)

while player_matrix != check_matrix:
    while True:
        showout(player_matrix)
        print('PLease enter your reply in the format like "row column O/X", e.g., "1 1 X" or "3 4 O". ')
        reply = input("What is your next step: ").strip().split()
        os.system("cls")
        if len(reply) != 3:
            print("PLease make sure there are exactly three parts in your reply and none of them is blank. \n")
        elif not (reply[0].isdigit() and reply[1].isdigit()):
            print("PLease make sure that both the first part and the second part in your reply are numbers. \n")        
        else:
            break

    row, column, ox = int(reply[0]) - 1, int(reply[1]) - 1, reply[2]

    os.system("cls")
    if row > side - 1 or column > side - 1 or row < 0 or column < 0:
        print(f"Please enter the row or column number between 1-{side}. \n")
        continue

    if locked_matrix[row][column] == "L":
        # os.system("cls")
        print("Please choose a location that isn't in the initial question. \n")
        continue

    if ox not in list("OoXx"):
        print('Please choose "O" or "X" for the third part of reply. \n')
        continue
    else:
        player_matrix[row][column] = ox.upper()

        if answer_matrix[row][column] == 1 and player_matrix[row][column] == "X":
            print('Sorry, the location of your last step is 1. Please change it to "O". \n')

# end = time.time()
print("Congratulations! You finished the question! \n")
showout(answer_matrix)
os.system("pause")
os.system("cls")