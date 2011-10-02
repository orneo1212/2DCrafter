class Player:
    def __init__(self, name, currmap=None):
        self.name=name
        self.position=[0, 0]
        self.currmap=currmap

    def setmap(self, mapobject):
        self.currmap=mapobject

    def move(self, direction, speed):
        """Move player to a given direction"""
        #north east west south up down
        mv={"n":(0, 1), "s":(0, -1), "e":(-1, 0), "w":(1, 0)}
        if direction not in mv.keys():return

        #can't go through a blocked block
        if self.currmap:
            xx=int(self.position[0]+mv[direction][0]*speed)
            yy=int(self.position[1]+mv[direction][1]*speed)
            #if self.currmap.isblocked((xx, yy)):return
        #update position
        self.position[0]+=mv[direction][0]*speed
        self.position[1]+=mv[direction][1]*speed

    def getposition(self):
        """Return position of ther player integer"""
        return (int(self.position[0]), int(self.position[1]))
