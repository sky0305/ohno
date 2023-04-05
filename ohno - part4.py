import random 
# import time
import numpy as np
import math
from copy import deepcopy
import os

def create_random_matrix(square):
    c = [["X"] * square for i in range(square)]
    num1 = 0
    num0 = 0
    for i in range(square):
        for j in range(square):
            c[i][j] = random.choices(["X", "O"], weights = [37, 63], k = 1)[0]
            if c[i][j] == "O":
                num1 += 1
            else:
                num0 += 1
    # print(num1, num0)
    # showout(c)
    return c

# def check_out_side(pre_answer_matrix, init_matrix, loop_times, y, x):
#     if pre_answer_matrix[y][x] > len(init_matrix):
#         loop_times += 1
#         init_matrix = create_random_matrix(len(init_matrix))
#         return init_matrix, loop_times, True
#     return init_matrix, loop_times, False


def generate_answer_matrix(init_matrix, loop_times = 1):
    pre_answer_matrix = [[0] * len(init_matrix) for i in range(len(init_matrix))]

    # value = 0
    for y in range(len(init_matrix)):
        for x in range(len(init_matrix)):
            if init_matrix[y][x] == "X":
                pre_answer_matrix[y][x] = 0
                continue

            countx = 1
            if x == 0 or init_matrix[y][x - 1] == "X":
                value = 0
                while x + countx != len(init_matrix):
                    if init_matrix[y][x + countx] == "O":
                        value += 1
                    else:
                        break
                    countx += 1
            pre_answer_matrix[y][x] += value
            if pre_answer_matrix[y][x] > len(init_matrix):
                loop_times += 1
                init_matrix = create_random_matrix(len(init_matrix))
                return generate_answer_matrix(init_matrix, loop_times)
        if pre_answer_matrix[y][x] > len(init_matrix):
            loop_times += 1
            init_matrix = create_random_matrix(len(init_matrix))
            return generate_answer_matrix(init_matrix, loop_times)
        #     if pre_answer_matrix[y][x] > len(init_matrix):
        #         break
        # if pre_answer_matrix[y][x] > len(init_matrix):
        #     break

    # value = 0
    for x in range(len(init_matrix)):
        for y in range(len(init_matrix)):
            if init_matrix[y][x] == "X":
                pre_answer_matrix[y][x] = 0
                continue

            county = 1
            if y == 0 or init_matrix[y - 1][x] == "X":
                value = 0
                while y + county != len(init_matrix):
                    if init_matrix[y + county][x] == "O":
                        value += 1
                    else:
                        break
                    county += 1
            pre_answer_matrix[y][x] += value

            if pre_answer_matrix[y][x] > len(init_matrix):
                loop_times += 1
                init_matrix = create_random_matrix(len(init_matrix))
                return generate_answer_matrix(init_matrix, loop_times)
        if pre_answer_matrix[y][x] > len(init_matrix):
            loop_times += 1
            init_matrix = create_random_matrix(len(init_matrix))
            return generate_answer_matrix(init_matrix, loop_times)

        #     if pre_answer_matrix[y][x] > len(init_matrix):
        #         loop_times += 1
        #         init_matrix = create_random_matrix(len(init_matrix))
        #         pre_answer_matrix, loop_times = generate_answer_matrix(init_matrix, loop_times)
        #         break
        # if pre_answer_matrix[y][x] > len(init_matrix):
        #     loop_times += 1
        #     init_matrix = create_random_matrix(len(init_matrix))
        #     pre_answer_matrix, loop_times = generate_answer_matrix(init_matrix, loop_times)
        #     break

        #     if pre_answer_matrix[y][x] > len(init_matrix):
        #         break
        # if pre_answer_matrix[y][x] > len(init_matrix):
        #     break
    
    # showout(pre_answer_matrix)  #I change this line to after 103 line, and pre_answer will == answer, why?
    # because the copy & = issue

    answer_matrix = deepcopy(pre_answer_matrix)
    for x in range(len(init_matrix)):
        for y in range(len(init_matrix)):
            if pre_answer_matrix[y][x] == 0:
                answer_matrix[y][x] = "X"
    # showout(answer_matrix)
    # print(loop_times)
    return answer_matrix, loop_times

