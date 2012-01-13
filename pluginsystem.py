"""
Plugin system with logging support
Author: orneo1212 <orneo1212@gmail.com>
"""
import logging

#################
# EVENT
#################
class Event:
    """
    Base event
    """
    def __init__(self,name,**args):
        self.name=name
        self.args=args


#################
# PLUGIN
#################
class BasePlugin:
    """
    Base Plugin
    """
    name="nonameplugin"
    version="0.0"

    def __init__(self):
        """Init base plugin"""
        self.system=None #Plugin system object when installed
        self.hooks={}
        try:
            self.setup()
        except Exception,e:
            if self.system.showerrors:print e

    def _handle(self, event):
        """Handle events"""
        try:hook=self.hooks[event.name]
        except KeyError:return
        #Execute hook function
        try:hook(**event.args)
        except Exception,e:
            if self.system.showerrors:print e

    def createHook(self,name,function):
        """Create hook for event name"""
        self.hooks[name]=function

#################
# PLUGINSYSTEM
#################
class PluginSystem:
    """
    Plugin system. Only one instance for application.
    """
    def __init__(self):
        self.eventqueue=[]
        self._plugins=[]
        self.showerrors=True

    def installPlugin(self,pluginObject):
        """
        Add plugin to system
        """
        try:
            plugin=pluginObject()
            plugin.system=self
            self._plugins.append(plugin)
        except AttributeError:
            msg="Can't install plugin from %s." % str(pluginObject)
            if self.showerrors:print msg

    def run(self):
        """
        Send events to plugins. This should be called with tick delay
        """
        for nr in xrange(len(self.eventqueue)):
            ev=self.eventqueue.pop(0)
            for plugin in self._plugins:
                plugin._handle(ev)

    def emit(self,event):
        """Emit event"""
        if isinstance(event,Event):
            self.eventqueue.append(event)

    def emit_event(self,eventname,**args):
        """
        Emit event by name and args (object Event will be created)
        """
        event=Event(eventname, **args)
        self.emit(event)
###########
###########
basePluginSystem=PluginSystem()
