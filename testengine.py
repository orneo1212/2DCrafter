from pygamefrontend import imageloader, mapviewer
import Engine2d as engine
import pygame
import sys

pygame.init()
pygame.key.set_repeat(50,50)

#    y
#    ^
#    |
#    |
# -------> x
#
#Z is a layer

class PygameTest:
    def __init__(self):
        self.screen=pygame.display.set_mode((640, 480))
        self.mapo=engine.map.Map()
        self.player=engine.player.Player("test")
        self.imageloader=imageloader.ImageLoader()
        self.mapviewer=mapviewer.MapViever()

    def events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_d:
                    self.player.move("e",3.3)
                if event.key==pygame.K_a:
                    self.player.move("w",3.3)
                if event.key==pygame.K_w:
                    self.player.move("n",3.3)
                if event.key==pygame.K_s:
                    self.player.move("s",3.3)
                if event.key==pygame.K_r:
                    self.player.move("u",3.3)
                if event.key==pygame.K_f:
                    self.player.move("d",15)

    def redraw(self):
        self.mapviewer.render(self.screen, self.player.getposition(), self.imageloader, self.mapo)
        pygame.display.update()

    def mainloop(self):
        while 1:
            self.events()
            self.redraw()

test=PygameTest()
test.mainloop()