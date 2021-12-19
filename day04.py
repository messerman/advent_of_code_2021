#!/usr/bin/env python3

def read_board():
    # read past any newlines
    line = None
    while not line:
        line = input()
    
    board = []
    while line:
        board.append([int(num) for num in line.split(' ') if num])
        try:
            line = input()
        except:
            line = None
    
    return board

def mark_boards(boards, num):
    for board in boards:
        for row in board:
            for col in range(len(row)):
                if num == row[col]:
                    row[col] = 'X'

def has_bingo(board):
    if board.count(['X'] * 5) > 0:
        return True
    
    valid = [0, 1, 2, 3, 4]
    for row in board:
        for col in valid:
            if 'col' != -1 and 'X' != row[col]:
                valid[col] = -1

    return bool(valid.count(-1) < 5)

def sum_unmarked(board):
    total = 0
    for row in board:
        for value in row:
            if value != 'X':
                total += value
    return total

if '__main__' == __name__:
    done = False
    nums = [int(num) for num in input().split(',')]
    boards = []

    while not done:
        try:
            boards.append(read_board())
        except:
            done = True

    count = 0
    for num in nums:
        mark_boards(boards, num)
        count += 1
        if count >= 5:
            to_remove = []
            for board in boards:
                if has_bingo(board):
                    to_remove.append(board)
                    if 1 == len(boards):
                        print(board)
                        print(sum_unmarked(board), num)
                        print(sum_unmarked(board) * num)
                        exit()

            for board in to_remove:
                boards.remove(board)
                