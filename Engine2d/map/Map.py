import os
import yaml
import Engine2d as engine

class Map:
    def __init__(self):
        self.sectors=[] # loaded sectors
        self.entities=[]
        self.mapname="world"
        self.maptype=0 # 0-outdoor 1-underground
        self.itemloader=engine.items.ItemLoader(self)

    # SET
    def setblock(self, position, newblock):
        secpos=self.convertposition(position)
        sector=self.getsector(secpos[0])
        sector.setblock(secpos[1], newblock)

    def setmapname(self,newmapname):
        """Set new name for map """
        self.mapname=newmapname
        for sector in self.sectors:
            if sector:sector.markmodified()

    # GET
    def getblock(self, position):
        """get block from global position=[x,y]
        """
        secpos=self.convertposition(position)
        sector=self.getsector(secpos[0])
        block=sector.getblock(secpos[1])
        return block

    def getsector(self, sectorposition):
        """get sector by position. Should always return Sector object"""
        for loadedsector in self.sectors:
            if loadedsector.position[0]==sectorposition[0] and \
                loadedsector.position[1]==sectorposition[1]:
                #return currently loaded sector
                return loadedsector
        sector=engine.map.loadsector(self.mapname, sectorposition)
        if sector==1:
            #not found loaded sector create new sector
            #Select correct map generator
            if self.maptype==0:
                sector=engine.map.Sector(sectorposition)
                engine.map.generate_outdoor(sector)
            elif self.maptype==1:
                sector=engine.map.Sector(sectorposition)
                engine.map.generate_underground(sector)
            sector.markmodified()

        #add it to loaded
        self.sectors.append(sector)
        return sector

    #OTHERS FUNCTIONS
    def isblocked(self, position):
        block=self.getblock(position)
        if block:return block.blocked

    def unloadsectors(self):
        """Unload all sectors"""
        for sector in self.sectors:
            if sector.modified:
                print "Unloading sector."
                engine.map.savesector(self.mapname, sector)
                self.sectors.remove(sector)

    def addentity(self, entity):
        if entity not in self.entities:
            self.entities.append(entity)

    def convertposition(self, position):
        """Convert position from world to sector"""
        secx=position[0]/engine.Config['SS']
        secy=position[1]/engine.Config['SS']
        #local position for sector tiles
        locx=position[0]-secx*engine.Config['SS']
        locy=position[1]-secy*engine.Config['SS']
        return [[int(secx), int(secy)], [int(locx), int(locy)]]

    def savemapdata(self):
        """Save map data to file"""
        #create world directory if not exist
        mapspath=os.path.join(engine.mainpath, self.mapname)
        if not os.path.isdir(mapspath):
            os.mkdir(mapspath)
        mapfile=os.path.join(mapspath,"world.yaml")
        try:
            datafile=open(mapfile,"w")
        except:return
        args={}
        args["daytime"]=engine.environment.DAYTIME.daytime
        args["mapseed"]=engine.seed
        yaml.dump(args,datafile)

    def loadmapdata(self):
        """Load map data from file"""
        worldpath=os.path.join(engine.mainpath, self.mapname)
        mapfile=os.path.join(worldpath,"world.yaml")
        try:
            data=yaml.load(open(mapfile))
        except:return
        engine.environment.DAYTIME.daytime=data["daytime"]
        engine.seed=data["mapseed"]
