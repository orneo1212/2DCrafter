import random
import Engine2d as engine
import math
import random

class Sector:
    def __init__(self, newposition,generate=True):
        self.position=newposition
        self.blocks=self.makearray()
        self.modified=True
        if generate:self.generate()

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
                #noises
                h=self.makenoise(nx,ny,64)*128
                h=int(128+h)
                ndetail=self.makenoise(nx,ny,2,869)
                ndetail2=self.makenoise(nx,ny,2,7965)
                trees=ndetail>0.4 and ndetail2>0.1

                #water level
                if h<128:
                    blockid=3
                #ground level h>128
                else:
                    if h>=128:blockid=4 #sand
                    if h>=128+8:blockid=2 #mud
                    if h>=128+8 and trees:blockid=7 #tree
                    if h>=128+45:blockid=1 #stone

                block=engine.map.Block(blockid)
                self.setblock([xx,yy],block)
