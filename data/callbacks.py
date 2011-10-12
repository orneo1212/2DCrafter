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
    #do openchest
