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
        seed=65535

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

                #noises
                detailp=self.makenoise(70, nx, ny)
                waterp=self.makenoise(300, nx, ny)
                stonep=self.makenoise(100, nx, ny)
                mudp=self.makenoise(70, nx, ny)
                lavap=self.makenoise(4, nx, ny)
                sandp=self.makenoise(70, nx, ny)
                treep=self.makenoise(3, nx, ny)

                #check
                isstone=stonep>0.88
                ismud=mudp>0.07 and mudp < 0.49
                islava=lavap<0.5 and waterp<0
                issand=sandp>0 and sandp<0.5 and waterp>0
                istree=treep>0.48 and ismud and waterp>0

                if istree:blockid=7 #tree
                elif isstone:blockid=1 # stone
                elif islava:blockid=5 # lava
                elif ismud:blockid=2 # mud
                elif issand:blockid=4 # sand
                else:blockid=3 # water

                self.setblock([xx,yy],engine.map.Block(blockid))