def generate_question_matrix(answer_matrix, level):
    if level == "easy":
        dig_probability = 40
    elif level == "medium":
        dig_probability = 50
    # elif level == "hard":
    else:
        dig_probability = 60
    # else:
    #     print("Please re-execute this program.")

    question_matrix = deepcopy(answer_matrix)
    for y in range(len(answer_matrix)):
        for x in range(len(answer_matrix)):
            # factor = abs(answer_matrix[y][x] - np.round((1 + len(answer_matrix) - 1) / 2))
            if answer_matrix[y][x] == 1:
                question_matrix[y][x] = random.choices([" ", answer_matrix[y][x]], weights = [20, 80], k = 1)[0]
            else:
                question_matrix[y][x] = random.choices([" ", answer_matrix[y][x]], weights = [dig_probability, 100 - dig_probability], k = 1)[0]

    # showout(question_matrix)
    return question_matrix

def showout(any_matrix):
    matrix_side = len(any_matrix)
    xy_label = [str(i) for i in range(1, matrix_side + 1)]
    print("  |", "  ".join(xy_label))
    print("-" * (3 * (len(xy_label) + 1) + 1))
    print("\n  |\n".join([xy_label[i] + " | " + "  ".join(map(str, any_matrix[i])) for i in range(matrix_side)]))
    print("  |\n")

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

def generate_locked_question_matrix(question_matrix):
    locked_matrix = deepcopy(question_matrix)
    for y in range(len(question_matrix)):
        for x in range(len(question_matrix)):
            if question_matrix[y][x] != " ":
                locked_matrix[y][x] = "L"
    # showout(locked)     
    return locked_matrix


side = int(input("one side of the matrix: "))
print()

empty_matrix = [str(i) for i in range(1, side + 1)]

random_matrix = create_random_matrix(side)

# showout(c)

answer_matrix, loop_times = generate_answer_matrix(random_matrix)

question_matrix = generate_question_matrix(answer_matrix, "easy")

locked_question_matrix = generate_locked_question_matrix(question_matrix)
# showout(locked_question_matrix)

check_matrix = generate_check_matrix(locked_question_matrix, answer_matrix)

player = deepcopy(question_matrix)

while player != check_matrix:
    showout(player)
    while True:
        print('PLease enter your answer in the format like "row column O/X", e.g., "1 1 X" or "3 4 O". ')
        # print('e.g., "1 1 X" or "3 4 O".')
        reply = [input("What is your next step: ").strip().split(" ")]
        if len(reply) != 3:
            os.system("cls")
            print("Please make sure that none of the three parts in your answer is blank. \n")
        else:
            break

    row, column, ox = int(reply[0]), int(reply[1]), reply[3]

    if row > side or column > side:
        os.system("cls")
        print("Please don't enter the row or column number bigger than one side of the matrix. \n")
        continue

    if locked_question_matrix[row - 1][column - 1] == "L":
        os.system("cls")
        print("Please choose a space that isn't in the initial question. \n")
        continue

    if ox not in list("OoXx"):
        os.system("cls")
        print('Please choose "O" or "X" for your answer. \n')
        continue
    else:
        os.system("cls")
        player[row - 1][column - 1] = ox.upper()

        if answer_matrix[row - 1][column - 1] == 1 and player[row - 1][column - 1] == "X":
            print('Sorry, the space of your last step is 1. Please change it to "O". \n')

print("Congratulations! You finished the question! \n")
showout(answer_matrix)
# input('Press "Enter" to exit the program.')
# print('Press any key to exit the program.')
os.system("pause")
