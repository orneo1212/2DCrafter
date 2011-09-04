from pygamefrontend import game
import Engine2d as engine
import pygame
import sys

pygame.init()
pygame.key.set_repeat(50, 50)

#    y
#    ^
#    |
#    |
# -------> x

class PygameTest:
    def __init__(self):
        self.screen=pygame.display.set_mode((640, 480), pygame.RESIZABLE)
        #game object
        self.game=game.Game(self.screen)
        #page of view
        self.page=self.game

    def mainloop(self):
        while 1:
            self.page.events()
            self.page.redraw()

test=PygameTest()
test.mainloop()