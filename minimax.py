from copy import deepcopy
import pygame
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
ROWS, COLS = 8, 8

red_pieces_left = 12
white_pieces_left = 12

def piecesLeft(board):
    redPieces = 0
    whitePieces = 0
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if(piece == 1 or piece == 3):
                whitePieces += 1
            elif(piece == 2 or piece == 4):
                redPieces += 1
    if redPieces == 0 or whitePieces == 0:
        return True
    else:
        return False


def minimax(depth, posBoard, maxPlayer, alpha, beta):
    if(depth == 0 or piecesLeft(posBoard)):
        return evaluationFunction(posBoard), posBoard
    #Maximazing Player -> WHITE
    if maxPlayer:
        maxValue = float('-inf')
        maxAction = None
        for action in possibleLegalActions(maxPlayer, posBoard): #for every action possible at that position
            successor = minimax(depth - 1, posBoard, False, alpha, beta)
            if successor[0] > maxValue:
                maxValue = successor[0]
                maxAction = successor[1]
                alpha = max(alpha, maxValue)
                if maxValue > beta:
                    return maxValue, maxAction
        return maxValue, maxAction
    else: # If minizing -> RED
        minValue = float('inf')
        minAction = None
        for action in possibleLegalActions(maxPlayer, posBoard):
            successor = minimax(depth - 1, action, True, alpha, beta)
            if successor[0] < minValue:
                minValue = successor[0]
                minAction = action
                beta = min(beta, minValue)
                if minValue < alpha:
                    return (minValue, minAction)
        return minValue, minAction 


