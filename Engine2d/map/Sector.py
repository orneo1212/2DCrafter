import random
import Engine2d as engine

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
        posz=int(localposition[2])
        return self.blocks[posz][posy][posx]

    def setblock(self, localposition, block):
        """set block in local position"""
        posx=int(localposition[0])
        posy=int(localposition[1])
        posz=int(localposition[2])
        self.blocks[posz][posy][posx]=block

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
        for zz in range(size+1):
            ss=[]
            for yy in range(size+1):
                line=[]
                for xx in range(size+1):
                    line.append(None)
                ss.append(line);line=[]
            array.append(ss);ss=[]
        return array

    def generate(self):
        """Generate new sector"""
        x,y,z=self.position
        print "Generating sector %s" % self.position

        size=engine.Config['SS']

        #fill
        for zz in range(size+1):
            for yy in range(size+1):
                for xx in range(size+1):
                    blockid=0 # air
                    nx=self.position[0]*size+xx+0.5
                    ny=self.position[1]*size+yy+0.5
                    nz=self.position[2]*size+zz+0.5
                    noise=engine.tools.pnoise(nx,ny,nz)*100
                    #ground
                    if noise<0:
                        blockid=0
                    #air
                    if noise>=0:
                        blockid=1
                    self.setblock([xx,yy,zz],engine.map.Block(blockid))
