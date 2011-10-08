import Engine2d as engine
import yaml

class Player:
    def __init__(self, name, currmap=None):
        self.name=name
        self.position=[0, 0]
        self.currmap=currmap
        self.inventory=engine.player.Inventory()
        self.tryloadplayer()

    def tryloadplayer(self):
        """Try load player"""
        playerfile="players/%s.yaml" % self.name
        try:playerdata=open(playerfile,"r")
        except IOError:return
        #file exist load player data
        playerdata=yaml.load(playerdata)
        if not playerdata:return
        #parse data fropm file
        if playerdata.has_key("player"):
            self.position=playerdata["player"]["position"]
        if playerdata.has_key("inventory"):
            self.inventory.slots=playerdata["inventory"]

    def unloadplayer(self):
        """unload player data"""
        playerfile="players/%s.yaml" % self.name
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
        mv={"n":(0, 1), "s":(0, -1), "e":(-1, 0), "w":(1, 0)}
        if direction not in mv.keys():return

        #can't go through a blocked block
        if self.currmap:
            xx=int(self.position[0]+mv[direction][0]*speed)
            yy=int(self.position[1]+mv[direction][1]*speed)
            if collisions and self.currmap.isblocked((xx, yy)):return
        #update position
        self.position[0]+=mv[direction][0]*speed
        self.position[1]+=mv[direction][1]*speed

    def mineblock(self,blockposition):
        """Mine Block and put into inventory"""
        if not self.currmap:return 1 #Err: Map not assigned
        block=self.currmap.getblock(blockposition)
        if block:
            if not block.obstacle:return 3 # Block is not an obstacle
            err=self.inventory.additem(block.id)
            if err:print "Additem error code:",err
            else:self.currmap.setblock(blockposition,None)
            return 0 # Done
        else:return 2 # Err: Can't mine air (or empty block)

    def putblock(self,blockposition,blockID):
        """Put block on the map."""
        if not self.currmap:return 1 #Err: Map not assigned
        block=self.currmap.getblock(blockposition)
        if block:
            if block.obstacle:return 2 # Block exist
        if self.inventory.haveitem(blockID):
            err=self.inventory.removeitem(blockID)
            if err:print "Removeitem error code:",err
            newblock=engine.map.Block(blockID)
            self.currmap.setblock(blockposition,newblock)
            return 0 # Done
    def getposition(self):
        """Return position of ther player integer"""
        return (int(self.position[0]), int(self.position[1]))
