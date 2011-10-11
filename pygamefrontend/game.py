from pygamefrontend import imageloader, mapviewer,inventoryscreen
import Engine2d as engine
import pygame
import time
import math

"""Game """
class Game:
    def __init__(self, screen):
        self.screen=screen
        self.mapo=engine.map.Map()
        self.player=engine.player.Player("test", self.mapo)
        self.imageloader=imageloader.ImageLoader()
        self.mapviewer=mapviewer.MapViever()
        self.mapviewer.loadmapdata(self.mapo)
        #pages
        self.invscreen=inventoryscreen.InventoryScreen(self)
        #speeds
        self.movespeed=0.25
        self.mineticks=10 # number of ticks to mine
        #timers
        self.minetimer=engine.tools.Timer()
        self.eventtimer=engine.tools.Timer()
        self.gametimer=pygame.time.Clock()
        #Action Distance
        self.actiondistance=4

        self.starttime=0

        #Current selection
        self.currenttile=8

    def update(self):
        """Update"""
        daydelta=time.time()-self.starttime
        if daydelta>1:
            self.starttime=time.time()
            self.mapviewer.updatedattime()
        #Grow
        if self.minetimer.tickpassed(1000):
            secp=self.mapo.convertposition(self.player.getposition())
            sector=self.mapo.getsector(secp[0])
            engine.map.randomgrow(sector)
        #update pages
        self.invscreen.update()

    def events(self):
        keys=pygame.key.get_pressed()
        mousekeys=pygame.mouse.get_pressed()

        self.gametimer.tick()

        #get event from queue
        event=pygame.event.poll()

        if event.type==pygame.QUIT:self.onexit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_e:
                 #toggle inventory
                if self.invscreen.visible:
                    self.invscreen.visible=False
                else:self.invscreen.visible=True
        #events tick
        if not self.eventtimer.timepassed(0.025):return
        self.eventtimer.tick()
        self.minetimer.tick()

        #ALL LINES BELOW WILL BE CALLED ONE PER EVENT TICK

        #get mouse pos and calculate block position
        plpos=self.player.getposition()
        mx, my=pygame.mouse.get_pos()
        mtx, mty=self.mapviewer.getglobalfromscreen(plpos, (mx, my))

        #time change
        if keys[pygame.K_F3]:
            self.mapviewer.daytime+=5
        if keys[pygame.K_F4]:
            self.mapviewer.daytime-=5
        #directions
        if keys[pygame.K_d]:
            self.player.move("e", self.movespeed)
        if keys[pygame.K_a]:
            self.player.move("w", self.movespeed)
        if keys[pygame.K_w]:
            self.player.move("n", self.movespeed)
        if keys[pygame.K_s]:
            self.player.move("s", self.movespeed)
        if keys[pygame.K_SPACE]:
            print "FPS:", self.gametimer.get_fps()
        #mine block
        if mousekeys[0]==1:
            self.mineblock((mtx,mty))
        #get block under cursor
        if mousekeys[1]==1:
            block=self.mapo.getblock((mtx, mty))
            if block:self.currenttile=block.id
            else:self.currenttile=None
        #put block
        if mousekeys[2]==1:
            self.putblock((mtx,mty))
        #Send events to pages
        self.invscreen.events(event)

    def actioninrange(self,actionpos):
        plpos=self.player.getposition()
        if math.fabs(actionpos[0]-plpos[0])<=self.actiondistance and \
            math.fabs(actionpos[1]-plpos[1])<=self.actiondistance:
            return True
        else:return False

    def putblock(self,mousepos):
        #avoid putblock on player position
        if mousepos!=self.player.getposition():
            if self.minetimer.tickpassed(5):
                if self.actioninrange(mousepos):
                    err=self.player.putblock(mousepos, self.currenttile)

    def mineblock(self,mousepos):
        plpos=self.player.getposition()
        if self.actioninrange(mousepos):
            if self.minetimer.tickpassed(self.mineticks):
                err=self.player.mineblock(mousepos)

    def redraw(self):
        #clean the screen
        self.screen.fill((117,101,50))
        #render
        self.mapviewer.renderatplayer(self.screen, self.player, self.imageloader, self.mapo)
        #redraw pages
        self.invscreen.redraw(self.screen)
        pygame.display.update()

    def onexit(self):
        """On exit"""
        self.mapviewer.savemapdata(self.mapo)
        self.mapo.unloadsectors()
        self.player.unloadplayer()
        pygame.quit()
        exit()
