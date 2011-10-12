import sys

import Engine2d as engine

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
        self.onput=0 # item id when block right click (replace blocks)
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
            if bldata.has_key("mineitems"):
                self.mineitems=engine.blocks[self.id]["mineitems"]
            if bldata.has_key("ongrow"):
                self.ongrow=engine.blocks[self.id]["ongrow"]
            if bldata.has_key("onput"):
                self.onput=engine.blocks[self.id]["onput"]
