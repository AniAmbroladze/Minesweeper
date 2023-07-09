import pygame, os 
os.environ['SDL_VIDEO_CENTERED'] = '1'

from board import Board


class UI():
    def __init__(self):   
        self.setInitValues()

    def setInitValues(self):
        self.gameState = "init"
        self.screenSize = (592,592)
        self.boardSize = (16,16)
        self.iconSize = self.screenSize[0]//self.boardSize[0], self.screenSize[1]//self.boardSize[1]
    
    def createBoard(self,boardSize,totalNumMines):
        self.boardSize, self.totalNumMines = boardSize, totalNumMines
        self.boardClass = Board(self.boardSize, self.totalNumMines)
        self.board = self.boardClass.board
        #self.iconSize = self.screenSize[0]//self.boardSize[0], self.screenSize[1]//self.boardSize[1]
    
    def updateGrid(self):
        for x in range(self.boardSize[0]):
            for y in range(self.boardSize[1]):
                if self.gameState == "init":
                    icon = pygame.image.load("images/closed.png")
                else:
                    icon = pygame.image.load(self.board[x][y].icon)
                icon = pygame.transform.scale(icon,(self.iconSize[0], self.iconSize[1]))
                self.grid_surf.blit(icon, (x*self.iconSize[0], y*self.iconSize[1]))

    def drawGrid(self):
        self.grid_surf = pygame.Surface(self.screenSize)
        self.grid_surf = self.grid_surf.convert()
        self.grid_surf.fill((250, 250, 250))
        self.updateGrid()

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.screenSize)
        self.drawGrid()

        running = True
        while running:

            self.isLevelChosen = False
            self.startsNewGame = False

            mousePos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if self.gameState == "init":
                        self.isLevelChosen = True
                    if self.gameState == "over":
                        self.startsNewGame = True
                    if self.gameState == "on":
                        xCell = mousePos[0]//self.iconSize[0]
                        yCell = mousePos[1]//self.iconSize[1]
                        clickType = event.button
                        self.handleClick(xCell, yCell, clickType)
                        self.drawGrid()

            self.display(mousePos)
            pygame.display.update()
            clock.tick(60)
        pygame.quit()

    def displayButtons(self,buttons,mousePos):

        width = 3/5*self.screenSize[0]
        height = round(1/5*self.screenSize[1])
        startY = (self.screenSize[0] - width)/2
        startX = height
        clicked = False

        font = pygame.font.SysFont('Georgia', 30, bold=True)
        for buttonNum in range(len(buttons)):
            startXLevel = startX+(height*buttonNum)
            color = (54, 69, 79)
            if mousePos[0] >= startY and mousePos[0] <= startY+width and mousePos[1] >= startXLevel and mousePos[1] <= startXLevel+height:
                clicked = True
                clickedButton = buttonNum
                color =  (169,169,169)
            pygame.draw.rect(self.screen, (255, 255, 255),pygame.Rect(startY, startXLevel, width, height))
            pygame.draw.rect(self.screen, color,pygame.Rect(startY+5, startXLevel+5, width-10, height-10))
            text = font.render(buttons[buttonNum][0], True, 'white')
            text_rect = text.get_rect(center=(startY+(width/2), startXLevel+(height/2)))
            self.screen.blit(text, text_rect)
        
        if clicked:
            if self.isLevelChosen:
                self.gameState = "on"
                if self.screenSize != buttons[clickedButton][1]:
                    self.screenSize = buttons[clickedButton][1]
                    self.screen = pygame.display.set_mode(self.screenSize)
                self.createBoard(buttons[clickedButton][2],buttons[clickedButton][3])
                self.drawGrid()
            elif self.startsNewGame:
                self.setInitValues()
                self.screen = pygame.display.set_mode(self.screenSize)
                self.drawGrid()


    def display(self,mousePos):
        self.screen.blit(self.grid_surf, (0, 0))
        button = []
        if self.gameState == "init":
                button = [["EASY", (333, 333), [9,9], 10],
                         ["MEDIUM", (592, 592), [16,16], 40],
                         ["DIFFICULT", (1110,592), [30,16], 99]]
        elif self.gameState == "over":
                button = [["New Game"]]
        self.displayButtons(button,mousePos)
            
    def handleClick(self, x, y, clickType):
        leftClick = 1
        rightClick = 3

        if clickType == rightClick:
            if self.board[x][y].isFlagged:
                self.boardClass.totalNumFlaggedCells -= 1
            else:
                self.boardClass.totalNumFlaggedCells += 1
            self.board[x][y].unflagORflagCell()

        elif clickType == leftClick:
            if self.board[x][y].isClosed:
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
            self.gameState = "over"
            print("You lost :(")
            for x in range((self.boardSize[0])):
                for y in range((self.boardSize[1])):
                    if self.board[x][y].isClosed:
                        self.board[x][y].revealCell()
        else:
            if len(self.boardClass.openCellSet) == self.boardClass.numNonMineCells \
                and self.boardClass.totalNumMines == self.boardClass.totalNumFlaggedCells:
                self.gameState = "over"
                print("You won :)")


