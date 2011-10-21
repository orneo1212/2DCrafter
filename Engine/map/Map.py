import os
import json
import Engine

class Map:
    def __init__(self):
        self.sectors=[] # loaded sectors
        self.entities=[]
        self.mapname="layer"
        self.maptype=0 # 0-outdoor 1-underground
        self.index=0

    # SET
    def setmapname(self, newmapname):
        """Set new name for map """
        self.mapname=newmapname
        for sector in self.sectors:
            if sector:sector.markmodified()

    def setblock(self, position, newblock, item=False):
        """Set block(or item if item is True) at global position"""
        secpos=self.convertposition(position)
        sector=self.getsector(secpos[0])
        sector.setblock(secpos[1], newblock, item)

    # GET
    def getblock(self, position, item=False):
        """get block(or item if item is True) from global position=[x,y]
        """
        secpos=self.convertposition(position)
        sector=self.getsector(secpos[0])
        block=sector.getblock(secpos[1], item)
        return block

    def getsector(self, sectorposition):
        """get sector by position. Should always return Sector object"""
        for loadedsector in self.sectors:
            if loadedsector.position[0]==sectorposition[0] and \
                loadedsector.position[1]==sectorposition[1]:
                #return currently loaded sector
                return loadedsector
        sector=Engine.map.loadsector(self.mapname, sectorposition)
        if sector==1:
            #not found loaded sector create new sector
            #Select correct map generator
            if self.maptype==0:
                sector=Engine.map.Sector(sectorposition)
                Engine.map.generate_outdoor(sector)
            elif self.maptype==1:
                sector=Engine.map.Sector(sectorposition)
                Engine.map.generate_underground(sector,self.index*97)
            sector.markmodified()

        #add it to loaded
        self.sectors.append(sector)
        return sector

    #OTHERS FUNCTIONS
    def isblocked(self, position):
        """Return True if position is blocked"""
        #check block
        block=self.getblock(position)
        if block and block.blocked:return True
        #check item
        item=self.getblock(position,True) #item get
        if item and item.blocked:return True
        return False

    def unloadsectors(self):
        """Unload all sectors"""
        for sector in self.sectors:
            if sector.modified:
                print "Unloading sector.", sector
                Engine.map.savesector(self.mapname, sector)
        #clear momory used by sectors
        #TODO:only not used sectors should be unloaded
        #self.sectors=[]

    def addentity(self, entity):
        if entity not in self.entities:
            self.entities.append(entity)

    def convertposition(self, position):
        """Convert position from world to sector"""
        secx=position[0]/Engine.Config['SS']
        secy=position[1]/Engine.Config['SS']
        #local position for sector tiles
        locx=position[0]-secx*Engine.Config['SS']
        locy=position[1]-secy*Engine.Config['SS']
        return [[int(secx), int(secy)], [int(locx), int(locy)]]

    def savemapdata(self, worldname="world"):
        """Save map data to file"""
        #create world directory if not exist
        worldpath=os.path.join(Engine.mainpath, worldname)
        mapspath=os.path.join(worldpath, self.mapname)
        if not os.path.isdir(worldpath):os.mkdir(worldpath)
        if not os.path.isdir(mapspath):os.mkdir(mapspath)
        mapfile=os.path.join(mapspath, "worlddata.txt")
        try:
            datafile=open(mapfile, "w")
        except:return
        args={}
        args["daytime"]=Engine.environment.DAYTIME.daytime
        args["mapseed"]=Engine.seed
        json.dump(args, datafile)
        datafile.close()

    def loadmapdata(self, worldname="world"):
        """Load map data from file"""
        worldpath=os.path.join(Engine.mainpath, worldname)
        layerspath=os.path.join(worldpath, self.mapname)
        mapfile=os.path.join(layerspath, "worlddata.txt")
        try:
            data=open(mapfile)
        except:return

        mapdata=json.load(data) # load mapdata from file
        Engine.environment.DAYTIME.daytime=mapdata["daytime"]
        print
        Engine.seed=mapdata["mapseed"]
