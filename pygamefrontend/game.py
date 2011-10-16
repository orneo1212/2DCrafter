import time
import math
import sys
import pygamefrontend
from pygamefrontend import imageloader, mapviewer, inventoryscreen
from pygamefrontend import actionbar
import Engine2d as engine
import pygame

SW, SH=pygamefrontend.SW, pygamefrontend.SH

"""Game """
class Game:
    def __init__(self, screen):
        self.screen=screen
        #define variables
        self.mapo=engine.map.mapstack.getmapbyindex(0)
        self.player=engine.player.Player("test", self.mapo)
        self.imageloader=imageloader.ImageLoader("data/images.yaml")
        self.mapviewer=mapviewer.MapViever()
        #Sounds
        self.minesound=pygame.mixer.Sound("data/sounds/pickaxe.ogg")
        #Font
        self.font=pygame.font.SysFont("Sans", 16)
        self.font1=pygame.font.SysFont("Sans", 12)
        #pages
        self.invscreen=inventoryscreen.InventoryScreen()
        self.invscreen.setinventory(self.player.inventory)
        self.chestinventory=None #chest content if selected
        self.actionbar=actionbar.Actionbar(self.player.inventory)
        #speeds
        self.movespeed=0.25
        self.mineticks=10 # number of ticks to mine
        #timers
        self.minetimer=engine.tools.Timer()
        self.eventtimer=engine.tools.Timer()
        #Action Distance
        self.actiondistance=4

        self.starttime=0

        #Current selection
        self.currenttile=0
        self.currentrecipe=""
        self.currentrecipeID=0

    def update(self):
        """Update game"""
        daydelta=time.time()-self.starttime
        if daydelta>1:
            self.starttime=time.time()
            engine.environment.DAYTIME.updatedaytime()
        #Grow
        if self.minetimer.tickpassed(1000):
            secp=self.mapo.convertposition(self.player.getposition())
            sector=self.mapo.getsector(secp[0])
            engine.map.randomgrow(sector)
        #move msg texts up
        if self.minetimer.tickpassed(50):
            engine.ui.msgbuffer.addtext("")
        #update pages
        self.invscreen.update()
        if self.chestinventory:self.chestinventory.update()
        self.actionbar.update()
        #set current tile
        self.currenttile=self.actionbar.getselected()

    def isunderpages(self):
        """return false if mouse is not under pages"""
        mx, my=pygame.mouse.get_pos()
        if self.chestinventory:
            return self.chestinventory.isunder((mx, my))
        return self.invscreen.isunder((mx, my))

    def handlekeydown(self, event):
        """handle all keydown events"""
        if event.key==pygame.K_e:
            #toggle inventory
            if self.invscreen.visible:
                self.invscreen.visible=False
            else:self.invscreen.visible=True
        #QUIT
        if event.key==pygame.K_ESCAPE:self.onexit()
        #Actionbar selection
        if event.key==pygame.K_1:self.actionbar.selected=0
        if event.key==pygame.K_2:self.actionbar.selected=1
        if event.key==pygame.K_3:self.actionbar.selected=2
        if event.key==pygame.K_4:self.actionbar.selected=3
        if event.key==pygame.K_5:self.actionbar.selected=4
        if event.key==pygame.K_6:self.actionbar.selected=5
        if event.key==pygame.K_7:self.actionbar.selected=6
        if event.key==pygame.K_8:self.actionbar.selected=7
        #Toggle fullscreen
        if event.key==pygame.K_F11:
            pygame.display.toggle_fullscreen()
        #Toggle light circle
        if event.key==pygame.K_F10:
            conf=engine.Config
            light=conf["circlelight"]
            if light:conf["circlelight"]=False
            else: conf["circlelight"]=True
        #Next Recipe
        if event.key==pygame.K_PAGEDOWN:self.nextrecipe()
        if event.key==pygame.K_PAGEUP:self.nextrecipe(True)
        #Craft
        if event.key==pygame.K_RETURN:
            engine.crafting.craft(self.player, self.currentrecipe)
            self.nextrecipe(update=True)
        #Sort inventory
        if event.key==pygame.K_BACKSPACE:
            self.player.sortinventory()
        #time change
        if event.key==pygame.K_F3:
            engine.environment.DAYTIME.daytime-=5
        if event.key==pygame.K_F4:
            engine.environment.DAYTIME.daytime+=5

    def events(self):
        """handle events"""
        keys=pygame.key.get_pressed()
        mousekeys=pygame.mouse.get_pressed()
        #get event from queue
        pygame.event.clear(pygame.MOUSEMOTION)
        event=pygame.event.poll()

        if event.type==pygame.QUIT:self.onexit()
        if event.type==pygame.KEYDOWN:self.handlekeydown(event)
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.actionbar.selected is  not None:
                if event.button==4:self.actionbar.selected-=1
                if event.button==5:self.actionbar.selected+=1

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
        if mousekeys[0]==1 and not self.isunderpages():
            self.mineblock((mtx, mty))
        #put block
        if mousekeys[2]==1 and not self.invscreen.isunder((mx, my)):
            self.putblock((mtx, mty))
            self.setupaction() # setupaction if any
        #Send events to pages
        self.invscreen.events(event)
        if self.chestinventory:
            self.chestinventory.events(event)
        self.actionbar.events(event)

    def actioninrange(self, actionpos, distance=0):
        """Check if the action is in range.
        If distance=0 then will be used self.actiondistance"""
        plpos=self.player.getposition()
        if not distance:distance=self.actiondistance
        if math.fabs(actionpos[0]-plpos[0])<=distance and \
            math.fabs(actionpos[1]-plpos[1])<=distance:
            return True
        else:return False

    def putblock(self, mousepos):
        """Put block on the ground"""
        if self.minetimer.tickpassed(5):
            if self.actioninrange(mousepos):
                err=self.player.putblock(mousepos, self.currenttile)

    def mineblock(self, mousepos):
        """Collect block"""
        plpos=self.player.getposition()
        if self.actioninrange(mousepos, 2):
            if not self.minetimer.tickpassed(self.mineticks):return
            self.hidechest()
            err=self.player.mineblock(mousepos)
            if not err:self.playsound(self.minesound)

    def setupaction(self):
        """Setup action. like open chests"""
        actiondata=self.player.actiondata # get action block
        if not actiondata:return
        if actiondata.id==18: # Chest
            #create inventoryscreen object for chest content
            self.chestinventory=inventoryscreen.InventoryScreen("chestframe")
            self.chestinventory.invsoffset=(10, -180)
            #create inventory object to store items
            inventory=engine.player.Inventory()
            if actiondata.itemdata:
                inventory.slots=actiondata.itemdata["data"]
            #set inventory to show in inventoryscreen
            self.chestinventory.setinventory(inventory)
            self.chestinventory.visible=True
            # set player actiondata to None. avoid run this code again
            self.player.actiondata=None
            #setup trade (player>chest and chest>player)
            self.invscreen.tradeinventory=inventory
            self.chestinventory.tradeinventory=self.player.inventory

    def hidechest(self):
        """hide chest view with inventory"""
        self.invscreen.tradeinventory=None
        if self.chestinventory:
            self.chestinventory.visible=False
            #self.invscreen.visible=False
            self.chestinventory.tradeinventory=None

    def playsound(self, sound):
        """Play sound"""
        if not pygame.mixer.get_busy():
            if sound:sound.play()

    def nextrecipe(self, reverse=False, update=False):
        """Toggle recipe"""
        if not update:
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

    def redraw(self,screen):
        if not self.eventtimer.tickpassed(2):return
        #clean the screen
        screen.fill((117, 101, 50))
        #render
        self.mapviewer.renderatplayer(screen, self.player,\
            self.player.currmap)
        #Draw on screen text
        self.drawosd(screen)
        #redraw pages
        if self.chestinventory:self.chestinventory.redraw(screen)
        self.invscreen.redraw(screen)
        self.actionbar.redraw(screen)

    def drawosd(self, screen):
        """Draw on screen texts"""
        #draw position
        pos=self.player.getposition()
        text=self.font.render("Position: %s" % str(pos), 1, (255, 255, 255))
        screen.blit(text, (0, 0))
        #draw current day state
        daystate=engine.environment.DAYTIME.daystate
        text=self.font.render(str(daystate), 1, (255, 255, 255))
        screen.blit(text, (0, 1*18))
        #draw selected block  name
        block=engine.map.Block(self.currenttile)
        if block:name=block.name
        else:name=""
        text=self.font.render("Selected: %s" % name, 1, (255, 255, 255))
        screen.blit(text, (0, 3*18))
        #draw current recipe
        text=self.font.render("Recipe: %s" % str(self.currentrecipe), \
            1, (255, 255, 255))
        screen.blit(text, (0, 4*18))
        #Draw messages
        msgs=engine.ui.msgbuffer.getlast(10)
        msgs.reverse()
        counter=0
        for msg in msgs:
            counter+=1
            text=self.font1.render(str(msg), 1, (255, 255, 255))
            screen.blit(text, (20, SH-counter*10-40))

    def onexit(self):
        """On exit"""
        engine.ui.msgbuffer.addtext("Saveing data please wait...")
        self.redraw(self.screen)
        engine.map.mapstack.unloadall()
        self.player.unloadplayer()
        sys.exit()
