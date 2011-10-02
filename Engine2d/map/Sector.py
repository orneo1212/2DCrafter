import random
import Engine2d as engine
import math
import random

class Sector:
    def __init__(self, newposition):
        self.position=newposition
        self.blocks=self.makearray()
        self.modified=True
        self.generate()

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
    def makenoise(self,divide,x,y):
        pnoise=engine.tools.pnoise
        seed=engine.seed

        divide=float(divide)
        return pnoise(x/divide,y/divide,seed)

    def generate(self):
        """Generate new sector"""
        x,y=self.position

        print "Generating sector %s" % self.position

        size=engine.Config['SS']

        #fill
        for yy in range(size+1):
            for xx in range(size+1):
                blockid=0 # air

                #global position
                nx=self.position[0]*size+xx+1
                ny=self.position[1]*size+yy+1
                if ny>1:continue
                #noises
                noise=int(self.makenoise(5, nx,ny/0.5)*15%7)
                if noise>0.9:blockid=1
                block=engine.map.Block(blockid)
                self.setblock([xx,yy],block)
