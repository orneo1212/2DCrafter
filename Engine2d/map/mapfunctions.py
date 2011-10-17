import random
import os
import time
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
    newsector=engine.map.Sector(sectorposition)

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
                    if blockdata.has_key("itemdata"):
                        block.itemdata=blockdata["itemdata"]
                    #If not block
                    if block.id==None:block=None
                    if block.id==0:block=None
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
                if block.id==0:continue
                data["id"]=block.id
                if block.uid!=0:data["uid"]=block.uid
                if block.itemdata!=None:data["itemdata"]=block.itemdata
            else:continue

            sectorfile["%iX%i" % (xx, yy)]=data
    dfile=open("%s/%iX%i" % (mapname, pos[0], pos[1]), "w")
    yaml.dump(sectorfile, dfile)
    return 0 # Done

def randomgrow(map):
    """Randomly grow blocks in map"""
    try:
        sector=random.choice(map.sectors)
    except:return
    for yy in range(engine.Config['SS']):
        for xx in range(engine.Config['SS']):
            block=sector.getblock((xx, yy))
            if not block:continue
            if block.ongrow:
                if time.time()-block.startgrowtime>block.growtime:
                    sector.setblock((xx, yy), None)
                    sector.setblock((xx, yy), engine.map.Block(block.ongrow))

def generate_outdoor(sector):
    """Generate new sector (outdoor)"""
    x,y=sector.position
    print "Generating sector %s" % sector.position

    size=engine.Config['SS']

    #fill
    for yy in range(size+1):
        for xx in range(size+1):
            blockid=0 # air

            #global position
            nx=x*size+xx+1
            ny=y*size+yy+1
            #noises
            h=sector.makenoise(nx,ny,512)*128 -\
                sector.makenoise(nx,ny,8,276)*8
            h=int(128+h)

            #others
            ndetail=sector.makenoise(nx,ny,2,869)
            ndetail2=sector.makenoise(nx,ny,2,7965)
            ngravel=sector.makenoise(nx,ny,8,8496)
            nstone=sector.makenoise(nx,ny,64,9865)
            nwater=sector.makenoise(nx,ny,12,1045)

            #
            trees=ndetail>0.4 and ndetail2>0.1
            coalore=ndetail>0.4 and ndetail2>0.2
            ironore=ndetail>0.4 and ndetail2>0.4
            gravel=ngravel>0.6
            stone=nstone>0.2
            water=nwater>0.4
            lava=nwater and gravel
            blackmarble=stone and ndetail2>0.2

            #water level
            if h<128:
                blockid=3
            #ground level h>128
            else:
                #coast layer
                if h>=128:blockid=4 #sand
                #mud layer
                if h>=128+8:blockid=9 #grass
                if h>=128+8 and trees:blockid=7 #tree
                if h>=128+8 and gravel:blockid=16 #gravel
                if h>=128+8 and stone:blockid=1 #stone
                if h>=128+8 and stone and coalore:blockid=13 #coal ore
                if h>=128+8 and stone and ironore:blockid=14 #Iron ore
                #stone layer
                if h>=128+45:blockid=1 #stone
                if h>=128+45 and coalore:blockid=13 #coal ore
                if h>=128+45 and ironore:blockid=14 #Iron ore
                if h>=128+60 and blackmarble:blockid=21 #Blk marble
                #
                if h>=128 and water:blockid=3 #lakes
                if h>=128 and lava:blockid=5 #lava lakes
            #create block and put on sector
            if blockid:block=engine.map.Block(blockid)
            else:block=None
            sector.setblock([xx,yy],block)

def generate_underground(sector):
    """Generate new sector (underground)"""
    x,y=sector.position
    print "Generating sector %s" % sector.position

    size=engine.Config['SS']

    #fill
    for yy in range(size+1):
        for xx in range(size+1):
            blockid=0 # air

            #global position
            nx=x*size+xx+1
            ny=y*size+yy+1
            #noises
            h=sector.makenoise(nx,ny,512)*128
            h=int(128+h)

            #others
            ndetail=sector.makenoise(nx,ny,2,869)
            ndetail2=sector.makenoise(nx,ny,2,7965)
            ngravel=sector.makenoise(nx,ny,8,8496)
            nstone=sector.makenoise(nx,ny,64,9865)
            nwater=sector.makenoise(nx,ny,12,1045)

            coalore=ndetail>0.4 and ndetail2>0.2
            ironore=ndetail>0.4 and ndetail2>0.4
            gravel=ngravel>0.6
            stone=nstone>0.2
            water=nwater>0.4
            lava=nwater and gravel
            blackmarble=stone and ndetail2>0.2

            #water level (stone underground)
            if h<128:
                blockid=1 #underground stone
            #ground level h>128
            else:
                if h>128:blockid=16
                if h>=128+8 and gravel:blockid=16 #gravel
                if h>=128+8 and stone:blockid=1 #stone
                if h>=128+8 and stone and coalore:blockid=13 #coal ore
                if h>=128+8 and stone and ironore:blockid=14 #Iron ore
                #stone layer
                if h>=128+45:blockid=1 #stone
                if h>=128+45 and coalore:blockid=13 #coal ore
                if h>=128+45 and ironore:blockid=14 #Iron ore
                if h>=128+60 and blackmarble:blockid=21 #Blk marble
                #
                if h>=128 and water:blockid=3 #lakes
                if h>=128 and lava:blockid=5 #lava lakes
            #create block and put on sector
            if blockid:block=engine.map.Block(blockid)
            else:block=None
            sector.setblock([xx,yy],block)
