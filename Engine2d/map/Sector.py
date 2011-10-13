import random
import Engine2d as engine
import math
import random

class Sector:
    def __init__(self, newposition):
        self.position=newposition
        self.blocks=self.makearray()
        self.modified=True

    def getblock(self, localposition):
        """get block from local position"""
        posx=int(localposition[0])
        posy=int(localposition[1])
        return self.blocks[posy][posx]

    def setblock(self, localposition, block):
        """set block in local position"""
        posx=int(localposition[0])
        posy=int(localposition[1])
        self.blocks[posy][posx]=block
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

    #temp
    def makenoise(self,x,y,freq,seedchange=0):
        pnoise=engine.tools.pnoise
        seed=engine.seed

        freq=1/float(freq)
        return pnoise(x*freq,y*freq,seed+seedchange)
