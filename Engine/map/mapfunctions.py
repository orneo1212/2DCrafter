import random
import os
import time
import json
import Engine

def makenoise(x,y,freq,seedchange=0):
    """make perlin noise for global X and Y position.
    seedchange is value added to seed to perform other noise"""
    pnoise=Engine.tools.pnoise
    seed=Engine.seed

    freq=1/float(freq)
    return pnoise(x*freq,y*freq,seed+seedchange)

def loadsector(mapname, sectorposition, worldname="world"):
    """Load sector from given mapname at position sectorposition"""
    #paths
    worldpath=os.path.join(Engine.mainpath, worldname)
    mapspath=os.path.join(worldpath, mapname)

    xx, yy=sectorposition
    sectorpath=os.path.join(mapspath,"%iX%i" % (xx, yy))
    try:data=open(sectorpath)
    except IOError:
        return 1 # sector not loaded (not exist)

    sectordata=json.load(data)
    newsector=Engine.map.Sector(sectorposition)

    size=Engine.Config['SS']
    for layer in [0,1]: # layers 0=blocks 1=items
        for yy in xrange(size+1):
            for xx in xrange(size+1):
                if sectordata.has_key("%i|%iX%i" % (layer, xx, yy)):
                    blockdata=sectordata["%i|%iX%i" % (layer, xx, yy)]
                    if blockdata!=None:
                        #create block
                        block=Engine.map.Block(blockdata["id"])
                        #load metadata
                        if blockdata.has_key("uid"):
                            block.uid=blockdata["uid"]
                        if blockdata.has_key("itemdata"):
                            block.itemdata=blockdata["itemdata"]
                        #If not block
                        if block.id==None:block=None
                        if block.id==0:block=None
                    else:block=None
                    #put block on the map on the correct layer
                    newsector.setblock((xx, yy), block, layer)
    newsector.marknotmodified()
    return newsector

def savesector(mapname, sector, worldname="world"):
    """Save sector to folder named mapname."""
    #paths
    worldpath=os.path.join(Engine.mainpath, worldname)
    mapspath=os.path.join(worldpath, mapname)
    #create directories if not exist
    if not os.path.isdir(worldpath):os.mkdir(worldpath)
    if not os.path.isdir(mapspath):os.mkdir(mapspath)

    pos=sector.position

    sectorfile={}

    size=Engine.Config['SS']
    for layer in [0,1]: # layers 0=blocks 1=items
        for yy in xrange(size+1):
            for xx in xrange(size+1):
                data={}
                block=sector.getblock((xx, yy), layer)
                #new format
                if block:
                    if block.id==0:continue
                    data["id"]=block.id
                    if block.uid!=0:data["uid"]=block.uid
                    if block.itemdata!=None:data["itemdata"]=block.itemdata
                else:continue
                #fill dictionary with block/item data
                sectorfile["%i|%iX%i" % (layer, xx, yy)]=data
    #Store data
    sectorpath=os.path.join(mapspath, "%iX%i" % (pos[0], pos[1]) )
    dfile=open(sectorpath, "w")
    json.dump(sectorfile,dfile)
    return 0 # Done

def randomgrow(map):
    """Randomly grow blocks in map"""
    try:
        sector=random.choice(map.sectors)
    except:return
    for yy in xrange(Engine.Config['SS']):
        for xx in xrange(Engine.Config['SS']):
            block=sector.getblock((xx, yy))
            if not block:continue
            if block.ongrow:
                if time.time()-block.startgrowtime>block.growtime:
                    sector.setblock((xx, yy), None)
                    sector.setblock((xx, yy), Engine.map.Block(block.ongrow))

def generate_outdoor(sector):
    """Generate new sector (outdoor)"""
    x,y=sector.position
    print "Generating sector %s" % sector.position

    size=Engine.Config['SS']

    #fill
    for yy in xrange(size+1):
        for xx in xrange(size+1):
            blockid=0 # air

            #global position
            nx=x*size+xx+1
            ny=y*size+yy+1
            #noises
            h=makenoise(nx,ny,512)*128 -\
                makenoise(nx,ny,8,276)*8
            h=int(128+h)

            #others
            ndetail=makenoise(nx,ny,2,869)
            ndetail2=makenoise(nx,ny,2,7965)
            ngravel=makenoise(nx,ny,8,8496)
            nstone=makenoise(nx,ny,64,9865)
            nwater=makenoise(nx,ny,12,1045)

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
            if blockid:block=Engine.map.Block(blockid)
            else:block=None
            sector.setblock([xx,yy],block)

def generate_underground(sector,seedchange=0):
    """Generate new sector (underground)"""
    x,y=sector.position
    print "Generating sector %s" % sector.position

    size=Engine.Config['SS']

    #fill
    for yy in range(size+1):
        for xx in range(size+1):
            blockid=0 # air

            #global position
            nx=x*size+xx+1
            ny=y*size+yy+1
            #noises
            h=makenoise(nx,ny,512,seedchange)*128
            h=int(128+h)

            #others
            ndetail=makenoise(nx,ny,2,869+seedchange)
            ndetail2=makenoise(nx,ny,2,7965+seedchange)
            ngravel=makenoise(nx,ny,8,8496+seedchange)
            nstone=makenoise(nx,ny,64,9865+seedchange)
            nwater=makenoise(nx,ny,12,1045+seedchange)

            coalore=ndetail>0.4 and ndetail2>0.2
            ironore=ndetail>0.4 and ndetail2>0.4
            gravel=ngravel>0.6
            stone=nstone>0.2
            water=nwater>0.4
            lava=nwater and gravel
            blackmarble=stone and ndetail2>0.2

            #water level (stone underground)
            if h<128:
                if h<128:blockid=1 # Stone
                if h<=128-45 and coalore:blockid=13 #coal ore
                if h<=128-45 and ironore:blockid=14 #Iron ore
                if h<=128-60 and blackmarble:blockid=21 #Blk marble
            #ground level h>128
            else:
                if h>=128:blockid=16
                if h>=128+5:blockid=1
                if h>=128+5 and coalore:blockid=13 #coal ore
                if h>=128+5 and ironore:blockid=14 #Iron ore
                if h>=128+5 and blackmarble:blockid=21 #Blk marble
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
            if blockid:block=Engine.map.Block(blockid)
            else:block=None
            sector.setblock([xx,yy],block)
