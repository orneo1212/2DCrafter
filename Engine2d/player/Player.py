class Player:
    def __init__(self, name):
        self.name=name
        self.position=[0, 0]

    def move(self, direction, speed):
        """Move player to a given direction"""
        mv={"n":(0, 1), "s":(0, -1), "e":(-1, 0), "w":(1, 0)}
        if direction not in mv.keys():return
        self.position[0]+=mv[direction][0]*speed
        self.position[1]+=mv[direction][1]*speed
        #self.position[2]+=mv[direction][2]
        #TODO: Z position for move

    def getposition(self):
        """Return position of ther player integer"""
        return (int(self.position[0]), int(self.position[1]))