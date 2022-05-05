class Cell():
    def __init__(self):
        self.hasMine = False
        self.isFlagged = False
        self.isClosed = True
        self.icon = "images/closed.png"
        self.numMines = 0
        self.neighList = []
        self.lost = False

    def revealCell(self):
        if self.isFlagged:
            if self.hasMine:
                self.icon = "images/mine.png"
            else:
                self.icon = "images/wrong_flag.png"
        else:
            if self.hasMine:
                self.icon = "images/red_mine.png"
                self.lost = True
            else:
                self.icon = "images/"+str(self.numMines)+".png"
        self.isClosed = False

    def unflagORflagCell(self):
        if self.isFlagged:
            self.icon = "images/closed.png"
            self.isFlagged = False
        else:
            self.icon = "images/flag.png"
            self.isFlagged = True
        
