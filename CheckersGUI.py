import pygame
from minimax import minimax
# Constants
WIDTH, HEIGHT = 400, 400
WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
CROWN = pygame.transform.scale(pygame.image.load('./crown.png'), (44, 25))

red_pieces_left = 12
white_pieces_left = 12

# Initialize the player
current_player = 1  # Player 1 starts

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# Define restart button rectangle
restart_button_width = 200
restart_button_height = 50
restart_button_x = (WIDTH - restart_button_width) // 2
restart_button_y = (HEIGHT - restart_button_height) // 2
restart_button_rect = pygame.Rect(restart_button_x, restart_button_y+40, restart_button_width, restart_button_height)
quit_button_rect = pygame.Rect(restart_button_x, restart_button_y-40, restart_button_width, restart_button_height)

# Define restart text
font = pygame.font.Font(pygame.font.get_default_font(), 36)
restart_text = font.render("Restart", True, WHITE)
restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
quit_text = font.render("Quit", True, WHITE)
quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)

# Example piece representation: 0 for empty, 1 for white, 2 for red
board = [
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0]
]

selected_piece = None  # Store the selected piece position

# Function to draw the board
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw board pieces
def draw_pieces(board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece == 1:  # White piece
                pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif piece == 2:  # Red piece
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif piece == 3: # White king
                pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
                screen.blit(CROWN, ((col * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3))
            elif piece == 4: # Red king
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
                screen.blit(CROWN, ((col * SQUARE_SIZE) + 3, (row * SQUARE_SIZE) + 3))

# Check if the move is valid
def is_valid_move(board, start, end, player):
    # Ensure that the starting position contains the player's piece
    if board[start[0]][start[1]] == player or board[start[0]][start[1]] == player + 2:

        # Determine the move direction based on the player (1 for white, 2 for red)
        move_direction = -1 if player == 1 else 1

        # Calculate the move distance
        move_row = end[0] - start[0]
        move_col = end[1] - start[1]
        
        if board[start[0]][start[1]] == 1 or board[start[0]][start[1]] == 2:
            if (move_direction * move_row <= 0):
                return False
        # check if capture piece
        if capture_piece(board, start, end):
            return True
        # Check for valid diagonal move (must move by 1 in both row and col)
        if abs(move_row) != 1 or abs(move_col) != 1:
            return False
        # Regular move: an empty destination square
        if board[end[0]][end[1]] == 0:
            return True

    return False

# Function to switch players
def switch_player(current_player):
    return 3 - current_player  # Assuming players are represented as 1 and 2

# Function to check if square is black square
def isBlack(board, square):
    if (square[0] + square[1]) % 2 != 0:
        return True

# Function to capture a piece
def capture_piece(board, start, end):

    # making the variables point to the global one
    # so the amount of pieces is updated correctly
    global red_pieces_left
    global white_pieces_left

    move_row = end[0] - start[0]
    move_col = end[1] - start[1]
    capture_row_forwards = start[0] + move_row // 2
    capture_col_forwards = start[1] + move_col // 2
    # if end square selected was not black, return false
    if not isBlack(board, end):
        return False
    if (
        0 <= capture_row_forwards < ROWS
        and 0 <= capture_col_forwards < COLS
        and board[capture_row_forwards][capture_col_forwards] != 0
        and board[capture_row_forwards][capture_col_forwards] != board[start[0]][start[1]]
        and board[end[0]][end[1]] == 0
        and abs(move_row) == 2
    ):
        # decrementing the number of pieces left for the side where the piece is captured
        if board[capture_row_forwards][capture_col_forwards] == 1:
            white_pieces_left = white_pieces_left - 1
        else:
            red_pieces_left = red_pieces_left - 1
        #print("Num red left: " + str(red_pieces_left))
        #print("Num white left: " + str(white_pieces_left))

        board[capture_row_forwards][capture_col_forwards] = 0
        return True
    # Can only capture backwards if we have a king
    if board[start[0]][start[1]] == 3 or board[start[0]][start[1]] == 4:
        capture_row_backwards = start[0] + move_row // 2
        capture_col_backwards = start[1] + move_col // 2
        if (
            0 <= capture_row_backwards < ROWS
            and 0 <= capture_col_backwards < COLS
            and board[capture_row_backwards][capture_col_backwards] != 0
            and board[capture_row_backwards][capture_col_backwards] != board[start[0]][start[1]]
            and board[end[0]][end[1]] == 0
            and abs(move_row) == 2
        ):
            # decrementing the number of pieces left for the side where the piece is captured
            if board[capture_row_backwards][capture_col_backwards] == 1:
                white_pieces_left = white_pieces_left - 1
            else:
                red_pieces_left = red_pieces_left - 1
            #print("Num red left: " + str(red_pieces_left))
            #print("Num white left: " + str(white_pieces_left))

            board[capture_row_backwards][capture_col_backwards] = 0
            return True
    return False

def has_legal_moves(board, player):
    # checks if player has any legal moves
    # returns false if no legal moves exist, or if no pieces are left
    # legal moves include moves where a piece is jumped over and taken
    for row in range(ROWS):
        for col in range(COLS):
            #check player 1
            if player == 1:
                if board[row][col] == 1 or board[row][col] == 3:
                    # Check for legal moves for player 1's normal pieces
                    if (has_move(board, row, col, row - 1, col - 1)
                            or has_move(board, row, col, row - 1, col + 1)
                            or has_move(board, row, col, row - 2, col - 2)
                            or has_move(board, row, col, row - 2, col + 2)):
                        return True
                if board[row][col] == 3:
                    # Check backward moves for player 1's kings
                    if (has_move(board, row, col, row + 1, col - 1)
                            or has_move(board, row, col, row + 1, col + 1)
                            or has_move(board, row, col, row + 2, col - 2)
                            or has_move(board, row, col, row + 2, col + 2)):
                        return True
            #check player 2
            if player == 2:
                if board[row][col] == 2 or board[row][col] == 4:
                    # Check for legal moves for player 2's normal pieces
                    if (has_move(board, row, col, row + 1, col - 1)
                            or has_move(board, row, col, row + 1, col + 1)
                            or has_move(board, row, col, row + 1, col - 2)
                            or has_move(board, row, col, row + 2, col + 2)):
                        return True
                if board[row][col] == 4:
                    # Check backward moves for player 2's kings
                    if (has_move(board, row, col, row - 1, col - 1)
                            or has_move(board, row, col, row - 1, col + 1)
                            or has_move(board, row, col, row - 2, col - 2)
                            or has_move(board, row, col, row - 2, col + 2)):
                        return True
    return False

def has_move(board, from_row, from_col, to_row, to_col):
    if 0 <= to_row < ROWS and 0 <= to_col < COLS:
        if board[to_row][to_col] == 0:
            return True
    return False

def piecesLeftAI(board):
    global red_pieces_left
    global white_pieces_left
    redPieces = 0
    whitePieces = 0
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if(piece == 1 or piece == 3):
                whitePieces += 1
            elif(piece == 2 or piece == 4):
                redPieces += 1
    red_pieces_left = redPieces
    white_pieces_left = whitePieces

def difficulty_screen():
    font_title = pygame.font.Font(None, 42)
    title_text = font_title.render("CS 5804 Mini Project:", True, WHITE)
    title_text2 = font_title.render("Checkers AI", True, WHITE)

    font = pygame.font.Font(None, 32)
    easy_text = font.render("Easy (AI Depth: 2)", True, WHITE)
    medium_text = font.render("Medium (AI Depth: 3)", True, WHITE)
    hard_text = font.render("Hard (AI Depth: 4)", True, WHITE)

    screen.fill(BLACK)
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 16))
    screen.blit(title_text2, ((WIDTH - title_text2.get_width()) // 2, 2.2* HEIGHT // 16))


    screen.blit(easy_text, (WIDTH // 4,  3* HEIGHT // 8))
    screen.blit(medium_text, (WIDTH // 4, HEIGHT // 2))
    screen.blit(hard_text, (WIDTH // 4, 5 * HEIGHT // 8))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 4 <= x <= WIDTH // 4 + easy_text.get_width() and 3 * HEIGHT // 8 <= y <= 3 * HEIGHT // 8 + easy_text.get_height():
                    #print(2)
                    return 2  # AI Depth for Easy
                elif WIDTH // 4 <= x <= WIDTH // 4 + medium_text.get_width() and HEIGHT // 2 <= y <= HEIGHT // 2 + medium_text.get_height():
                    #print(3)
                    return 3  # AI Depth for Medium
                elif WIDTH // 4 <= x <= WIDTH // 4 + hard_text.get_width() and 5 * HEIGHT // 8 <= y <= 5 * HEIGHT // 8 + hard_text.get_height():
                    #print(4)
                    return 4  # AI Depth for Hard


# Main loop
running = True
gameEnded = False
set_difficulty = False
while running:
    if not set_difficulty:
        ai_difficulty = difficulty_screen()
        set_difficulty = True
    if gameEnded:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if restart button is selected, restart game board and pieces
                if restart_button_rect.collidepoint(event.pos):
                    gameEnded = False
                    board = [
                        [0, 2, 0, 2, 0, 2, 0, 2],
                        [2, 0, 2, 0, 2, 0, 2, 0],
                        [0, 2, 0, 2, 0, 2, 0, 2],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 1, 0, 1, 0, 1, 0],
                        [0, 1, 0, 1, 0, 1, 0, 1],
                        [1, 0, 1, 0, 1, 0, 1, 0]
                    ]
                    white_pieces_left = 12
                    red_pieces_left = 12
                    selected_piece = None
                    current_player = 1
                    break
                # if quit button is selected,terminate running loop
                if quit_button_rect.collidepoint(event.pos):
                    current_player = -1
                    running = False
                    break
        continue
    if(current_player == 2): #ai player
        #print("Current Player 2")
        #print(board)
        value, actionBoard = minimax(ai_difficulty, board, False, float("-inf"), float("inf"))
      #  print("-----------------------")
      #  print(actionBoard)
        for row in range(ROWS):
            for col in range(COLS):
                if actionBoard != None:
                    board[row][col] = actionBoard[row][col]
                else:
                    print("No legal moves left for Player ", current_player, ". Player ", (current_player % 2 + 1), " has won")
                    gameEnded = True
                    break
                
        piecesLeftAI(board)
       # print(board)
        current_player = switch_player(current_player)               
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print(current_player)
                x, y = event.pos
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                if board[row][col] == current_player or board[row][col] == current_player + 2:
                    selected_piece = (row, col)
                        # print(selected_piece)                          
                if selected_piece != None:
                    if is_valid_move(board, selected_piece, (row, col), current_player):
                        board[row][col] = board[selected_piece[0]][selected_piece[1]]
                        board[selected_piece[0]][selected_piece[1]] = 0
                        if (current_player == 1 and row == 0) or (current_player == 2 and row == ROWS - 1):
                            if board[row][col] != 3 or board[row][col] != 4:
                                board[row][col] = current_player + 2  # Assign a value to represent a king
                        selected_piece = None
                        current_player = switch_player(current_player)               
                    # Inside your main loop, after a valid move is made, switch to the next player
    draw_board()
    draw_pieces(board)
    #checks how many pieces are left
    if white_pieces_left == 0:
        print("Player 1 has won the game")
    if red_pieces_left == 0:\
        print("Player 2 has won the game")
    # check if next player has available moves left
    if not has_legal_moves(board, current_player):
        print("No legal moves left for Player ", current_player, ". Player ", (current_player % 2 + 1), " has won")
        gameEnded = True
    #add restart and quit buttons if game has ended
    if gameEnded:
        pygame.draw.rect(screen, GREEN, restart_button_rect)
        pygame.draw.rect(screen, BLUE, quit_button_rect)
        screen.blit(quit_text, quit_text_rect)
        screen.blit(restart_text, restart_text_rect)
    pygame.display.flip()

pygame.quit()
