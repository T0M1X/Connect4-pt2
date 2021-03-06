# main file for coding the game
import random
import time
import sqlite3
from os import getcwd

import numpy as np


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
            # if the loop isn't at the bottom or the next row has a counter inside
            grid[i][column] = playerID
            checkForWins(playerID, i, column)
            return


def isAIorPlayer(playerID):
    global gameMode

    if gameMode == 1:
        return "human"
    elif gameMode == 2:
        if playerID == 2:
            return "AI"
        else:
            return "human"
    elif gameMode == 3:
        if playerID == 1:
            return "AI"
        else:
            return "human"
    else:
        return "AI"


def takeTurn(playerID):
    if isAIorPlayer(playerID) == "human":

        valid = False
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
        currentState=""
        for i in range(0, 6):
            for j in range(0, 7):
                currentState += str(grid[i][j])
        available = possibleMoves()
        numColumns = len(available)
        usedStates[0].append(currentState)
        usedStates[1].append(playerID)
        usedStates[2].append(numColumns)
        usedStates[3].append(column)
        c.execute("SELECT aw FROM states WHERE state=?",
                  (currentState,))

        # If this state is not in the database then this state
        # will be inserted into the db.
        if not c.fetchall():
            print("\n \n \n \n ")
            c.execute("""INSERT INTO states(state,aw,bw,cw,dw,ew,fw,gw)
                        VALUES(?,0,0,0,0,0,0,0)""",
                      (currentState,))
            con.commit()
            print("Record inserted successfully into table ", c.rowcount)
    else:
        column = ai(playerID)
        
    placeCounter(playerID, column)


def countPieces(playerID, row, column, rowIncrement, columnIncrement):
    counter = 0

    try:
        x = row
        y = column
        print(0,x,y)
        while grid[x][y] == playerID and x >= 0 and y >= 0:
            if counter >= 4:
                return 4
            counter += 1
            x += rowIncrement
            y += columnIncrement
            print(counter,x,y)
        x = row - rowIncrement
        y = column - columnIncrement
        while grid[x][y] == playerID and x >= 0 and y >= 0:
            if counter >= 4:
                return 4
            counter += 1

            x -= rowIncrement
            y -= columnIncrement
            print(counter,x,y)
        return counter
    except:
        return counter


def winSequence(playerID):
    global isGameRunning
    global isSessionFinished

    printGrid()
    print(playerID, " wins!!!")
    isGameRunning = False
    modifyWeights(playerID)

    decision = ""
    while decision != "y" and decision != "n":
        decision = input("Rematch? y/n: ")
    if decision == "n":
        isSessionFinished = True


def drawSequence():
    global isGameRunning
    global isSessionFinished

    printGrid()
    print("Game drawn")
    isGameRunning = False

    decision = ""
    while decision != "y" and decision != "n":
        decision = input("Rematch? y/n: ")
    if decision == "n":
        isSessionFinished = True


