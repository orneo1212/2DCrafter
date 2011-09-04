import Engine2d as engine

class Block:
    """Class represent each block in game"""
    def __init__(self, idd):
        self.id=idd
        self.name=""
        self.blocked=False # block move through
        self.destoyable=True # can't be destroyed?
        self.putable=True
        #restore settings from blocks.yaml if possible
        if self.id in engine.blocks.keys():
            self.name=engine.blocks[self.id]["name"]
            self.blocked=engine.blocks[self.id]["blocked"]

    #callbacks
    def onDestroy(self):
        """Will be call when player destroy this block"""
        if self.destoyable:
            pass # call here

    def onPut(self):
        """Will be call when player put block"""
        if self.putable:
            pass # call here
