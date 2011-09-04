from pygamefrontend import imageloader, mapviewer
import Engine2d as engine
import pygame

"""Game page"""
class Game:
    def __init__(self, screen):
        self.screen=screen
        self.mapo=engine.map.Map()
        self.player=engine.player.Player("test", self.mapo)
        self.imageloader=imageloader.ImageLoader()
        self.mapviewer=mapviewer.MapViever()

    def events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_d:
                    self.player.move("e", 3.3)
                if event.key==pygame.K_a:
                    self.player.move("w", 3.3)
                if event.key==pygame.K_w:
                    self.player.move("n", 3.3)
                if event.key==pygame.K_s:
                    self.player.move("s", 3.3)

    def redraw(self):
        self.mapviewer.renderatplayer(self.screen, self.player, self.imageloader, self.mapo)
        pygame.display.update()