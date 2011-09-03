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

        SEED=12345

        #fill
        for zz in range(size+1):
            for yy in range(size+1):
                for xx in range(size+1):
                    blockid=0 # air
                    nx=self.position[0]*size+xx
                    ny=self.position[1]*size+yy
                    nz=self.position[2]*size+zz
                    #noise height
                    h=20.0*engine.tools.pnoise(nx/100.0,ny/100.0,SEED+0)
                    h+=15.0*engine.tools.pnoise(nx/30.0,ny/30.0,SEED+65535)
                    if engine.tools.pnoise(nx/30.0,ny/30.0,SEED)>0.5:
                        h+=10.0
                    h=int(h)

                    if nz<h:
                        blockid=1
                    elif nz<=1:
                        blockid=0
                    self.setblock([xx,yy,zz],engine.map.Block(blockid))
