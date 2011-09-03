from pygamefrontend import imageloader, mapviewer
import Engine2d as engine
import pygame
import sys

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

    def redraw(self):
        self.mapviewer.render(self.screen, (0, -5), self.imageloader, self.mapo)
        pygame.display.update()

    def mainloop(self):
        while 1:
            self.events()
            self.redraw()

test=PygameTest()
test.mainloop()