# main file for coding the game
import random
import time
import sqlite3


grid = [[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]]
isGameRunning = True


def printGrid():
    for i in range(len(grid)):
        print(grid[i])


def isPossible(column):
    if grid[0][column] == 0:
        return True
    else:
        return False


def placeCounter(playerID, column):
    for i in range(0, len(grid)):
        if i + 1 >= len(grid) or grid[i + 1][column] != 0:
            #if the loop isnt at the bottom or the next row has a counter inside
            grid[i][column] = playerID
            checkForWins(playerID, i, column)
            return


def takeTurn(playerID):
    valid = False
    
    if playerID == 2: #Player 2 is now the ai
        column = ai()
        valid = True
    
    while valid == False:
        try:
            column = int(input("Enter column: "))
            if column < 7 and column >= -1:
                if isPossible(column):
                    valid = True
                else:
                    print("That column is full!")
            else:
                print("\nEnter a number between 0 and 6.\n")
        except:
            print("\nEnter a number you crackhead.\n")
    placeCounter(playerID, column)


def countPieces(playerID, row, column, rowIncrement, columnIncrement):
    counter = 0

    try:
        x = row
        y = column
        while grid[x][y] == playerID and x >= 0 and y >= 0:
            if counter >= 4:
                return 4
            counter += 1
            x += rowIncrement
            y += columnIncrement

        x = row - rowIncrement
        y = column - columnIncrement
        while grid[x][y] == playerID  and x >= 0 and y >= 0:
            if counter >= 4:
                return 4
            counter += 1
            
            x -= rowIncrement
            y -= columnIncrement

        return counter
    except:
        return counter


def winSequence(playerID):
    global isGameRunning

    printGrid()
    print(playerID, " wins!!!")
    isGameRunning = False


def checkForWins(playerID, row, column):
    # vertical
    if countPieces(playerID, row, column, 1, 0) == 4:
        print("vertical win")
        winSequence(playerID)
        return

    # horizontal
    if countPieces(playerID, row, column, 0, -1) == 4:
        print("horizontal win")
        winSequence(playerID)
        return

    # 45-degrees left
    if countPieces(playerID, row, column, -1, -1) == 4:
        print("diaganol left win")
        winSequence(playerID)
        return

    # 45-degrees right
    if countPieces(playerID, row, column, 1, -1) == 4:
        print("diaganol right win")
        winSequence(playerID)
        return

#This function should pick a column based on weights and randomness
def ai():
    weights=[0,0,0,0,0,0,0]
    available = possibleMoves()
    choice = random.randint(0,len(available) -1)
    return available[choice]


#Find all the possible moves the Ai can go (i.e. all columns that are not full)
def possibleMoves():
    possibles = []
    for i in range(0,7):
        if grid[0][i] == 0:
            possibles.append(i)
    return possibles
        

turnCounter = 0
# game
while isGameRunning:
    printGrid()
    if turnCounter % 2:
        # player 2's turn
        takeTurn(2)

    else:
        # player 1's turn
        takeTurn(1)

    turnCounter += 1
