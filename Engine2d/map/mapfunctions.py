import random
import os
import yaml
import Engine2d as engine

def loadsector(mapname, sectorposition):
    """Load sector from given mapname at position sectorposition"""
    xx, yy=sectorposition
    try:
        data=open("%s/%iX%i" % (mapname, xx, yy))
    except IOError:
        return 1 # sector not loaded (not exist)

    sectordata=yaml.load(data)
    newsector=engine.map.Sector(sectorposition, generate=False)

    size=engine.Config['SS']
    for yy in range(size+1):
        for xx in range(size+1):
            if sectordata.has_key("%iX%i" % (xx, yy)):
                blockdata=sectordata["%iX%i" % (xx, yy)]
                if blockdata!=None:
                    #convert old format
                    if isinstance(blockdata,int):
                        print "Converting"
                        blockdata={"id":blockdata}
                    #create block
                    block=engine.map.Block(blockdata["id"])
                    #load metadata
                    if blockdata.has_key("uid"):
                        block.uid=blockdata["uid"]
                    #If not block
                    if block.id==None:block=None
                else:block=None
                newsector.setblock((xx, yy), block)
    newsector.marknotmodified()
    return newsector

def savesector(mapname, sector):
    """Save sector to folder named mapname."""
    #create world directory if not exist
    mapspath=os.path.join(engine.mainpath, mapname)
    if not os.path.isdir(mapspath):
        os.mkdir(mapspath)

    pos=sector.position

    sectorfile={}

    size=engine.Config['SS']
    for yy in range(size+1):
        for xx in range(size+1):
            data={}
            block=sector.getblock((xx, yy))
            #new format
            if block:
                data["id"]=block.id
                if block.uid!=0:data["uid"]=block.uid
            else:data["id"]=None

            sectorfile["%iX%i" % (xx, yy)]=data
    dfile=open("%s/%iX%i" % (mapname, pos[0], pos[1]), "w")
    yaml.dump(sectorfile, dfile)
    return 0 # Done

def randomgrow(sector):
    """Randomly grow blocks in sector"""
    for xx in range(6):
        nx=random.randint(0, engine.Config['SS'])
        ny=random.randint(0, engine.Config['SS'])
        block=sector.getblock((nx, ny))
        if not block:continue
        if block.ongrow:
            sector.setblock((nx, ny), None)
            sector.setblock((nx, ny), engine.map.Block(block.ongrow))
