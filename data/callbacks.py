import Engine2d as engine

def OpenChest(player,position):
    """Open Chest"""
    mapo=player.currmap
    chestblock=mapo.getblock(position)
    #Generate unique ID when not exist
    if chestblock.uid==0:
        chestblock.generateUID()
    #mark sector as modified to save block data
    positions=mapo.convertposition(position)
    sectorposition=positions[0]
    sector=mapo.getsector(sectorposition)
    sector.markmodified()
    #init new chest if needed
    if not chestblock.itemdata:
        chestblock.itemdata={}
        chestblock.itemdata["data"]=[None]*32
    #set player action data
    player.actiondata=chestblock

def MoveDown(player,position):
    """Move down"""
    player.movedown(position)

def MoveUp(player,position):
    """Move up"""
    player.moveup(position)

def MineDownStairs(player,block,blockposition):
    pass

def MineUpstairs(player,block,blockposition):
    pass

def PutUpstairs(player, block, blockposition):
    if player.mapindex==0:return 1 # Error. can place stairs up
    nmap=engine.map.mapstack.getmapbyindex(player.mapindex+1)
    nmap.setblock(blockposition,engine.map.Block(22))
    return 0

def PutDownstairs(player, block, blockposition):
    print "Put stairs down"
