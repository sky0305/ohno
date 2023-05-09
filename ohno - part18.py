import random, os, sys, time
from copy import deepcopy

def showout(any_matrix, way = 1):
    matrix_side = len(any_matrix)
    xy_label = [str(i) for i in range(1, matrix_side + 1)]
    if way == 1:
        print("  |", "  ".join(xy_label))
        print("-" * (3 * (len(xy_label) + 1) + 1))
        # print("\n  |\n".join([xy_label[i] + " | " + "  ".join(map(str, any_matrix[i])) for i in range(matrix_side)]))
        for i in range(matrix_side):
            a_row = list(map(str, any_matrix[i]))
            for j in range(len(a_row)):
                if len(a_row[j]) == 1:
                    a_row[j] = a_row[j] + "  "
                elif len(a_row[j]) == 2:
                    a_row[j] = a_row[j] + " "
            b = "".join(a_row)
            print(xy_label[i] + " | " + b + "\n  |")
        print()

        # [xy_label[i] + " | " + "  ".join(map(str, any_matrix[i])) for i in range(matrix_side) for j in range(matrix_side) if len(any_matrix[i][j]) == 1 else any_matrix[i][j] = any_matrix[i][j] + " "]
        
    elif way == 2:
        print("  |", "  ".join(xy_label), "|")
        print("-" * (3 * (len(xy_label) + 1) + 4))
        # print(("\n  |" + "   " * matrix_side + "|\n").join([xy_label[i] + " | " + "  ".join(map(str, any_matrix[i])) + " | " + xy_label[i] for i in range(matrix_side)]))
        
        for i in range(matrix_side):
            a_row = list(map(str, any_matrix[i]))
            for j in range(len(a_row)):
                if len(a_row[j]) == 1:
                    a_row[j] = " " + a_row[j] + " "
                elif len(a_row[j]) == 2:
                    a_row[j] = " " + a_row[j] 
            b = "".join(a_row)
            print(xy_label[i] + " |" + b + "| " + xy_label[i])
            if i != matrix_side - 1:
                print("  |" + "   " * matrix_side + "|")


        print("-" * (3 * (len(xy_label) + 1) + 4))
        print("  |", "  ".join(xy_label), "|\n")

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

def transpose_matrix(init_matrix):
    transposed_matrix = [[0] * len(init_matrix) for i in range(len(init_matrix))]
    for y in range(len(init_matrix)):
        for x in range(len(init_matrix)):
            transposed_matrix[x][y] = init_matrix[y][x]

    return transposed_matrix

def count_line_siblings(init_matrix, counter_matrix):
    for y in range(len(init_matrix)):
        for x in range(len(init_matrix[0])):
            if str(init_matrix[y][x])[0] in ("X", " "):
                counter_matrix[y][x] = 0
                continue

            offset = 1
            if x == 0 or str(init_matrix[y][x - 1])[0] in ("X", " "):
                value = 0
                while x + offset != len(init_matrix):
                    if str(init_matrix[y][x + offset])[0] in "O123456789":
                    # if str(init_matrix[y][x + offset])[0] in ("O", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                        value += 1
                    else:
                        break
                    offset += 1
            counter_matrix[y][x] += value

    init_matrix = transpose_matrix(init_matrix)
    counter_matrix = transpose_matrix(counter_matrix)

    # showout(init_matrix, howtoshow)
    # showout(counter_matrix, howtoshow)
    return init_matrix, counter_matrix

def check_full_siblings(init_matrix, return_matrix):
    for y in range(len(init_matrix)):
        for x in range(len(init_matrix[0])):
            if str(init_matrix[y][x])[0] == "X":
                return_matrix[y][x] = 0
                continue

            offset = 0
            if x == 0 or str(init_matrix[y][x - 1])[0] == "X":
                full = 1
                while x + offset != len(init_matrix):
                    if str(init_matrix[y][x + offset])[0] == " ":
                        full = 0
                        break
                    elif str(init_matrix[y][x + offset])[0] in "O123456789":
                    # elif str(init_matrix[y][x + offset])[0] in ("O", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                        pass
                    else:
                        break
                    offset += 1
            if full == 1:        
                return_matrix[y][x] += 1

    init_matrix = transpose_matrix(init_matrix)
    return_matrix = transpose_matrix(return_matrix)

    # showout(init_matrix, howtoshow)
    # showout(return_matrix, howtoshow)
    return init_matrix, return_matrix

def generate_answer_matrix(init_matrix, loop_times = 1):
    pre_answer_matrix = [[0] * len(init_matrix[0]) for i in range(len(init_matrix))]
    # X
    init_matrix, pre_answer_matrix = count_line_siblings(init_matrix, pre_answer_matrix)
    # Y
    init_matrix, pre_answer_matrix = count_line_siblings(init_matrix, pre_answer_matrix)

    for y in range(len(pre_answer_matrix)):
        for x in range(len(pre_answer_matrix[0])):
            if pre_answer_matrix[y][x] > len(pre_answer_matrix):
                loop_times += 1
                init_matrix = create_random_matrix(len(pre_answer_matrix))
                return generate_answer_matrix(init_matrix, loop_times)

    answer_matrix = deepcopy(pre_answer_matrix)
    for y in range(len(init_matrix)):
        for x in range(len(init_matrix[0])):
            if pre_answer_matrix[y][x] == 0:
                answer_matrix[y][x] = "X"
    # showout(answer_matrix, howtoshow)
    # print(loop_times, howtoshow)
    return answer_matrix, loop_times

