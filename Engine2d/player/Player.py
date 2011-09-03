class Player:
    def __init__(self, name):
        self.name=name
        self.position=[0, 0]

    def move(self, direction, speed):
        """Move player to a given direction"""
        #north east west south up down
        mv={"n":(0, 1, 0), "s":(0, -1, 0), "e":(-1, 0, 0), "w":(1, 0, 0)}
        if direction not in mv.keys():return
        self.position[0]+=mv[direction][0]*speed
        self.position[1]+=mv[direction][1]*speed

    def getposition(self):
        """Return position of ther player integer"""
        return (int(self.position[0]), int(self.position[1]))