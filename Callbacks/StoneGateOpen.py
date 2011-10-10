import Engine2d as engine

def ondestroy(position,player):
    player.currmap.setblock(position,None)
    player.inventory.additem(11)

def onput(position,player):
    player.currmap.setblock(position,None)
    player.currmap.setblock(position,engine.map.Block(11))
