
class Block:
    """Class represent each block in game"""
    def __init__(self, idd):
        self.id=idd
        self.blocked=False # block move through
        self.destoyable=True # can't be destroyed?
        self.putable=True

    #callbacks
    def onDestroy(self):
        """Will be call when player destroy this block"""
        if self.destoyable:
            pass # call here

    def onPut(self):
        """Will be call when player put block"""
        if self.putable:
            pass # call here
