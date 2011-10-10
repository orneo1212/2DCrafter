import Engine2d as engine

def ondestroy(position,player):
    player.currmap.setblock(position,None)
    player.inventory.additem(2)

def onput(position,player):
    print "On put"

def ongrow(block, sector, position):
    sector.setblock(position,None)
    sector.setblock(position,engine.map.Block(9))
