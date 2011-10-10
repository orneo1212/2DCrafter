import sys

import Engine2d as engine

class Block:
    """Class represent each block in game"""
    def __init__(self, idd):
        self.id=idd
        self.name=""
        self.blocked=False # block move through
        self.obstacle=True
        # lightradius is a radius in tiles
        self.lightradius=0 # if greeter then 0 will emit light
        self.callbacksmodule=None # Name of module with callbacks for this block
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
            if bldata.has_key("callbacksmodule"):
                modname=engine.blocks[self.id]["callbacksmodule"]
                try:
                    module=__import__("Callbacks."+modname)
                    self.callbacksmodule=getattr(module, modname)
                except Exception:self.callbacksmodule=None

    def _callcallback(self,callbackname,args):
        if self.callbacksmodule:
            module=self.callbacksmodule
            if module.__dict__.has_key(callbackname):
                try:
                    module.__dict__[callbackname](**args)
                except Exception,e:
                    print "Error in %s." % callbackname,e
    #callbacks
    def onDestroy(self,position, player):
        """Will be call when player destroy this block"""
        args={
            "player":player,
            "position":position,
            }
        self._callcallback("ondestroy",args)

    def onPut(self,position, player):
        """Will be call when player put block"""
        args={
            "player":player,
            "position":position,
            }
        self._callcallback("onput",args)
