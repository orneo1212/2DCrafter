from pygamefrontend import imageloader, mapviewer
import Engine2d as engine
import pygame
import time

"""Game """
class Game:
    def __init__(self, screen):
        self.screen=screen
        self.mapo=engine.map.Map()
        self.player=engine.player.Player("test", self.mapo)
        self.imageloader=imageloader.ImageLoader()
        self.mapviewer=mapviewer.MapViever()
        #light Surface
        self.lightsurface=pygame.Surface((640,480),pygame.SRCALPHA)
        #speeds
        self.movespeed=0.25
        self.mineticks=10 # number of ticks to mine
        self.minetick=0
        #times
        self.eventstime=time.time()
        self.eventdelay=0.025
        self.gametimer=pygame.time.Clock()
        #day night cycle
        self.daytime=0.0 # 0 day 255 night
        self.starttime=time.time()
        self.daytimestep=255/600 # day length in secs
        #
        self.currenttile=0

    def update(self):
        self.gametimer.tick()
        daydelta=time.time()-self.starttime
        if daydelta>1:
            self.daytime+=self.daytimestep
            self.starttime=time.time()
            if self.daytime>=255 or self.daytime<=0:
                self.daytimestep=-self.daytimestep
        self.daytime=max(0,self.daytime)
        self.daytime=min(self.daytime,255)

    def events(self):
        keys=pygame.key.get_pressed()
        event=pygame.event.poll()
        if event.type==pygame.QUIT:
            self.mapo.unloadsectors()
            exit()
        #events tick
        if time.time()>self.eventstime+self.eventdelay:
            self.eventstime=time.time()
            self.minetick+=1

            plpos=self.player.getposition()
            mx,my=pygame.mouse.get_pos()
            mtx,mty=self.mapviewer.getglobalfromscreen(plpos,(mx,my))

            #keys

            #time change
            if keys[pygame.K_F3]:
                self.daytime+=5
            if keys[pygame.K_F4]:
                self.daytime-=5
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
                print "Position:",mtx,mty
                print "FPS:",self.gametimer.get_fps()
                print "Inventory:"
                for slot in self.player.inventory.slots:
                    if slot:print "Item ID=%s Count=%s" % (slot[0],slot[1])
            #Mouse events
            mousekeys=pygame.mouse.get_pressed()
            #mine block
            if mousekeys[0]==1:
                if self.minetick%self.mineticks==0:
                    err=self.player.mineblock((mtx,mty))
            #get block under cursor
            if mousekeys[1]==1:
                block=self.mapo.getblock((mtx,mty))
                if block:self.currenttile=block.id
                else:self.currenttile=None
            #put block
            if mousekeys[2]==1:
                #avoid putblock on player position
                if (mtx,mty)!=self.player.getposition():
                    err=self.player.putblock((mtx,mty),self.currenttile)

    def redraw(self):
        self.lightsurface.fill((0,0,0,self.daytime))
        pygame.draw.circle(self.lightsurface,(255,255,255,0),(320+8,240),128,0)
        self.mapviewer.renderatplayer(self.screen, self.player, self.imageloader, self.mapo)
        self.screen.blit(self.lightsurface,(0,0))
        pygame.display.update()
