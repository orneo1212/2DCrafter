import os
import yaml
import Engine2d as engine

class ItemLoader(engine.dataobj.DataLoader):
    def __init__(self,mapobject):
        engine.dataobj.DataLoader.__init__(self,"")
        self.mapo=mapobject # Map Object
        self.loaded={} # example of item {"data":{"data":None},"changed":False}

    def getitem(self,uid):
        """Get item by uid return item data"""
        if uid not in self.loaded.keys():
            item=self.loaditem(uid)
            if not item:return {"data":{},"changed":False}
            #add loaded item and return it
            self.loaded[uid]=item
            return item
        else:return self.loaded[uid]

    def unloaditems(self):
        """Unload changed items"""
        for loaded in self.loaded.keys():
            #save only chnaged
            if self.loaded[loaded]["changed"]:
                self.saveitem(self.loaded[loaded])

    def saveitem(self,uid):
        """Save item by uid"""
        if uid not in self.loaded:return 1 #item with UIS not exist
        #create world directory if not exist
        mappath=os.path.join(engine.mainpath, self.mapo.mapname)
        if not os.path.isdir(mappath):os.mkdir(mappath)
        newfile=os.path.join(mappath, str(uid)+".yaml")
        yaml.dump(self.loaded[uid], newfile)
        return 0 # Done

    def loaditem(self,uid):
        """Load item by UID"""
        #create world directory if not exist
        mappath=os.path.join(engine.mainpath, self.mapo.mapname)
        if not os.path.isdir(mappath):os.mkdir(mappath)
        itemfilepath=os.path.join(mappath, str(uid)+".yaml")
        try:itemfile=open(itemfilepath,"r")
        except IOError:return None #  File not found
        return yaml.load(itemfile)