def generate_question_matrix(answer_matrix):
    question_matrix = deepcopy(answer_matrix)
    for y in range(len(answer_matrix)):
        for x in range(len(answer_matrix)):
            if answer_matrix[y][x] == 1:
                question_matrix[y][x] = random.choices([" ", answer_matrix[y][x]], weights = [20, 80], k = 1)[0]
            else:
                question_matrix[y][x] = random.choices([" ", answer_matrix[y][x]], weights = [40, 60], k = 1)[0]
    # showout(question_matrix, howtoshow)
    return question_matrix

def generate_locked_question_matrix(question_matrix):
    locked_matrix = deepcopy(question_matrix)
    for y in range(len(question_matrix)):
        for x in range(len(question_matrix)):
            if question_matrix[y][x] != " ":
                locked_matrix[y][x] = "L"
    # showout(locked, howtoshow)     
    return locked_matrix

def generate_check_matrix(locked_matrix, answer_matrix):
    check_matrix = deepcopy(answer_matrix)
    for y in range(len(answer_matrix)):
        for x in range(len(answer_matrix)):
            if locked_matrix[y][x] == "L":
                continue
            if check_matrix[y][x] != "X":
                check_matrix[y][x] = "O"
    # showout(check_matrix, howtoshow)
    return check_matrix

def print_one_by_one(text):
    os.system("cls")
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        if i == "\n":
            time.sleep(0.10)
        else:
            time.sleep(0.03)
    # sys.stdout.flush()
    print()

rule = '''題目中所呈現的數字代表
以 該位置 十字狀放射
在遇到X或是邊界前
數字與O的總合(不含本身)。
請以 "列 行 O/X" 的格式回答每一步的更動，
例如："1 1 X" 或 "3 4 O"。
有時題目所挖的空格可有兩解，但僅有唯一正解，
請嘗試不同組合。

祝您玩得愉快～\n

The numbers in cell, presented in the question,
represent the sum of any number and O (not including itself) 
in the range from that cell radiated in the shape of a cross, 
before encountering X or the boundary.
Please answer each step of the change in "column row O/X" format,
for example: "1 1 X" or "3 4 O".
Sometimes there are two solutions to the space in the question,
but there is only one correct solution, 
please try different combinations.

Wish you have a good time~\n'''
# 理論上每個空格需僅有唯一解

print_one_by_one(rule)
os.system("pause")

os.system("cls")
example = [["O", "X"], ["X", "O"]]
while True:
    print("[1] half matrix surrounded by lines: \n")
    showout(example, 1)
    print("[2] full matrix surrounded by lines: \n")
    showout(example, 2)
    print()

    howtoshow = input("Please choose one way to show question matrix: ").strip()
    os.system("cls")
    if howtoshow.isdigit() and int(howtoshow) in (1, 2):
        howtoshow = int(howtoshow)
        break
    print("Please choose a number from [1] or [2]. ")
    
while True:
    side = input("Please choose a level from 1-5: ").strip()
    os.system("cls")
    if side.isdigit() and 1 <= int(side) <= 5:
        side = int(side) + 4
        break

    print("Please enter a number from 1-5. ")

while True:
    play_mode = input(f'''
 - [E]asy   mode (show "!" when your response is different from the answer)
 - [M]edium mode (show "?" when the number in certain cell exceeds that given by question, 
              and show "!" when the number in certain cell, surrounded by "X" and boundary, 
                            is less than that given by question)
 - [H]ard   mode (no hint)
 Which mode do you want to play in? [E]/[M]/[H]: ''').strip().lower()
    
    os.system("cls")
    if play_mode.isalpha():
        if play_mode in ("e", "easy", "easy mode"):
            play_mode = 1
            break
        elif play_mode in ("m", "medium", "medium mode"):
            play_mode = 2
            break
        elif play_mode in ("h", "hard", "hard mode"):
        # elif play_mode in ("h", "hard", "hard mode", "n", "normal", "normal mode"):
            play_mode = 3
            break

    print("Please enter [E] or [M] or [H] for choosing game difficulty. \n")

def easy_mode(player_matrix, check_matrix, row, column):
    if player_matrix[row][column] != check_matrix[row][column]:
        player_matrix[row][column] = player_matrix[row][column] + "!"
        # print("!\n")
    return