def possibleLegalActions(player, board):
    possibleActions = []
    if player: #if player = true => WHITE
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]
                if(piece == 1 or piece == 3): # white piece or king
                    if(piece == 3): #checks to see if that piece is king ONLY -> its exception actions
                        if(col > 0 and row < 7 and board[row + 1][col - 1] == 0): #checks if space left backward disgonally is open 
                            newBoard = deepcopy(board)
                            newBoard[row][col] = 0 #sets current space 0
                            newBoard[row + 1][col - 1] = piece #sets the diagonal space/square to that piece/checker
                            possibleActions.append(newBoard)
                        if(col < 7 and row < 7 and board[row + 1][col + 1] == 0): #checks to see if space right backward diagonally is open                               
                            newBoard = deepcopy(board)
                            newBoard[row][col] = 0 #sets current space 0
                            newBoard[row + 1][col + 1] = piece
                            possibleActions.append(newBoard)
                        #checks to see if there exists red piece rigth diagonally for king for capture
                        if(row < 6 and col < 6 and (board[row + 1][col + 1] == 2 or board[row + 1][col + 1] == 4)): 
                            if(board[row + 2][col + 2] == 0): #checks to see if there exists empty space next to red piece
                                newBoard = deepcopy(board)
                                newBoard[row + 1][col + 1] = 0 #sets an empty space to red piece position
                                newBoard[row + 2][col + 2] = piece #sets empty space to king piece
                                newBoard[row][col] = 0 #sets current king position to empty 
                                possibleActions.append(newBoard)
                        #checks to see if there exists red piece diagonalky for king left for capture
                        if(row > 1 and col < 6 and (board[row + 1][col - 1] == 2 or board[row + 1][col - 1] == 4)): 
                            if(board[row + 2][col - 2] == 0): #checks to see if there exists empty space next to red piece
                                newBoard = deepcopy(board)
                                newBoard[row + 1][col - 1] = 0 #sets an empty space to red piece position
                                newBoard[row + 2][col - 2] = piece #sets empty space to king piece
                                newBoard[row][col] = 0 #sets current king position to empty 
                                possibleActions.append(newBoard)
                    if(row > 0 and col < 7 and board[row - 1][col + 1] == 0): #checking if move diagonally left is possible
                        newBoard = deepcopy(board)
                        newBoard[row][col] = 0 #makes current position a 0 -> an open space
                        if(piece == 1 and row - 1 == 0): # checks to see if piece can become king
                            newBoard[row - 1][col + 1] = 3 #sets it to a king white piece
                        else:
                            newBoard[row - 1][col + 1] = piece #sets the diagonal left open space to that piece
                        possibleActions.append(newBoard)
                    if(row > 0 and col > 0 and board[row - 1][col - 1] == 0): # checking to see if move diagonaly right is possible 
                        newBoard = deepcopy(board)
                        newBoard[row][col] = 0 #makes current space free/open 
                        if(piece == 1 and row - 1 == 0): #checks to see if piece can become king
                            newBoard[row - 1][col - 1] = 3 #sets piece to king white piece
                        else:
                            newBoard[row - 1][col - 1] = piece #sets the space located diagonally right to the piece
                        possibleActions.append(newBoard)
                        #checking if there exists a red piece disgonally to the left 
                    if(row > 1 and col > 1 and (board[row - 1][col - 1] == 2 or board[row - 1][col - 1] == 4)): 
                        if(board[row-2][col-2] == 0): #checks if so, does there exist an empty space diagonally after that red piece
                            newBoard = deepcopy(board) #makes copy of board
                            newBoard[row - 1][col - 1] = 0 # "removes" red piece from board
                            if (row - 2 == 0 and piece == 1): #checks to see if piece can become king -> if so need to change its num.
                                newBoard[row - 2][col - 2] = 3 # the piece has reached the opposite side and becomes a king
                            else:
                                #sets the square/space after that red piece diagonally to the white piece that captured it
                                newBoard[row - 2][col - 2] = piece 
                            newBoard[row][col] = 0 #sets the current position of that white piece to be empty 
                            possibleActions.append(newBoard)  
                    #checking if there exists a red piece diagonally to the right
                    if(row > 1 and col < 6 and (board[row - 1][col + 1] == 2 or board[row - 1][col + 1] == 4)):
                        #if so, checks to see if there exists an empty space left diagonally after that red piece 
                        # such that it can perform the capture 
                        if(board[row - 2][col + 2] == 0): 
                            newBoard = deepcopy(board) #makes copy of board
                            #sets an empty space to the place where the red piece is as the capture is performed
                            newBoard[row - 1][col + 1] = 0 
                            if(row - 2 == 0 and piece == 1): #checks to see if piece can become king upon capture
                               newBoard[row - 2][col + 2] = 3 # the piece has reached the opposite side and becomes a king
                            else: 
                                newBoard[row - 2][col + 2] = piece #if not, sets to piece = 1
                            newBoard[row][col] = 0 #sets current position to empty space = 0
                            possibleActions.append(newBoard)

    else: #player is red -> AI
        for row in range(ROWS):
            for col in range(COLS):
                newBoard = deepcopy(board)
                piece = board[row][col]
                if(piece == 2 or piece == 4): # red piece or king
                    if(piece == 4): #checks to see if piece is king
                        if(col > 0 and row > 0 and board[row - 1][col - 1] == 0): #checks if space left backward disgonally is open 
                            newBoard = deepcopy(board)
                            newBoard[row][col] = 0 #sets current space 0
                            newBoard[row - 1][col - 1] = piece
                            possibleActions.append(newBoard)
                        if(col < 7 and row > 0 and board[row - 1][col + 1] == 0): #checks to see if space right backward diagonally is open                             
                            newBoard = deepcopy(board)
                            newBoard[row][col] = 0 #sets current space 0
                            newBoard[row - 1][col + 1] = piece
                            possibleActions.append(newBoard)
                        #checks to see if there exists white piece left backward diagonally 
                        if(row > 1 and col > 1 and piece == 4 and (board[row - 1][col - 1] == 1 or board[row - 1][col - 1] == 3)): 
                            if(board[row - 2][col - 2] == 0): #checks to see if space exists next to white piece
                                newBoard = deepcopy(board)
                                newBoard[row - 1][col - 1] = 0 #sets the current position where white piece resides to empty
                                newBoard[row - 2][col - 2] = piece #sets the position where the capture occured to king/piece
                                newBoard[row][col] = 0 #sets current position where king resides to empty
                                possibleActions.append(newBoard)
                        #checks to see if there exists white piece right backward diagonally 
                        if(row > 1 and col < 6 and (board[row - 1][col + 1] == 1 or board[row - 1][col + 1] == 3)): 
                            if(board[row - 2][col + 2] == 0): #checks to see if space exists next to white piece
                                newBoard = deepcopy(board)
                                newBoard[row - 1][col + 1] = 0 #sets the current position where white piece resides to empty
                                newBoard[row - 2][col + 2] = piece #sets the position where the capture occured to king/piece
                                newBoard[row][col] = 0 #sets current position where king resides to empty
                                possibleActions.append(newBoard)
                    if(row < 7 and col < 7 and board[row + 1][col + 1] == 0): # checking to see if move diagonaly right is possible 
                        newBoard = deepcopy(board)
                        newBoard[row][col] = 0 #makes current space free/open 
                        if(piece == 2 and row + 1 == 7): #checks to see if piece can become king
                            newBoard[row + 1][col + 1] = 4 #sets piece to king
                        else:
                            newBoard[row + 1][col + 1] = piece #sets the space located diagonally right to the piece
                        possibleActions.append(newBoard)
                    if(row < 7 and col > 0 and board[row + 1][col - 1] == 0): #checking if move diagonally left is possible 
                        newBoard = deepcopy(board)
                        newBoard[row][col] = 0 #makes current position a 0 -> an open space
                        if(piece == 2 and row + 1 == 7): # checks to see if piece can become king
                            newBoard[row + 1][col - 1] = 4 #sets it to a king piece
                        else:
                            newBoard[row + 1][col - 1] = piece #sets the diagonal left open space to that piece
                        possibleActions.append(newBoard)
                        #checks to see if can capture to the left
                    if (row < 6 and col > 1 and (board[row + 1][col - 1] == 1 or board[row + 1][col - 1] == 3)): 
                        if(board[row + 2][col - 2] == 0): #if so, checks to see if the space next to the white piece diagonally is free
                            newBoard = deepcopy(board) #copy of board to append to list as possible actions
                            newBoard[row + 1][col - 1] = 0 
                            if(row + 2 == 7 and piece == 2): #checks to see if red piece can become king upon capture
                                newBoard[row + 2][col - 2] = 4 
                            else:
                                newBoard[row + 2][col - 2] = piece 
                            newBoard[row][col] = 0 
                            possibleActions.append(newBoard) 
                            #checks to see if there exists a white piece to the right
                    if(row < 6 and col < 6 and (board[row + 1][col + 1] == 1 or board[row + 1][col + 1] == 3)): 
                        if(board[row + 2][col + 2] == 0): #checks to see if space exists next to the white piece
                            newBoard = deepcopy(board)
                            newBoard[row + 1][col + 1] = 0 #sets the current space where the white piece resides to empty = 0
                            if(row + 2 == 7 and piece == 2): #checks to see after performing capture leads to be piece becoming king
                                newBoard[row + 2][col + 2] = 4 
                            else:
                                newBoard[row + 2][col + 2] = piece 
                            newBoard[row][col] = 0 
                            possibleActions.append(newBoard) 

    return possibleActions

def evaluationFunction(board):
    redPieces = 0
    whitePieces = 0
    redKings = 0
    whiteKings = 0
    for row in range(ROWS):
        for col in range(COLS): #each row and column
            piece = board[row][col] #w each piece add 1 to each checker
            if piece == 1:
                whitePieces += 1
            elif piece == 2:
                redPieces += 1
            elif piece == 3: 
                whiteKings += 1
            elif piece == 4:
                redKings += 1
    # # of kings will be multiplied w more weight 
    return whitePieces - redPieces + (2*whiteKings - 2*redKings) #more weights to kings