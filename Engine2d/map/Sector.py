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
        posz=int(localposition[1])
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
        for zz in range(engine.Config["SS"]+1):
            ss=[]
            for yy in range(engine.Config["SS"]+1):
                line=[]
                for xx in range(engine.Config["SS"]+1):
                    line.append(None)
                ss.append(line);line=[]
            array.append(ss);ss=[]
        return array

    def generate(self):
        """Generate new sector"""
        x,y,z=self.position
        print "Generating sector %s" % self.position
        if y<0:blocks=[1,2]
        else:blocks=[0]


        #fill
        for zz in range(engine.Config['SS']):
            for yy in range(engine.Config['SS']):
                for xx in range(engine.Config['SS']):
                    blockid=random.choice(blocks)
                    self.setblock([xx,yy,zz],engine.map.Block(blockid))
