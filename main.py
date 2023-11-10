import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Sound effects
place_sound = pygame.mixer.Sound("scribble.wav")
win_sound = pygame.mixer.Sound("winner.wav")

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
# RGB Colors
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tanner's Tic Tac Toe")
screen.fill(BG_COLOR)

# Board
board = [[None] * BOARD_ROWS for _ in range(BOARD_COLS)]

# Functions
def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_win(player):
    # Vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True
    # Horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True
    # Ascending diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True
    # Descending diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True
    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    if player == 'O':
        color = CIRCLE_COLOR
    elif player == 'X':
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), WIN_LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    if player == 'O':
        color = CIRCLE_COLOR
    elif player == 'X':
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH)

def draw_asc_diagonal(player):
    if player == 'O':
        color = CIRCLE_COLOR
    elif player == 'X':
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH)

def draw_desc_diagonal(player):
    if player == 'O':
        color = CIRCLE_COLOR
    elif player == 'X':
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

draw_lines()

# Additions for save and load feature
def save_game():
    with open('tictactoe_save.json', 'w') as file:
        json.dump(board, file)

def load_game():
    try:
        with open('tictactoe_save.json', 'r') as file:
            loaded_board = json.load(file)
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    board[row][col] = loaded_board[row][col]
            return True
    except FileNotFoundError:
        return False

def display_text(message, pos_y, font_size=20, color=(0, 0, 0)):
    font = pygame.font.Font(None, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, pos_y))
    screen.blit(text, text_rect)

# Initialize the game state
player = 'X'  # Player X always starts
game_over = False  # Game is not over at the start

# Main loop
# Modify the main loop to include save/load and sound effects
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                place_sound.play()
                if check_win(player):
                    win_sound.play()
                    game_over = True
                player = 'O' if player == 'X' else 'X'

                draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Press 'S' to save the game
                save_game()
            elif event.key == pygame.K_l:  # Press 'L' to load the last saved game
                if load_game():
                    draw_figures()
            elif event.key == pygame.K_r:  # Press 'R' to restart the game
                restart()
                player = 'X'
                game_over = False

    # Display instructions
    display_text('Press S to Save | L to Load | R to Restart', 10)

    pygame.display.update()