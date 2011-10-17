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
    print "Mine down stairs"

def MineUpstairs(player,block,blockposition):
    print "Mine down stairs"
