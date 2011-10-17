import Engine2d as engine

class MapStack:
    def __init__(self):
        self.loaded={}

    def getmapbyindex(self,index):
        """Get map by index"""
        if self.loaded.has_key(index):
            return self.loaded[index]
        else:
            newmap=engine.map.Map()
            newmap.index=index
            newmap.mapname="world"+str(index)
            if index>0:newmap.maptype=1
            else:newmap.maptype=0
            newmap.loadmapdata()
            self.loaded[index]=newmap
            return newmap

    def unloadall(self):
        """Unload all loaded maps"""
        for mapid in self.loaded.keys():
            mapo=self.loaded[mapid]
            #print "Unloading MAP with index",mapo.mapname, len(mapo.sectors)
            mapo.savemapdata()
            mapo.unloadsectors()
        return

mapstack=MapStack()
