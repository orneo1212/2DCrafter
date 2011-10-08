import Engine2d as engine
import yaml

def loadsector(mapname, sectorposition):
    """Load sector from given mapname at position sectorposition"""
    xx, yy=sectorposition
    try:
        data=open("%s/%iX%i" % (mapname, xx, yy))
    except IOError:
        return 1 # sector not loaded (not exist)

    sectordata=yaml.load(data)
    newsector=engine.map.Sector(sectorposition,generate=False)

    size=engine.Config['SS']
    for yy in range(size+1):
        for xx in range(size+1):
            if sectordata.has_key("%iX%i" % (xx, yy)):
                blockid=sectordata["%iX%i" % (xx, yy)]
                if blockid!=None:
                    block=engine.map.Block(blockid)
                else:block=None
                newsector.setblock((xx, yy), block)
    newsector.marknotmodified()
    return newsector

def savesector(mapname, sector):
    """Save sectot to folder named mapname."""
    #TODO: create world directory if not exist
    pos=sector.position

    sectorfile={}

    size=engine.Config['SS']
    for yy in range(size+1):
        for xx in range(size+1):
            block=sector.getblock((xx, yy))
            if block:data=block.id
            else:data=None
            sectorfile["%iX%i" % (xx, yy)]=data
    yaml.dump(sectorfile, open("%s/%iX%i" % (mapname, pos[0], pos[1]), "w"))
    return 0 # Done
