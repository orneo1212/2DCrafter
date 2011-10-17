import pygame
import pygamefrontend
from pygamefrontend import game

class MainMenu:
    def __init__(self,screen):
        self.screen=screen
        self.backimg=pygamefrontend.imgloader.loadimage("mainmenubackground")
        #new game button
        self.ngbtn=pygamefrontend.gui.Button("New Game",(400,250))
        self.qbtn=pygamefrontend.gui.Button("Quit",(400,300))
        self.ngbtn.connect(self.newgame)
        self.qbtn.connect(self.onexit)
        #page
        self.page=None

    def update(self):
        pass

    def events(self):
        event=pygame.event.poll()
        if event.type==pygame.QUIT:self.onexit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:self.onexit()
        self.ngbtn.events(event)
        self.qbtn.events(event)

    def redraw(self,surface):
        surface.blit(self.backimg, (0,0))
        self.ngbtn.draw(surface)
        self.qbtn.draw(surface)

    def onexit(self):
        exit(0)

    #
    def newgame(self):
        pygamefrontend.CURRPAGE=game.Game(self.screen)
        #clear pygame events
        pygame.event.clear()
