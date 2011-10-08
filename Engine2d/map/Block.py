import Engine2d as engine

class Block:
    """Class represent each block in game"""
    def __init__(self, idd):
        self.id=idd
        self.name=""
        self.blocked=False # block move through
        self.destoyable=True # can be destroyed?
        self.obstacle=True
        self.putable=True
        # lightradius is a radius in tiles
        self.lightradius=0 # if greeter then 0 will emit light
        self.restorefromconfig()

    def restorefromconfig(self):
        """restore settings from blocks.yaml if possible """
        blocks=engine.blocks
        if self.id in blocks.keys():
            bldata=blocks[self.id] # block data
            if bldata.has_key("name"):
                self.name=engine.blocks[self.id]["name"]
            if bldata.has_key("blocked"):
                self.blocked=engine.blocks[self.id]["blocked"]
            if bldata.has_key("obstacle"):
                self.obstacle=engine.blocks[self.id]["obstacle"]
            if bldata.has_key("lightradius"):
                self.lightradius=engine.blocks[self.id]["lightradius"]

    #callbacks
    def onDestroy(self,player):
        """Will be call when player destroy this block"""
        if self.destoyable:
            pass # call here

    def onPut(self,player):
        """Will be call when player put block"""
        if self.putable:
            pass # call here
