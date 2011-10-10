
def ondestroy(position,player):
    player.currmap.setblock(position,None)
    player.inventory.additem(7)

def onput(position,player):
    print "On put"
