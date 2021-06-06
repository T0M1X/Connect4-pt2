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
            grid[i][column] = playerID
            checkForWins(playerID, i, column)
            return


def takeTurn(playerID):
    valid = False
    while valid == False:
        try:
            column = int(input("Enter column: "))
            if column < 7 and column >= -1:
                valid = True
            else:
                print("\nEnter a number between 0 and 6.\n")
        except:
            print("\nEnter a number you crackhead.\n")
    if isPossible(column):
        placeCounter(playerID, column)


def countPieces(playerID, row, column, rowIncrement, columnIncrement):
    counter = 0

    try:
        x = row
        y = column
        while grid[x][y] == playerID:
            if counter >= 4:
                return 4

            counter += 1
            x += rowIncrement
            y += columnIncrement

        x = row - rowIncrement
        y = column - columnIncrement
        while grid[x][y] == playerID:
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
    # horizontal
    if countPieces(playerID, row, column, 1, 0) == 4:
        winSequence(playerID)

    # vertical
    if countPieces(playerID, row, column, 0, -1) == 4:
        winSequence(playerID)

    # 45-degrees left
    if countPieces(playerID, row, column, -1, -1) == 4:
        winSequence(playerID)

    # 45-degrees right
    if countPieces(playerID, row, column, 1, -1) == 4:
        winSequence(playerID)

#This function should pick a column based on weights and randomness
def ai():
    return


#Find all the possible moves the Ai can go (i.e. all columns that are not full)
#def possibleMoves():
    


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
