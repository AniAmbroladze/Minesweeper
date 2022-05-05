import pygame
from cell import Cell
import random


class Board():
    def __init__(self, size, totalNumMines):
        self.size = size
        self.totalNumMines = totalNumMines
        self.numNonMineCells = size[0]*size[1] - totalNumMines
        self.openCellSet = set()
        self.totalNumFlaggedCells = 0
        self.board = []
        self.setBoard()

    def setBoard(self):
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                cell = Cell()
                row.append(cell)
            self.board.append(row)
        self.setMines()
        self.setNeighbours()

    def setMines(self):
        uniqIndexList = set()
        while len(uniqIndexList) < self.totalNumMines:
            x, y = random.randint(
                0, self.size[0]-1), random.randint(0, self.size[1]-1)
            if not (x, y) in uniqIndexList:
                uniqIndexList.add((x, y))
                self.board[x][y].hasMine = True

    def setNeighbours(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.board[row][col].hasMine == False:
                    self.board[row][col].numMines = self.getNumSurroundingMines(
                        row, col)

    def getNumSurroundingMines(self, row, col):
        nMines = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x+row >= 0 and x+row < self.size[0]) and (y+col >= 0 and y+col < self.size[1]):
                    if x == 0 and y == 0:
                        continue
                    if self.board[x+row][y+col].hasMine:
                        nMines += 1
                    else:
                        self.board[row][col].neighList.append((x+row, y+col))
        return nMines
