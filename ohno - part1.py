import random 
import time

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

# def generate_answer_matrix(init_matrix, loop_times = 1):
#     pre_answer_matrix = [[0] * len(init_matrix) for i in range(len(init_matrix))]

#     # value = 0
#     for y in range(len(init_matrix)):
#         for x in range(len(init_matrix)):
#             if init_matrix[y][x] == "X":
#                 pre_answer_matrix[y][x] = 0
#                 continue

#             countx = 1
#             if x == 0 or init_matrix[y][x - 1] == "X":
#                 value = 0
#                 while x + countx != len(init_matrix):
#                     if init_matrix[y][x + countx] == "O":
#                         value += 1
#                     else:
#                         break
#                     countx += 1
#             pre_answer_matrix[y][x] += value
#             if pre_answer_matrix[y][x] > len(init_matrix):
#                 loop_times += 1
#                 init_matrix = create_random_matrix(len(init_matrix))
#                 return generate_answer_matrix(init_matrix, loop_times)
#         if pre_answer_matrix[y][x] > len(init_matrix):
#             loop_times += 1
#             init_matrix = create_random_matrix(len(init_matrix))
#             return generate_answer_matrix(init_matrix, loop_times)
#         #     if pre_answer_matrix[y][x] > len(init_matrix):
#         #         break
#         # if pre_answer_matrix[y][x] > len(init_matrix):
#         #     break

#     # value = 0
#     for x in range(len(init_matrix)):
#         for y in range(len(init_matrix)):
#             if init_matrix[y][x] == "X":
#                 pre_answer_matrix[y][x] = 0
#                 continue

#             county = 1
#             if y == 0 or init_matrix[y - 1][x] == "X":
#                 value = 0
#                 while y + county != len(init_matrix):
#                     if init_matrix[y + county][x] == "O":
#                         value += 1
#                     else:
#                         break
#                     county += 1
#             pre_answer_matrix[y][x] += value

#             if pre_answer_matrix[y][x] > len(init_matrix):
#                 loop_times += 1
#                 init_matrix = create_random_matrix(len(init_matrix))
#                 return generate_answer_matrix(init_matrix, loop_times)
#         if pre_answer_matrix[y][x] > len(init_matrix):
#             loop_times += 1
#             init_matrix = create_random_matrix(len(init_matrix))
#             return generate_answer_matrix(init_matrix, loop_times)

#         #     if pre_answer_matrix[y][x] > len(init_matrix):
#         #         loop_times += 1
#         #         init_matrix = create_random_matrix(len(init_matrix))
#         #         pre_answer_matrix, loop_times = generate_answer_matrix(init_matrix, loop_times)
#         #         break
#         # if pre_answer_matrix[y][x] > len(init_matrix):
#         #     loop_times += 1
#         #     init_matrix = create_random_matrix(len(init_matrix))
#         #     pre_answer_matrix, loop_times = generate_answer_matrix(init_matrix, loop_times)
#         #     break

#         #     if pre_answer_matrix[y][x] > len(init_matrix):
#         #         break
#         # if pre_answer_matrix[y][x] > len(init_matrix):
#         #     break
    
#     answer_matrix = pre_answer_matrix
#     for x in range(len(init_matrix)):
#         for y in range(len(init_matrix)):
#             if pre_answer_matrix[y][x] == 0:
#                 answer_matrix[y][x] = "X"
#     showout(answer_matrix)
#     print(loop_times)
#     return pre_answer_matrix, loop_times

# def generate_question_matrix(answer_matrix, level):
#     if level == "easy":
#         probability = 25
#     elif level == "medium":
#         probability = 40
#     elif level == "hard":
#         probability = 60
#     else:
#         print("Please re-execute this program.")

#     question_matrix = answer_matrix
#     for y in range(len(answer_matrix)):
#         for x in range(len(answer_matrix)):
#             question_matrix[y][x] = random.choices([" ", answer_matrix[y][x]], weights = [probability, 100 - probability], k = 1)[0]

#     showout(question_matrix)
#     return question_matrix

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

showout(c)

# d, e = generate_answer_matrix(c)

# f = generate_question_matrix(d, "easy")
d = [[0] * a for i in range(a)]

state = 0
loop_times = 0
while state != 1:
    # value = 0
    for y in range(a):
        for x in range(a):
            if c[y][x] == "X":
                d[y][x] = 0
                continue

            countx = 1
            if x == 0 or c[y][x - 1] == "X":
                value = 0
                while x + countx != a:
                    if c[y][x + countx] == "O":
                        value += 1
                    else:
                        break
                    countx += 1
            d[y][x] += value
            if d[y][x] > a:
                break
        if d[y][x] > a:
            break
    loop_times += 1
    if y == a - 1 and d[y][x] <= a:
        state = 1
    

showout(d)
print(loop_times)

state = 0
loop_times = 0
while state != 1:
    # value = 0
    for x in range(a):
        for y in range(a):
            if c[y][x] == "X":
                d[y][x] = 0
                continue

            county = 1
            if y == 0 or c[y - 1][x] == "X":
                value = 0
                while y + county != a:
                    if c[y + county][x] == "O":
                        value += 1
                    else:
                        break
                    county += 1
            d[y][x] += value
            if d[y][x] > a:
                break
        if d[y][x] > a:
            break
    loop_times += 1
    if x == a - 1 and d[y][x] <= a:
        state = 1

showout(d)
print(loop_times)

# 超過a就重新生成

# for y in range(a):
#     for x in range(a):
#         count = 0
#         value = 0
#         if c[y][x] == 0:
#             continue
#         else:
#             for times in range(4):
#                 if x - count == 0:
#                     continue
#                 else:
#                     count += 1
#                     if c[y][x - count] == 0:
#                         continue
#                     else:
#                         value += 1

# for y in range(a):
#     for x in range(a):
#         county = 1
#         value = 0
#         while y + county != a:
#             countx = 1
#             while x + countx != a:
#                 if c[y + county][x + countx] != 0:
#                     value += 1
#                     countx += 1
#                 else:
#                     break
#             county += 1

# a = 5
# pp = [1,1,1,1,0,0,1,1,1,0,1,1,1,0]
# ans = [3,3,3,3,0,0,2,2,2,0,2,2,2,0]
# d = pp

# for x in range(a):
#     countx = - a + 1
#     if pp[x] == 0:
#         countx = 0
#         continue
#     value = 0
#     while x + countx != a:
#         if countx != 0:
#             if x + countx >= 0:
#                 if pp[x + countx] != 0:
#                     value += 1
#                 else:
#                     break
#         countx += 1
#     d[x] = value

# # 目前沒有遇到0的累積數字


# pp = [1,1,1,1,0,0,1,1,1,0,1,1,1,0]
# ans = [3,3,3,3,0,0,2,2,2,0,2,2,2,0]
# d = pp

# for x in range(len(pp)):
#     if pp[x] == 0:
#         d[x] = 0
#         continue

#     countx = 1
#     if x == 0 or pp[x - 1] == 0:
#         value = 0
#         while x + countx != len(pp):
#             if pp[x + countx] == 1:
#                 value += 1
#             else:
#                 break
#             countx += 1
#     d[x] += value
    