# This function will modify the weights for the Ai
def modifyWeights(winner):
    for i in range(0,len(usedStates[0])):
        if usedStates[1][i] == winner:
            c.execute("""SELECT aw,bw,cw,dw,ew,fw,gw FROM states
                      WHERE state=?""",
                      (usedStates[0][i],))
            temp=c.fetchall()[0]
            weights=[]
            for j in range(0,len(temp)):
                weights.append(temp[j])
            for j in range(0,usedStates[2][i]):
                if weights[j] > (0 - usedStates[2][i]**3):
                    weights[j] -= 1
                    weights[usedStates[3][i]] += 1
            c.execute("""UPDATE states SET aw=?, bw=?, cw=?,
            dw=?, ew=?, fw=?, gw=? WHERE state=?""",
                              (weights[0],weights[1],weights[2],weights[3],
                               weights[4],weights[5],weights[6],
                               usedStates[0][i]))
            con.commit()
        else:
            c.execute("""SELECT aw,bw,cw,dw,ew,fw,gw FROM states
                      WHERE state=?""",
                      (usedStates[0][i],))
            temp=c.fetchall()[0]
            weights=[]
            for j in range(0,len(temp)):
                weights.append(temp[j])
            for j in range(0,usedStates[2][i]):
                if weights[usedStates[3][i]] > (0 - usedStates[2][i]**3):
                    weights[j] += 1
                    weights[usedStates[3][i]] -= 1
            c.execute("""UPDATE states SET aw=?, bw=?, cw=?,
            dw=?, ew=?, fw=?, gw=? WHERE state=?""",
                              (weights[0],weights[1],weights[2],weights[3],
                               weights[4],weights[5],weights[6],
                               usedStates[0][i]))
            con.commit()
    

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
        print("diagonal left win")
        winSequence(playerID)
        return

    # 45-degrees right
    if countPieces(playerID, row, column, -1, 1) == 4:
        print("diagonal right win")
        winSequence(playerID)
        return

    # game drawn
    if sum(x.count(0) for x in grid) == 0:
        drawSequence()
        return


# This function should pick a column based on weights and randomness
def ai(playerID):
    inverse = []
    available = possibleMoves()
    numColumns = len(available)
    currentState = ""
    for i in range(0, 6):
        for j in range(0, 7):
            currentState += str(grid[i][j])
    usedStates[0].append(currentState)
    usedStates[1].append(playerID)
    usedStates[2].append(numColumns)
    c.execute("SELECT aw FROM states WHERE state=?",
              (currentState,))

    # If this state is not in the database then this state
    # will be inserted into the db.
    if not c.fetchall():
        print("\n \n \n \n ")
        c.execute("""INSERT INTO states(state,aw,bw,cw,dw,ew,fw,gw)
                    VALUES(?,0,0,0,0,0,0,0)""",
                  (currentState,))
        con.commit()
        print("Record inserted successfully into table ", c.rowcount)
    for i in range(0, numColumns):
        inverse.append(1 / numColumns)
    choice = pickColumn(available, getWeights(currentState), inverse)
    usedStates[3].append(choice)
    print("I choose column " + str(choice))
    return choice


# Returns an array of the weights for that state
def getWeights(state):
    weights = []
    c.execute("SELECT aw,bw,cw,dw,ew,fw,gw FROM states WHERE state=?",
              (state,))
    allWeights = c.fetchall()
    for i in range(0, 7):
        weights.append(allWeights[0][i])
    return weights


# This function will pick the column and takes in account weights from
# the database and also the number of available columns there are.
def pickColumn(moves, weights, probabilities):
    finalWeights = []
    numProb = len(probabilities)
    for i in range(0, numProb):
        finalWeights.append(weights[moves[i]])
    for i in range(0, numProb):
        probabilities[i] += (finalWeights[i]/(numProb**4))
    choice = np.random.choice(moves, p=probabilities)
    return choice


# Find all the possible moves the Ai can go (i.e. all columns that are not full)
def possibleMoves():
    possibles = []
    for i in range(0, 7):
        if grid[0][i] == 0:
            possibles.append(i)
    return possibles


isSessionFinished = False

print("1 - Player vs. Player \n"
      "2 - Player vs. AI \n"
      "3 - AI vs. Player \n"
      "4 - AI vs. AI")

gameMode = 10
while gameMode < 1 or gameMode > 4:
    try:
        gameMode = int(input("Enter game mode: "))
    except:
        print("\nEnter a number you crackhead.\n")

while not isSessionFinished:
    grid = [[0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]]
    isGameRunning = True
    usedStates = [[],[],[],[]]
    con = sqlite3.connect("Ai.db")
    c = con.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS states(
        state text,
        aw integer,
        bw integer,
        cw integer,
        dw integer,
        ew integer,
        fw integer,
        gw integer);""")

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
    con.commit()
    c.close()
    con.close()
