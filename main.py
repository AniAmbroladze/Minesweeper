from UI import UI
from board import Board

board = Board([9, 9], 10)
game = UI(board, (600, 600))
game.run()
# difficulty levels
# easy: 9x9 / 10 mines
# normal: 16x16/ 40 mines
# hard: 16x30/ 99 mines
# customized? : max 30x24/ 200mines
# safe Startmode: YES/NO - click and do not put mines around the area
