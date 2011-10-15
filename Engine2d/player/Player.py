import os
import random
import yaml
import Engine2d as engine

class Player:
    def __init__(self, name, currmap):
        self.name=name
        self.position=[0.0, 0.0]
        self.respawnpos=[0,0]
        self.currmap=currmap
        self.inventory=engine.player.Inventory()
        self.actiondata=None # action data like chest data
        self.tryloadplayer()

    def find_spawn_position(self):
        """Find new non blocked spawn position"""
        tries=2000
        print "Finding respawn..."
        while tries>0:
            nx=random.randint(-500,500)
            ny=random.randint(-500,500)
            block=self.currmap.getblock((nx,ny))
            if block:
                if not block.blocked and block.obstacle:
                    self.position=[nx,ny]
                    self.respawnpos=[nx,ny]
                    return
            #try next random position
            tries-=1


    def tryloadplayer(self):
        """Try load player"""
        playerspath=os.path.join(engine.mainpath,"players")
        playerfile=os.path.join(playerspath,"%s.yaml" % self.name)
        try:
            playerdata=open(playerfile,"r")
            playerdata=yaml.load(playerdata)
            if not playerdata:return
        except:
            #find new player spawn point
            self.find_spawn_position()
            return

        #parse data fropm file
        if playerdata.has_key("player"):
            self.position=playerdata["player"]["position"]
        if playerdata.has_key("inventory"):
            self.inventory.slots=playerdata["inventory"]

    def unloadplayer(self):
        """unload player data"""
        #create players directory if not exist
        playerspath=os.path.join(engine.mainpath,"players")
        if not os.path.isdir(playerspath):
            os.mkdir(playerspath)
        playerfile=os.path.join(playerspath,"%s.yaml" % self.name)
        playerfile=open(playerfile,"w")
        data={}
        data["player"]={}
        data["player"]["position"]=self.position
        data["inventory"]=self.inventory.slots
        yaml.dump(data,playerfile)
        return 0 # done

    def setmap(self, mapobject):
        self.currmap=mapobject

    def move(self, direction, speed,collisions=True):
        """Move player to a given direction"""
        #north east west south up down
        mv={"n":(0, speed), "s":(0, -speed), "e":(-speed, 0), "w":(speed, 0)}
        if direction not in mv.keys():return

        #can't go through a blocked block
        if self.currmap:
            xx=int(self.position[0]+mv[direction][0])
            yy=int(self.position[1]+mv[direction][1])
            if collisions and self.currmap.isblocked((xx, yy)):
                #self.position=[int(self.position[0]),int(self.position[1])]
                return
        #update position
        self.position[0]+=mv[direction][0]
        self.position[1]+=mv[direction][1]

    def addpickupmsg(self,itemid):
        """Add pickup message"""
        block=engine.map.Block(itemid)
        txt="You got %s" % block.name
        engine.ui.msgbuffer.addtext(txt)

    def mineblock(self,blockposition):
        """Mine Block and put into inventory"""
        if not self.currmap:return 1 #Err: Map not assigned
        block=self.currmap.getblock(blockposition)
        if block:
            if not block.obstacle:return 3 # Block is not an obstacle
            #add self item or items definied in mineitems
            if block.id==18:
                #if chest have itemdata
                if block.itemdata:
                    #dont mine non empty chests
                    if not block.itemdata["data"].count(None)==32:
                        engine.ui.msgbuffer.addtext("You can't mine non empty"\
                                                    " chests")
                        return 4 #Cannot remoeve non empty chest
            #add mined block to inventory
            if not block.mineitems:
                err=self.inventory.additem(block.id)
                if not err:self.addpickupmsg(block.id)
            else:
                #simulate add item
                for itemid in block.mineitems:
                    err=self.inventory.additem(itemid,True)
                    if err:break

            #check error
            if err:print "Additem error code:",err
            #remove block only when added to invetory
            else:
                for itemid in block.mineitems:
                    self.addpickupmsg(itemid)
                    err=self.inventory.additem(itemid,False)
                self.currmap.setblock(blockposition,None)
            return 0 # Done
        else:return 2 # Err: Can't mine air (or empty block)

    def putblock(self,blockposition,blockID):
        """Put block on the map."""
        if not self.currmap:return 1 #Err: Map not assigned
        block=self.currmap.getblock(blockposition)
        if block:

            #call onputcall(player,position)
            if block.onputcall:
                block.onputcall(self,blockposition)
            #make block action
            if block.onput: #action
                self.currmap.setblock(blockposition,None)
                self.currmap.setblock(blockposition,engine.map.Block(block.onput))
            if block.obstacle:return 2 # Block exist

        #put block on the empty field
        if self.inventory.haveitem(blockID):
            err=self.inventory.removeitem(blockID)
            if err:print "Removeitem error code:",err
            newblock=engine.map.Block(blockID)
            #TODO:check for unique. Generate uid
            #set block at position
            self.currmap.setblock(blockposition,newblock)
            return 0 # Done

    def getposition(self):
        """Return position of ther player integer"""
        return (int(self.position[0]), int(self.position[1]))

    def sortinventory(self):
        """Sort inventory"""
        items=self.inventory.getitems()
        items.sort()
        self.inventory.clear()
        for item in items:
            self.inventory.additem(item)
