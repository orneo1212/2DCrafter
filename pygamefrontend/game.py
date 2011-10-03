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
        #init state of player
        self.falling=True
        self.jumping=False
        self.jumpstep=0
        self.jumpspeed=0.25
        self.fallspeed=0.5

    def update(self):
        self.fall()

    def events(self):
        keys=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:exit()
        #check keys
        #TODO:keys tick
        if keys[pygame.K_d]:
            self.player.move("e", 1.0)
        if keys[pygame.K_a]:
            self.player.move("w", 1.0)
        if keys[pygame.K_w]:
            self.jump()
        if keys[pygame.K_s]:
            self.player.move("s", 1.0)
        if keys[pygame.K_SPACE]:
            print self.jumpstep


    def redraw(self):
        self.mapviewer.renderatplayer(self.screen, self.player, self.imageloader, self.mapo)
        pygame.display.update()

    #FUCTIONS
    def jump(self):
        px,py=self.player.getposition()
        if self.mapo.isblocked((px,py+1)):
            self.jumpstep=0
            self.jumping=False
            return
        if self.jumpstep<=5/self.jumpspeed:
            self.jumpstep+=self.jumpspeed
            self.player.move("n", self.jumpspeed)

    def fall(self):
        px,py=self.player.getposition()
        #TODO: check for AIR not for blocked (fix for ladders)
        #fall
        if not self.mapo.isblocked((px,py-1)):
            if self.falling:
                self.player.move("s", self.jumpspeed)
            else:self.falling=True
        else: #hit the blocked
            self.falling=False
            self.jumpstep=0
