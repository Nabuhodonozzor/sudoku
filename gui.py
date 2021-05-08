import pygame
import sys
from init import print_board, sudoku_solver, board_validator, return_invalid


# initialisation of pygame module
pygame.init()
# setting window dimensions
screen = pygame.display.set_mode((1280, 760))
clock = pygame.time.Clock()
# setting time after which program recognises that key is held for at longer time
pygame.key.set_repeat(300, 75)

# Colour definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (250, 0, 0)
YELLOW = (255, 255, 0)
ERROR_RED = (133, 27, 27)


# Input init
sudoku_font = pygame.font.Font('res/FreeSans.ttf', 40)
x_pos = 0
y_pos = 0


# Display init
pygame.display.set_caption("Sudoku solver")
icon = pygame.image.load('res/obrazek.png')
pygame.display.set_icon(icon)


# Sound init (background music)
pygame.mixer.init()
sound = pygame.mixer.Sound('res/background.wav')
channel = sound.play()
sound.set_volume(0.05)


def clear_board():
    # function used to return a clear board
    board = [[0, 0, 0,   0, 0, 0,   0, 0, 0],
             [0, 0, 0,   0, 0, 0,   0, 0, 0],
             [0, 0, 0,   0, 0, 0,   0, 0, 0],

             [0, 0, 0,   0, 0, 0,   0, 0, 0],
             [0, 0, 0,   0, 0, 0,   0, 0, 0],
             [0, 0, 0,   0, 0, 0,   0, 0, 0],

             [0, 0, 0,   0, 0, 0,   0, 0, 0],
             [0, 0, 0,   0, 0, 0,   0, 0, 0],
             [0, 0, 0,   0, 0, 0,   0, 0, 0]]
    return board


def display_graphics():
    # function displaying image and help

    # displaying image
    logo = pygame.image.load('res/obrazek.png')
    logo_x = 750
    logo_y = 1
    screen.blit(logo, (logo_x, logo_y))

    # Solver text
    s_font = pygame.font.Font('res/comic_sans.ttf', 20)
    s_text = s_font.render('Sudoku Solver', True, WHITE, BLACK)
    s_text_area = s_text.get_rect()
    s_text_area.center = (1050, 500)
    screen.blit(s_text, s_text_area)

    # help text
    h_font = pygame.font.Font('res/comic_sans.ttf', 15)
    h1_text = h_font.render('Select box with mouse or arrows',  True, WHITE)
    h2_text = h_font.render('ESC - clearing the board', True, WHITE)
    h3_text = h_font.render('ENTER - solving', True, WHITE)
    h4_text = h_font.render('0 to delete a number', True, WHITE)
    screen.blit(h1_text, (875, 550))
    screen.blit(h2_text, (875, 570))
    screen.blit(h3_text, (875, 590))
    screen.blit(h4_text, (875, 610))


def calculate_offset(x, y, grid_dim, margin):
    # function calculating grid box dimensions
    x_offset = ((x // 3) * 5) + 50
    y_offset = ((y // 3) * 5) + 50

    rect_width = x_offset + x * (grid_dim + margin)
    rect_height = y_offset + y * (grid_dim + margin)

    return rect_width, rect_height


def create_grid(board, invalids=None):
    # Creating grid

    # background
    if invalids is None:
        invalids = []
    grid_bg = pygame.Rect(45, 45, 659, 659)
    pygame.draw.rect(screen, WHITE, grid_bg)

    # grid
    for x in range(9):
        for y in range(9):
            (grid_rect_width, grid_rect_height) = calculate_offset(x, y, 70, 1)
            grid_elem = pygame.Rect(grid_rect_width,
                                    grid_rect_height,
                                    70,
                                    70)

            if (x, y) in invalids:
                # highlighting invalid inputs
                pygame.draw.rect(screen, ERROR_RED, grid_elem)

            else:
                # drawing rest of the grid
                pygame.draw.rect(screen, BLACK, grid_elem)

            # filling grid with numbers
            fill_grid(board, x, y)


def fill_grid(board, x=0, y=0):
    # function filling the grid with numbers
    (digit_top, digit_left) = calculate_offset(x, y, 70, 1)

    text_surface = sudoku_font.render(f'{board[y][x]}', True, WHITE)

    if board[y][x] != 0:
        screen.blit(text_surface, (digit_top + 25, digit_left + 10))


def highlight(x, y):
    # creating a box that highlights currently selected box
    x_hl_offset = ((x // 3) * 5) + 50
    y_hl_offset = ((y // 3) * 5) + 50

    hl_perim = pygame.Rect(x_hl_offset + x * 71, y_hl_offset + y * 71, 71, 71)
    pygame.draw.rect(screen, RED, hl_perim, 3)


# initializing mouse
def mouse():

    # checking when button is pressed
    buttons = pygame.mouse.get_pressed(num_buttons=3)
    if buttons[0]:

        # getting cursor position
        cursor_pos = pygame.mouse.get_pos()

        # calculating grid box
        if 50 <= cursor_pos[0] <= 699 and 50 <= cursor_pos[1] <= 699:
            x = (cursor_pos[0] - 50)//72.3
            y = (cursor_pos[1] - 50)//72.3

            # print(x, y)
            return int(x), int(y)


# Main loop
blank_sudoku = clear_board()
wrong_nums = []
while True:
    for event in pygame.event.get():

        # quitting solver
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # keyboard functions
        if event.type == pygame.KEYDOWN:

            # highlight rectangle positioning and chosing grid box
            if event.key == pygame.K_UP or pygame.K_DOWN or pygame.K_LEFT or pygame.K_RIGHT:
                if event.key == pygame.K_UP:
                    y_pos -= 1
                if event.key == pygame.K_DOWN:
                    y_pos += 1
                if event.key == pygame.K_LEFT:
                    x_pos -= 1
                if event.key == pygame.K_RIGHT:
                    x_pos += 1

                # boundring x_pos
                if x_pos > 8:
                    x_pos = 0
                if x_pos < 0:
                    x_pos = 8

                # boundring y_pos
                if y_pos > 8:
                    y_pos = 0
                if y_pos < 0:
                    y_pos = 8

            # input numbers to grid (sudoku board)
            if pygame.K_0 <= event.key <= pygame.K_9:
                blank_sudoku[y_pos][x_pos] = event.key - 48
                print(event.key)

            if pygame.K_KP0 <= event.key <= pygame.K_KP9:
                blank_sudoku[y_pos][x_pos] = event.key - 256

            # clearing board
            if event.key == pygame.K_ESCAPE:
                blank_sudoku = clear_board()
                wrong_nums = []

            # attempting solving
            if event.key == pygame.K_RETURN:

                # fail to solve
                if not board_validator(blank_sudoku):
                    # finding wrong inputs
                    wrong_nums = return_invalid(blank_sudoku)

                # successfully solving and printing
                else:
                    wrong_nums = []
                    sudoku_solver(blank_sudoku)
                    print_board(blank_sudoku)
                    create_grid(blank_sudoku)

    # setting background colour
    screen.fill(BLACK)

    # displaying right side of window
    display_graphics()

    # enabling mouse
    mouse_init = mouse()
    if mouse_init:
        (x_pos, y_pos) = mouse_init

    # creating grid and filling it
    create_grid(blank_sudoku, wrong_nums)

    # creating the highlight square
    highlight(x_pos, y_pos)

    # refreshing the screen
    pygame.display.flip()

    # setting tickrate
    clock.tick(60)
