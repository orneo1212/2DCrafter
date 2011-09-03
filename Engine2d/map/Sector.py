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

                #noises
                biome=int(self.makenoise(300, nx, ny)*15%7)
                detailp=self.makenoise(70, nx, ny)
                waterp=self.makenoise(300, nx, ny)
                mudp=self.makenoise(70, nx, ny)
                sandp=self.makenoise(70, nx, ny)
                treep=self.makenoise(3, nx, ny)
                #biomes
                #0 tree and mud
                #1 mud
                #2 desert sand
                #check
                ismud=mudp>0 and biome in [0,1]
                issand=sandp>0 and biome==2
                istree=treep>0.6 and ismud and biome ==0

                if istree:blockid=7 #tree
                elif ismud:blockid=2 # mud
                elif issand:blockid=4 # sand
                else:blockid=3 # water

                self.setblock([xx,yy],engine.map.Block(blockid))
