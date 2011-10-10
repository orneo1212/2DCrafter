
def ondestroy(position,player):
    player.currmap.setblock(position,None)
    for x in range(4):
        player.inventory.additem(10)

def onput(position,player):
    print "On put"
