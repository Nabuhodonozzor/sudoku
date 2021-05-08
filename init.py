def print_board(board: list) -> None:
    for i, line in enumerate(board):
        for j, arg in enumerate(line):
            if (j + 1) % 3 == 0 and j != len(line) - 1:
                print(f'{arg} | ', end='')
            else:
                print(f'{arg}  ', end='')
        print()
        if (i + 1) % 3 == 0 and i != len(board) - 1:
            print("-" * (len(line) * 3))
    print()


def number_validator(num: int, x: int, y: int, board: list) -> bool:
    # line checking
    for arg in board[y]:
        if arg == num:
            return False

    # column checking
    for line in board:
        if line[x] == num:
            return False

    # box checking
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3

    for line in board[y0:y0+3]:
        for arg in line[x0:x0+3]:
            if arg == num:
                return False
    return True


def find_zero(board):
    for line in board:
        for arg in line:
            if arg == 0:
                return True
    return False


def board_validator(board):
    for y, line in enumerate(board):
        for x, arg in enumerate(line):
            if arg != 0:
                board[y][x] = 0
                if not number_validator(arg, x, y, board):
                    board[y][x] = arg
                    return False
                board[y][x] = arg
    return True


def return_invalid(board):
    invalid = []
    for y, line in enumerate(board):
        for x, arg in enumerate(line):
            if arg != 0:
                board[y][x] = 0
                if not number_validator(arg, x, y, board):
                    invalid += [(x, y)]
                board[y][x] = arg
    return invalid


def sudoku_solver(board):
    if not find_zero(board):
        return True

    for y, line in enumerate(board):
        for x, arg in enumerate(line):
            if arg == 0:
                for num in range(1, 10):
                    if number_validator(num, x, y, board):
                        board[y][x] = num
                        if sudoku_solver(board):
                            return True
                    board[y][x] = 0
                return False


def board_return(board):
    base_board = board
    if sudoku_solver(board):
        return board
    else:
        return base_board



