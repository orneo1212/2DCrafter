import random
import Engine2d as engine
import math
import random

class Sector:
    def __init__(self, newposition):
        self.position=newposition
        self.blocks=self.makearray()
        self.items=self.makearray()
        self.modified=True

    def __str__(self):
        return "Sector at position %i,%i" % (self.position[0],self.position[1])

    def getblock(self, localposition,item=False):
        """get block(or item if item is True) from local position"""
        posx=int(localposition[0])
        posy=int(localposition[1])
        if item:return self.items[posy][posx]
        else:return self.blocks[posy][posx]

    def setblock(self, localposition, block,item=False):
        """set block(or item if item is True) in local position"""
        posx=int(localposition[0])
        posy=int(localposition[1])
        if item:self.items[posy][posx]=block
        else:self.blocks[posy][posx]=block
        self.markmodified()

    def markmodified(self):
        """Mark sector as modified"""
        self.modified=True

    def marknotmodified(self):
        """Mark sector as not modified"""
        self.modified=False

    def makearray(self):
        """Make array for blocks data"""
        array=[]
        size=engine.Config['SS']
        for yy in range(size+1):
            line=[]
            for xx in range(size+1):
                line.append(None)
            array.append(line);line=[]
        return array
