import sys
import time
import Engine
from data import callbacks

class Block:
    """Class represent each block in game"""
    def __init__(self, idd):
        self.id=idd
        self.uid=0 #unique id or 0
        self.name=""
        self.blocked=False # block move through
        self.obstacle=True
        # lightradius is a radius in tiles
        self.lightradius=0 # if greeter then 0 will emit light
        self.mineitems=[] # items droped by block when mined
        self.ongrow=0 # item id when block grow
        self.growtime=0 # time needed to grow
        self.startgrowtime=0
        self.onput=0 # item id when block right click (action e.g.door)
        self.unique=False # Is unique object like chests, signs
        self.itemdata=None
        self.item=False # is this block item?
        #callbacks
        self.onputcall=None # when player put a block
        self.onminecall=None
        self.onputemptycall=None
        #restore default values from config
        self.restorefromconfig()

    def generateUID(self):
        """Generate unique id"""
        self.uid=id(self)+int(time.time())

    def getcallfunction(self,functionname):
        """Return function object by name to call or None"""
        if not callbacks.__dict__.has_key(functionname):return None
        function=getattr(callbacks,functionname)
        return function

    def restorefromconfig(self):
        """restore settings from blocks.yaml if possible """
        blocks=Engine.blocks
        if self.id not in blocks.keys():return
        #
        bldata=blocks[self.id] # block data
        if bldata.has_key("name"):
            self.name=Engine.blocks[self.id]["name"]
        if bldata.has_key("blocked"):
            self.blocked=Engine.blocks[self.id]["blocked"]
        if bldata.has_key("obstacle"):
            self.obstacle=Engine.blocks[self.id]["obstacle"]
        if bldata.has_key("item"):
            self.item=Engine.blocks[self.id]["item"]
        if bldata.has_key("lightradius"):
            self.lightradius=Engine.blocks[self.id]["lightradius"]
        if bldata.has_key("mineitems"):
            self.mineitems=Engine.blocks[self.id]["mineitems"]
        if bldata.has_key("ongrow"):
            self.ongrow=Engine.blocks[self.id]["ongrow"]
        if bldata.has_key("growtime"):
            self.growtime=Engine.blocks[self.id]["growtime"]
            self.startgrowtime=int(time.time())
        if bldata.has_key("onput"):
            self.onput=Engine.blocks[self.id]["onput"]
        if bldata.has_key("unique"):
            self.unique=Engine.blocks[self.id]["unique"]
        #callbacks
        if bldata.has_key("onputcall"):
            fn=Engine.blocks[self.id]["onputcall"]
            self.onputcall=self.getcallfunction(fn)
        if bldata.has_key("onminecall"):
            fn=Engine.blocks[self.id]["onminecall"]
            self.onminecall=self.getcallfunction(fn)
        if bldata.has_key("onputemptycall"):
            fn=Engine.blocks[self.id]["onputemptycall"]
            self.onputemptycall=self.getcallfunction(fn)
