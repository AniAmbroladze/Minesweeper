import pygame
from cell import Cell


class UI():
    def __init__(self, boardClass, screenSize):
        self.boardClass = boardClass
        self.board = boardClass.board
        self.boardSize = boardClass.size
        self.screenSize = screenSize
        self.iconSize = self.screenSize[0] // \
            self.boardSize[1], self.screenSize[1]//self.boardSize[0]
        self.gameOver = False

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    x = position[0]//self.iconSize[0]
                    y = position[1]//self.iconSize[1]
                    clickType = event.button
                    if not self.gameOver:
                        self.handleClick(x, y, clickType)
            self.display()
            pygame.display.flip()
        pygame.quit()

    def display(self):
        for x in range((self.boardSize[0])):
            for y in range((self.boardSize[1])):
                icon = pygame.image.load(self.board[x][y].icon)
                icon = pygame.transform.scale(
                    icon, (self.iconSize[0], self.iconSize[1]))
                self.screen.blit(
                    icon, (x*self.iconSize[0], y*self.iconSize[1]))

    def handleClick(self, x, y, clickType):
        leftClick = 1
        rightClick = 3

        if clickType == rightClick:
            self.board[x][y].unflagORflagCell()
            self.boardClass.totalNumFlaggedCells += 1
        elif clickType == leftClick:
            if self.board[x][y].isClosed:
                if self.board[x][y].isFlagged:
                    self.board[x][y].unflagORflagCell()
                    self.boardClass.totalNumFlaggedCells -= 1
                else:
                    self.board[x][y].revealCell()
                    self.boardClass.openCellSet.add((x, y))
                    if self.board[x][y].numMines == 0:
                        for neigh in self.board[x][y].neighList:
                            neigh_x, neigh_y = neigh
                            if not neigh in self.boardClass.openCellSet:
                                self.handleClick(neigh_x, neigh_y, leftClick)
        self.checkGameState(x, y)

    def checkGameState(self, x, y):
        if self.board[x][y].lost:
            self.popUpWindow("lost")
            for x in range((self.boardSize[0])):
                for y in range((self.boardSize[1])):
                    if self.board[x][y].isClosed:
                        self.board[x][y].revealCell()
        else:
            if len(self.boardClass.openCellSet) == self.boardClass.numNonMineCells and \
                    self.boardClass.totalNumMines == self.boardClass.totalNumFlaggedCells:
                self.gameOver = True
                self.popUpWindow("won")

    def popUpWindow(self, state):
        print("You "+state)


# number of mines
# time
# msiley face

# optimize neighbor checking and fix total num of clicks
