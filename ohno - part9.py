import random, os, sys, time
from copy import deepcopy

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
            OX_random_matrix[i][j] = random.choices(["X", "O"], weights = [5, 12], k = 1)[0]
            # OX_random_matrix[i][j] = random.choices(["X", "O"], weights = [37, 63], k = 1)[0]
            if OX_random_matrix[i][j] == "O":
                quantity_O += 1

    quantity_X = side ** 2 - quantity_O
    return OX_random_matrix

def count_line_siblings(init_matrix, pre_answer_matrix):
    for y in range(len(init_matrix)):
        for x in range(len(init_matrix)):
            if init_matrix[y][x] == "X":
                pre_answer_matrix[y][x] = 0
                continue

            offset = 1
            if x == 0 or init_matrix[y][x - 1] == "X":
                value = 0
                while x + offset != len(init_matrix):
                    if init_matrix[y][x + offset] == "O":
                        value += 1
                    else:
                        break
                    offset += 1
            pre_answer_matrix[y][x] += value

    init_matrix = transpose_matrix(init_matrix)
    pre_answer_matrix = transpose_matrix(pre_answer_matrix)

    # showout(init_matrix)
    # showout(pre_answer_matrix)
    return init_matrix, pre_answer_matrix
    
def transpose_matrix(init_matrix):
    transposed_matrix = [[0] * len(init_matrix) for i in range(len(init_matrix))]
    for y in range(len(init_matrix)):
        for x in range(len(init_matrix)):
            transposed_matrix[x][y] = init_matrix[y][x]

    return transposed_matrix

def generate_answer_matrix(init_matrix, loop_times = 1):
    pre_answer_matrix = [[0] * len(init_matrix) for i in range(len(init_matrix))]
    # X
    init_matrix, pre_answer_matrix = count_line_siblings(init_matrix, pre_answer_matrix)
    # Y
    init_matrix, pre_answer_matrix = count_line_siblings(init_matrix, pre_answer_matrix)

    for y in range(len(pre_answer_matrix)):
        for x in range(len(pre_answer_matrix)):
            if pre_answer_matrix[y][x] > len(pre_answer_matrix):
                loop_times += 1
                init_matrix = create_random_matrix(len(pre_answer_matrix))
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
    os.system("cls")
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        if i == "\n":
            time.sleep(0.3)
        else:
            time.sleep(0.1)
    # sys.stdout.flush()
    print()

rule = '''題目中所呈現的數字代表
以 那個位子 十字狀放射
遇到X或是邊界前的
數字與O的總合(不含本身)
請以 "列 行 O/X" 的格式回答每一步的更動
例如："1 1 X" 或 "3 4 O"
基本上每題僅有唯一解
祝您玩得愉快\n'''

print_one_by_one(rule)

os.system("pause")
os.system("cls")
while True:
    side = input("Please choose a level from 1-5: ").strip()
    os.system("cls")
    if side.isdigit():
        side = int(side) + 4
        if 5 <= side <= 9:
            break

    print("Please enter a number from 1-5. ")

while True:
    easy_mode = input('Would you like to play in easy mode(show "!" when your last step was wrong)? \n[Y]es / [N]o : ').strip().lower()
    os.system("cls")
    if easy_mode.isalpha():
        if easy_mode in ("y", "yes"):
            easy_mode = 1
            break
        elif easy_mode in ("n", "no"):
            easy_mode = 0
            break

    print("Please enter [Y] or [N] for choosing game difficulty. ")

random_matrix = create_random_matrix(side)

answer_matrix, loop_times = generate_answer_matrix(random_matrix)

question_matrix = generate_question_matrix(answer_matrix)

locked_matrix = generate_locked_question_matrix(question_matrix)

check_matrix = generate_check_matrix(locked_matrix, answer_matrix)

player_matrix = deepcopy(question_matrix)

for_undo_restart = [deepcopy(player_matrix)]

start = time.time()
while player_matrix != check_matrix:
    while True:
        # print(len(for_undo_restart))
        showout(player_matrix)
        print('Please enter your reply in the format like "row column O/X", e.g., "1 1 X" or "3 4 O". ')
        print('Or enter "U" or "undo" to undo your last step, "restart" to restart this game. ')
        reply = input("What is your next step: ").strip().split()
        os.system("cls")
        if len(reply) == 1 and reply[0].lower() in ("u", "undo") :
            if len(for_undo_restart) != 1:
                player_matrix = for_undo_restart.pop()
            undo_restart_code = 1
            break
        elif len(reply) == 1 and reply[0].lower() == "restart":
            print("i'm in restart")
            for_undo_restart.append(deepcopy(player_matrix))
            player_matrix = deepcopy(for_undo_restart[0])
            undo_restart_code = 2
            break
        elif len(reply) != 3:
            print("PLease make sure there are exactly three parts in your reply and none of them is blank. \n")
        elif not (reply[0].isdigit() and reply[1].isdigit()):
            print("PLease make sure that both the first part and the second part in your reply are numbers. \n")        
        else:
            undo_restart_code = 0
            break
    
    os.system("cls")

    if undo_restart_code != 0:
        continue

    row, column, ox = int(reply[0]) - 1, int(reply[1]) - 1, reply[2]
    if row > side - 1 or column > side - 1 or row < 0 or column < 0:
        print(f"Please enter the row or column number between 1-{side}. \n")
        continue

    if locked_matrix[row][column] == "L":
        print("Please choose a location that isn't in the initial question. \n")
        continue

    if ox not in list("OoXx"):
        print('Please choose "O" or "X" for the third part of reply. \n')
        continue
    else:
        for_undo_restart.append(deepcopy(player_matrix))

        player_matrix[row][column] = ox.upper()

        if answer_matrix[row][column] == 1 and player_matrix[row][column] == "X":
            print('Sorry, the location of your last step is 1. Please change it to "O". \n')

        if easy_mode == 1:
            if check_matrix[row][column] != player_matrix[row][column]:
                print("!\n")

end = time.time()
delta = end - start
print(f"Congratulations! You spent {int(delta / 3600)}h {int(delta % 3600 / 60)}m {int(delta % 60)}s solving this game.\n")
showout(answer_matrix)
os.system("pause")
os.system("cls")