def medium_hard_mode(player_matrix, hardmode = 0):
    # check the number over or not
    over_check_matrix = [[0] * len(player_matrix[0]) for i in range(len(player_matrix))]
    # X
    player_matrix, over_check_matrix = count_line_siblings(player_matrix, over_check_matrix)
    # Y
    player_matrix, over_check_matrix = count_line_siblings(player_matrix, over_check_matrix)
    
    # check the number, surrounded by boundary and X, enough or not
    check_full_matrix = [[0] * len(player_matrix[0]) for i in range(len(player_matrix))]
    # X
    player_matrix, check_full_matrix = check_full_siblings(player_matrix, check_full_matrix)
    # Y
    player_matrix, check_full_matrix = check_full_siblings(player_matrix, check_full_matrix)

    # showout(check_full_matrix, howtoshow)
    # showout(over_check_matrix, howtoshow)
    
    over_check = 0
    not_enough_check = 0
    alone_O = 0
 

    for y in range(len(player_matrix)):
        for x in range(len(player_matrix[0])):
            if str(player_matrix[y][x])[0].isdigit():
                if over_check_matrix[y][x] > int(str(player_matrix[y][x])[0]):
                    over_check = 1
                    if "?" not in str(player_matrix[y][x]):
                        player_matrix[y][x] = str(player_matrix[y][x]) + "?"
                else:
                    if "?" in str(player_matrix[y][x]):
                        player_matrix[y][x] = str(player_matrix[y][x]).replace("?", "")

                if check_full_matrix[y][x] == 2 and (over_check_matrix[y][x] < int(str(player_matrix[y][x])[0])):
                    not_enough_check = 1
                    if "!" not in str(player_matrix[y][x]):
                        player_matrix[y][x] = str(player_matrix[y][x]) + "!"
                else:
                    if "!" in str(player_matrix[y][x]):
                        player_matrix[y][x] = str(player_matrix[y][x]).replace("!", "")

    
            elif player_matrix[y][x] in ("O", "O*"):
                if (y != 0 and player_matrix[y - 1][x] != "X") \
                or (y != len(player_matrix) - 1 and player_matrix[y + 1][x] != "X") \
                or (x != 0 and player_matrix[y][x - 1] != "X") \
                or (x != len(player_matrix[0]) - 1 and player_matrix[y][x + 1] != "X"):
                    # if player_matrix[y][x] == "O*":
                    player_matrix[y][x] = "O"
                    continue
                else:      
                    alone_O = 1
                    if "*" not in player_matrix[y][x]:
                        player_matrix[y][x] = player_matrix[y][x] + "*"

    full_filled = 0
    if not_enough_check == over_check == 0 and alone_O == 0:
        full_filled = 1
        for y in range(len(player_matrix)):
            for x in range(len(player_matrix[0])):
                if player_matrix[y][x] == " ":
                    full_filled = 0
                    break
            if full_filled == 0:
                break

    if full_filled == 1:
        new_answer_matrix, new_loop_times = generate_answer_matrix(player_matrix)
        return player_matrix, new_answer_matrix
    
    if hardmode == 0:
        if alone_O == 1:
            print("There is/are certain O(s) feel alone QQ, please change it/them to X(s).\n")

        # if over_check == 1 and not_enough_check == 1:
        #     print("?    !\n")
        # elif over_check == 1:
        #     print("?\n")
        # elif not_enough_check == 1:
        #     print("!\n")
    elif hardmode == 1:
        pass

    return player_matrix, None

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
        if play_mode == 1:
            print('When your response is different from the answer, it will show "!".\n')
        if play_mode == 2:
            print("when [over] will show: ?      when [lack] will show: !\n")

        showout(player_matrix, howtoshow)
        print('Please enter your reply in the format like "row column O/X", e.g., "1 1 X" or "3 4 O". ')
        print('Or enter "U" or "undo" to undo your last step, "Restart" to restart this game. ')
        reply = input("What is your next step: ").strip().split()
        os.system("cls")
        if len(reply) == 1 and reply[0].lower() in ("u", "undo") :
            if len(for_undo_restart) != 1:
                player_matrix = for_undo_restart.pop()
            undo_restart_code = 1
            new_answer_matrix = medium_hard_mode(player_matrix)
            break
        elif len(reply) == 1 and reply[0] == "Restart":
            for_undo_restart.append(deepcopy(player_matrix))
            player_matrix = deepcopy(for_undo_restart[0])
            undo_restart_code = 2
            break
        elif len(reply) != 3:
            print("Please make sure there are exactly three parts in your reply and none of them is blank. \n")
        elif not (reply[0].isdigit() and reply[1].isdigit()):
            print("Please make sure that both the first part and the second part in your reply are numbers. \n")        
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

        if easy_mode == 1 and answer_matrix[row][column] == 1 and player_matrix[row][column] == "X":
            print('Sorry, the location of your last step is 1. Please change it to "O". \n')

        if play_mode == 1:
            easy_mode(player_matrix, check_matrix, row, column)
        elif play_mode in (2, 3):
            if play_mode == 2:
                player_matrix, new_answer_matrix = medium_hard_mode(player_matrix)
            elif play_mode == 3:
                player_matrix, new_answer_matrix = medium_hard_mode(player_matrix, 1)

            if new_answer_matrix is not None:
                answer_matrix = new_answer_matrix
                break

end = time.time()
delta = end - start
print(f"Congratulations! You spent {int(delta / 3600)}h {int(delta % 3600 / 60)}m {int(delta % 60)}s solving this game.\n")
showout(answer_matrix, howtoshow)
os.system("pause")
os.system("cls")