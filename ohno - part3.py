import random 
# import time
import numpy as np
import math

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
    return c

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
    
    answer_matrix = pre_answer_matrix
    for x in range(len(init_matrix)):
        for y in range(len(init_matrix)):
            if pre_answer_matrix[y][x] == 0:
                answer_matrix[y][x] = "X"
    # showout(answer_matrix)
    # print(loop_times)
    return pre_answer_matrix, loop_times

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

    question_matrix = answer_matrix
    for y in range(len(answer_matrix)):
        for x in range(len(answer_matrix)):
            # factor = abs(answer_matrix[y][x] - np.round((1 + len(answer_matrix) - 1) / 2))
            if answer_matrix[y][x] == 1:
                question_matrix[y][x] = random.choices([" ", answer_matrix[y][x]], weights = [20, 80], k = 1)[0]
            else:
                question_matrix[y][x] = random.choices([" ", answer_matrix[y][x]], weights = [dig_probability, 100 - dig_probability], k = 1)[0]

    showout(question_matrix)
    return question_matrix

def showout(any_matrix):
    matrix_side = len(any_matrix)
    xy_label = [str(i) for i in range(1, matrix_side + 1)]
    print("  |", "  ".join(xy_label))
    print("-" * (3 * (len(xy_label) + 1) + 1))
    print("\n  |\n".join([xy_label[i] + " | " + "  ".join(map(str, any_matrix[i])) for i in range(matrix_side)]))
    print("  |\n")

    # 第二種顯示方式
    # print(" " * 2, "  ".join(map(str, b)), "\n")
    # # print("-" * (3 * (len(b) + 1)))
    # print("\n\n".join([b[i] + "  " + "  ".join(map(str, c[i])) for i in range(a)]))
    

a = int(input("one side of the array: "))

b = [str(i) for i in range(1, a + 1)]

c = create_random_matrix(a)

# showout(c)

d, e = generate_answer_matrix(c)

f = generate_question_matrix(d, "easy")

locked = f
for y in range(len(f)):
    for x in range(len(f)):
        if f[y][x] != " ":
            locked[y][x] = "L"

# showout(locked)     

player = f

while player != d:
    row, column, ox = input('enter the move of this round, format like "1 1 X" or "3 4 O"').split(" ")