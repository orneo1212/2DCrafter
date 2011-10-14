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
            if not item:
                newitemdata={"data":[],"changed":False}
                self.loaded[uid]=newitemdata
                return newitemdata
            #add loaded item and return it
            self.loaded[uid]=item
            return item
        else:return self.loaded[uid]

    def setchanged(self, uid):
        """Set item as changed"""
        if uid not in self.loaded.keys():return
        self.loaded[uid]["changed"]=True

    def unloaditems(self):
        """Unload changed items"""
        for loaded in self.loaded.keys():
            #save only chnaged
            if self.loaded[loaded]["changed"]:
                self.saveitem(loaded)

    def saveitem(self,uid):
        """Save item by uid"""
        print "Saving itemdata UID:%s" % uid
        if uid not in self.loaded.keys():return 1 #item with UID not exist
        #create world directory if not exist
        mappath=os.path.join(engine.mainpath, self.mapo.mapname)
        if not os.path.isdir(mappath):os.mkdir(mappath)
        newfile=os.path.join(mappath, str(uid)+".yaml")
        yaml.dump(self.loaded[uid], open(newfile,"w"))
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
