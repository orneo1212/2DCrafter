import time
import math
import sys
from pygamefrontend import imageloader, mapviewer,inventoryscreen
import Engine2d as engine
import pygame

"""Game """
class Game:
    def __init__(self, screen):
        self.screen=screen
        self.mapo=engine.map.Map()
        self.player=engine.player.Player("test", self.mapo)
        self.imageloader=imageloader.ImageLoader()
        self.mapviewer=mapviewer.MapViever()
        self.mapviewer.loadmapdata(self.mapo)
        #Sounds
        self.minesound=pygame.mixer.Sound("data/sounds/pickaxe.ogg")
        #Font
        self.font=pygame.font.SysFont("Sans", 18)
        #pages
        self.invscreen=inventoryscreen.InventoryScreen()
        self.invscreen.setinventory(self.player.inventory)
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
        self.currenttile=0
        self.currentrecipe=""
        self.currentrecipeID=0

    def update(self):
        """Update"""
        daydelta=time.time()-self.starttime
        if daydelta>1:
            self.starttime=time.time()
            engine.environment.DAYTIME.updatedaytime()
        #Grow
        if self.minetimer.tickpassed(1000):
            secp=self.mapo.convertposition(self.player.getposition())
            sector=self.mapo.getsector(secp[0])
            engine.map.randomgrow(sector)
        #update pages
        self.invscreen.update()

        self.currenttile=self.invscreen.getselected()

    def events(self):
        keys=pygame.key.get_pressed()
        mousekeys=pygame.mouse.get_pressed()

        self.gametimer.tick()

        #get event from queue
        pygame.event.clear(pygame.MOUSEMOTION)
        event=pygame.event.poll()

        if event.type==pygame.QUIT:self.onexit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_e:
                 #toggle inventory
                if self.invscreen.visible:
                    self.invscreen.visible=False
                else:self.invscreen.visible=True
            #Next Recipe
            if event.key==pygame.K_PAGEDOWN:self.nextrecipe()
            if event.key==pygame.K_PAGEUP:self.nextrecipe(True)
            #Craft
            if event.key==pygame.K_RETURN:
                engine.crafting.craft(self.player,self.currentrecipe)
            #Sort inventory
            if event.key==pygame.K_BACKSPACE:
                self.player.sortinventory()
            #time change
            if event.key==pygame.K_F3:
                engine.environment.DAYTIME.daytime-=5
            if event.key==pygame.K_F4:
                engine.environment.DAYTIME.daytime+=5
            #Show FPS
            if event.key==pygame.K_SPACE:
                print "FPS:", self.gametimer.get_fps()

        #events tick
        if not self.eventtimer.timepassed(0.025):return
        self.eventtimer.tick()
        self.minetimer.tick()

        #ALL LINES BELOW WILL BE CALLED ONE PER EVENT TICK

        #get mouse pos and calculate block position
        plpos=self.player.getposition()
        mx, my=pygame.mouse.get_pos()
        mtx, mty=self.mapviewer.getglobalfromscreen(plpos, (mx, my))

        #directions
        if keys[pygame.K_d]:
            self.player.move("e", self.movespeed)
        if keys[pygame.K_a]:
            self.player.move("w", self.movespeed)
        if keys[pygame.K_w]:
            self.player.move("n", self.movespeed)
        if keys[pygame.K_s]:
            self.player.move("s", self.movespeed)
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
                if not err:self.playsound(self.minesound)


    def playsound(self,sound):
        """Play sound"""
        if not pygame.mixer.get_busy():
            if sound:sound.play()

    def nextrecipe(self,reverse=False):
        """Toggle recipe"""
        if reverse:self.currentrecipeID-=1
        else:self.currentrecipeID+=1

        items=self.player.inventory.getitems()
        recipelist=engine.crafting.getpossiblerecipes(items)
        if self.currentrecipeID>len(recipelist)-1:
            self.currentrecipeID=0
        if self.currentrecipeID<0:self.currentrecipeID=len(recipelist)-1
        #
        if len(recipelist)==0:
            self.currentrecipe=""
            return
        self.currentrecipe=recipelist[self.currentrecipeID]

    def redraw(self):
        #clean the screen
        self.screen.fill((117,101,50))
        #render
        self.mapviewer.renderatplayer(self.screen, self.player, self.imageloader, self.mapo)
        #Draw on screen text
        self.drawosd(self.screen)
        #redraw pages
        self.invscreen.redraw(self.screen)
        pygame.display.update()

    def drawosd(self,screen):
        #draw position
        pos=self.player.getposition()
        text=self.font.render("Position: %s" % str(pos), 1, (255,255,255))
        screen.blit(text,(0,0))
        #draw selected block  name
        block=engine.map.Block(self.currenttile)
        if block:name=block.name
        else:name=""
        text=self.font.render("Selected: %s" % name, 1, (255,255,255))
        screen.blit(text,(0,18))
        #draw current recipe
        text=self.font.render("Recipe: %s" % str(self.currentrecipe),\
            1, (255,255,255))
        screen.blit(text,(0,2*18))

    def onexit(self):
        """On exit"""
        self.mapviewer.savemapdata(self.mapo)
        self.mapo.unloadsectors()
        self.player.unloadplayer()
        sys.exit()
