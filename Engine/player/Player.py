import os
import json
import random
import Engine

class Player:
    def __init__(self, name, currmap):
        self.name=name
        self.position=[0.0, 0.0]
        self.respawnpos=[0, 0]
        #map
        self.currmap=currmap
        self.mapindex=0 # 0-outdoor 1+ undergrounds

        self.inventory=Engine.player.Inventory()
        self.actiondata=None # action data like chest data
        self.tryloadplayer()

    def find_spawn_position(self):
        """Find new non blocked spawn position"""
        tries=2000
        print "Finding respawn..."
        while tries>0:
            nx=random.randint(-500, 500)
            ny=random.randint(-500, 500)
            block=self.currmap.getblock((nx, ny))
            if block:
                if not block.blocked and block.obstacle:
                    self.position=[nx, ny]
                    self.respawnpos=[nx, ny]
                    return
            #try next random position
            tries-=1

    def movedown(self, fromposition):
        """Move to bottom layer"""
        self.position=list(fromposition)
        self.mapindex+=1
        index=self.currmap.index
        index+=1
        self.currmap=Engine.map.mapstack.getmapbyindex(index)
        Engine.ui.msgbuffer.addtext("Go below floor")

    def moveup(self, fromposition):
        """Move to upper layer"""
        self.mapindex-=1
        self.position=list(fromposition)
        index=self.currmap.index
        index-=1
        if index<0:index=0
        self.currmap=Engine.map.mapstack.getmapbyindex(index)
        Engine.ui.msgbuffer.addtext("Go above floor")

    def movetomap(self, mapindex):
        self.mapindex=mapindex
        self.currmap=Engine.map.mapstack.getmapbyindex(mapindex)

    def tryloadplayer(self):
        """Try load player"""
        playerspath=os.path.join(Engine.mainpath, "players")
        playerfile=os.path.join(playerspath, "%s.txt" % self.name)
        try:
            playerdata=open(playerfile, "r")
            if not playerdata:return
        except:
            #find new player spawn point
            self.find_spawn_position()
            return

        playerdata=json.load(playerdata) # load json player data

        #parse data fropm file
        if playerdata.has_key("player"):
            self.position=playerdata["player"]["position"]
        if playerdata.has_key("inventory"):
            self.inventory.slots=playerdata["inventory"]
        if playerdata.has_key("mapindex"):
            self.movetomap(playerdata["mapindex"])

    def unloadplayer(self):
        """unload player data"""
        #create players directory if not exist
        playerspath=os.path.join(Engine.mainpath, "players")
        if not os.path.isdir(playerspath):
            os.mkdir(playerspath)
        playerfile=os.path.join(playerspath, "%s.txt" % self.name)
        playerfile=open(playerfile, "w")
        data={}
        data["player"]={}
        data["player"]["position"]=self.position
        data["inventory"]=self.inventory.slots
        data["mapindex"]=self.currmap.index
        json.dump(data, playerfile) # dump data to json player file
        playerfile.close()
        return 0 # done

    def setmap(self, mapobject):
        self.currmap=mapobject

    def move(self, direction, speed, collisions=True):
        """Move player to a given direction"""
        #north east west south
        mv={"n":(0, speed),
            "s":(0, -speed),
            "e":(-speed, 0),
            "w":(speed, 0)}
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

    def addpickupmsg(self, itemid):
        """Add pickup message"""
        block=Engine.map.Block(itemid)
        txt="You got %s" % block.name
        Engine.ui.msgbuffer.addtext(txt)

    def verify_and_mine(self, blockposition, layer):
        """Verify and mine block from first possible layer"""
        if not self.currmap:return 1 #Err: Map not assigned
        block=self.currmap.getblock(blockposition, layer)
        if block:
            if not block.obstacle:return 3 # Block is not an obstacle
            #add self item or items definied in mineitems
            if block.id==18:
                #if chest have itemdata
                if block.itemdata:
                    #dont mine non empty chests
                    if not block.itemdata["data"].count(None)==32:
                        Engine.ui.msgbuffer.addtext("You can't mine non empty"\
                                                    " chests")
                        return 4 #Cannot remoeve non empty chest
            err=0
            #add mined block to inventory
            if not block.mineitems:
                err=self.inventory.additem(block.id)
                if not err:self.addpickupmsg(block.id)
            else:
                #simulate add item
                for itemid in block.mineitems:
                    if itemid==None:continue # skip None
                    err=self.inventory.additem(itemid, True)
                    if err:break

            #check error
            if err:print "Additem error code:", err
            #remove block only when added to invetory
            else:
                #call on mine callback
                if block.onminecall:
                    block.onminecall(self, block, blockposition)
                #add item to inventory
                for itemid in block.mineitems:
                    if itemid==None:continue # skip None
                    self.addpickupmsg(itemid)
                    err=self.inventory.additem(itemid, False)
                #remove item from map (taken)
                self.currmap.setblock(blockposition, None, layer)
            return 0 # Done
        else:return 2 # Err: Can't mine air (or empty block)

    def mineblock(self, blockposition):
        """Mine Block and put into inventory"""
        #mine only one block
        for layer in [1, 0]: # reverse order to mine first block from top layer
            err=self.verify_and_mine(blockposition, layer)
            if not err:return 0 # Done
        return 1 # cant mine nothing

    def verify_and_put(self, block, blockposition, blockID, layer):
        """Verify and put block on the map"""

        #If block exist
        if block:
            #make block action
            if block.onput: #action (replace blocks)
                self.currmap.setblock(blockposition, None)
                self.currmap.setblock(blockposition, \
                    Engine.map.Block(block.onput))
            #call onputcall(player, blockposition)
            if block.onputcall:
                err=block.onputcall(self, blockposition, layer)
                if err:return 1 #can't place block
            if block.obstacle:return 2 # Block exist

        #put block on the empty field
        if self.inventory.haveitem(blockID):
            #create block to put on the emopty place
            newblock=Engine.map.Block(blockID)

            #call onputemptycall(player, block, blockposition)
            if newblock.onputemptycall:
                err=newblock.onputemptycall(self, block, blockposition)
                if err:return 1 #can't place block

            err=self.inventory.removeitem(blockID)
            #set block at position
            self.currmap.setblock(blockposition, newblock, layer)
            return 0 # Done

    def putblock(self, blockposition, blockID):
        """Put block on the map."""
        if not self.currmap:return 1 #Err: Map not assigned
        #put only one block
        for layer in [0, 1]:
            #get current block on the ground
            block=self.currmap.getblock(blockposition, layer)
            newblock=Engine.map.Block(blockID) # temp item
            #dont put item block on layer 0 and not item blocks on layer 1
            if layer==0 and newblock and newblock.item:continue
            if layer==1 and newblock and not newblock.item:continue
            err=self.verify_and_put(block, blockposition, blockID, layer)
            if not err:return 0 # item placed
        return 1 # cant place item

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
