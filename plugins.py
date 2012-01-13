import Engine
import pygamefrontend

from pluginsystem import BasePlugin

class CorePlugin(BasePlugin):
    name="2dcraftercore"
    version="0.1"

    def setup(self):
        self.createHook("mineblock",self.on_block_mine)
        self.createHook("placeblock",self.on_block_place)
        self.createHook("daytimeupdate",self.on_daytime_update)
        self.createHook("daytimechange",self.on_daytime_change)
        self.createHook("messageadded",self.on_message_added)

    def on_block_mine(self,player,pos):
        print "Mine block event",pos,player
        player.mineblock(pos)

    def on_block_place(self,pos,block,player):
        print "Place block event"
        player.putblock(pos, block)

    def on_daytime_update(self):
        print "Daytime update event"
        Engine.environment.DAYTIME.updatedaytime()

    def on_daytime_change(self,daytime):
        pygamefrontend.functions.update_daytime_sounds(daytime)

    def on_message_added(self,message):
        print "Message:%s" % message
