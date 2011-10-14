import time
import math
import sys
import pygamefrontend
from pygamefrontend import imageloader, mapviewer,inventoryscreen
import Engine2d as engine
import pygame

SW,SH=pygamefrontend.SW,pygamefrontend.SH

"""Game """
class Game:
    def __init__(self):
        #init application
        self.screen=pygame.display.set_mode((SW, SH), pygame.DOUBLEBUF)
        pygame.display.set_caption("2DCrafter")
        #define variables
        self.mapo=engine.map.Map()
        self.mapo.loadmapdata()
        self.player=engine.player.Player("test", self.mapo)
        self.imageloader=imageloader.ImageLoader("data/images.yaml")
        self.mapviewer=mapviewer.MapViever()
        #Sounds
        self.minesound=pygame.mixer.Sound("data/sounds/pickaxe.ogg")
        #Font
        self.font=pygame.font.SysFont("Sans", 18)
        self.font1=pygame.font.SysFont("Sans", 14)
        #pages
        self.invscreen=inventoryscreen.InventoryScreen()
        self.invscreen.setinventory(self.player.inventory)
        self.chestinventory=None #chest content if selected
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
        if self.chestinventory:self.chestinventory.update()

        self.currenttile=self.invscreen.getselected()

    def events(self):
        keys=pygame.key.get_pressed()
        mousekeys=pygame.mouse.get_pressed()
        #get event from queue
        pygame.event.clear(pygame.MOUSEMOTION)
        event=pygame.event.poll()

        if event.type==pygame.QUIT:self.onexit()
        if event.type==pygame.KEYDOWN:
            self.needredraw=True
            if event.key==pygame.K_e:
                #toggle inventory
                if self.invscreen.visible:
                    self.invscreen.visible=False
                else:self.invscreen.visible=True
            #QUIT
            if event.key==pygame.K_ESCAPE:self.onexit()
            #Toggle fullscreen
            if event.key==pygame.K_F11:
                pygame.display.toggle_fullscreen()
            #Toggle light circle
            if event.key==pygame.K_F10:
                conf=pygamefrontend.imgloader.config
                light=conf["circlelight"]
                if light:conf["circlelight"]=False
                else: conf["circlelight"]=True
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
                txt="FPS: %s" % self.gametimer.get_fps()
                engine.ui.msgbuffer.addtext(txt)
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
            self.hidechest()
        if keys[pygame.K_a]:
            self.player.move("w", self.movespeed)
            self.hidechest()
        if keys[pygame.K_w]:
            self.player.move("n", self.movespeed)
            self.hidechest()
        if keys[pygame.K_s]:
            self.player.move("s", self.movespeed)
            self.hidechest()
        #mine block
        if mousekeys[0]==1 and not self.invscreen.isunder((mx,my)):
            self.mineblock((mtx,mty))
        #get block under cursor
        if mousekeys[1]==1 and not self.invscreen.isunder((mx,my)):
            block=self.mapo.getblock((mtx, mty))
            if block:self.currenttile=block.id
            else:self.currenttile=None
            self.invscreen.setselected(self.currenttile)
        #put block
        if mousekeys[2]==1 and not self.invscreen.isunder((mx,my)):
            self.putblock((mtx,mty))
            self.setupaction() # setupaction if any
        #Send events to pages
        self.invscreen.events(event)
        if self.chestinventory:self.chestinventory.events(event)

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

    def setupaction(self):
        actiondata=self.player.actiondata # get action block
        if not actiondata:return
        if actiondata.id==18: # Chest
            self.chestinventory=inventoryscreen.InventoryScreen("chestframe")
            inventory=engine.player.Inventory()
            inventory.slots=actiondata.itemdata["data"]
            self.chestinventory.setinventory(inventory)
            self.chestinventory.visible=True
            self.mapo.itemloader.setchanged(actiondata.uid)
            #
            self.player.actiondata=None

    def hidechest(self):
        """hide chest view with inventory"""
        if self.chestinventory:
            self.chestinventory.visible=False
            self.invscreen.visible=False

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
        if not self.eventtimer.tickpassed(2):return
        #clean the screen
        self.screen.fill((117,101,50))
        #render
        self.mapviewer.renderatplayer(self.screen, self.player, self.mapo)
        #Draw on screen text
        self.drawosd(self.screen)
        #redraw pages
        if self.chestinventory:self.chestinventory.redraw(self.screen)
        self.invscreen.redraw(self.screen)
        #redraw screen
        pygame.display.update()

    def drawosd(self,screen):
        #draw position
        pos=self.player.getposition()
        text=self.font.render("Position: %s" % str(pos), 1, (255,255,255))
        screen.blit(text,(0,0))
        #draw current day state
        daystate=engine.environment.DAYTIME.daystate
        text=self.font.render(str(daystate),1, (255,255,255))
        screen.blit(text,(0,1*18))
        #draw selected block  name
        block=engine.map.Block(self.currenttile)
        if block:name=block.name
        else:name=""
        text=self.font.render("Selected: %s" % name, 1, (255,255,255))
        screen.blit(text,(0,3*18))
        #draw current recipe
        text=self.font.render("Recipe: %s" % str(self.currentrecipe),\
            1, (255,255,255))
        screen.blit(text,(0,4*18))
        #Draw messages
        msgs=engine.ui.msgbuffer.getlast(5)
        msgs.reverse()
        counter=0
        for msg in msgs:
            counter+=1
            text=self.font1.render(str(msg),1, (255,255,255))
            screen.blit(text,(20,SH-counter*10-20))

    def onexit(self):
        """On exit"""
        engine.ui.msgbuffer.addtext("Saveing data please wait...")
        self.redraw()
        self.mapo.savemapdata()
        self.mapo.unloadsectors()
        self.player.unloadplayer()
        self.mapo.itemloader.unloaditems()
        sys.exit()

    def mainloop(self):
        while 1:
            self.gametimer.tick(self.imageloader.config["maxfps"])
            self.events()
            self.update()
            self.redraw()
