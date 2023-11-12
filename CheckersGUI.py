import pygame
from minimax import minimax
# Constants
WIDTH, HEIGHT = 400, 400
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
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

        #check if capture piece
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

# Main loop
running = True
while running:

    if(current_player == 2): #ai player
        #print("Current Player 2")
        #print(board)
        value, actionBoard = minimax(3, board, True, float("-inf"), float("inf"))
      #  print("-----------------------")
      #  print(actionBoard)
        for row in range(ROWS):
            for col in range(COLS):
                board[row][col] = actionBoard[row][col]
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
        running = False
        print("Player 1 has won the game")
    if red_pieces_left == 0:
        running = False
        print("Player 2 has won the game")

    pygame.display.flip()

pygame.quit()
