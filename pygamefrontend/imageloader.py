import pygame
import yaml
import Engine2d as engine

from pygamefrontend import mapviewer

class ImageLoader(engine.dataobj.DataLoader):

    def __init__(self,filename):
        engine.dataobj.DataLoader.__init__(self,filename)
        self.config={}
        self.loaded={}

        #load config
        self.loadconfig()

    def loadconfig(self):
        """Load config file (YAML file)"""
        try:
            conf=open(self.filename)
        except IOError, e:
            print e
            self.config={"smoothscale":True}
            return
        #load data
        try:
            self.config=yaml.load(conf.read())
        except Exception, e:
            print e
            self.config={}
            return

    def loadimage(self, name):
        """Load image by name"""
        empty=pygame.Surface((mapviewer.TILESIZE, mapviewer.TILESIZE))
        #check images option in yaml loaded
        if 'images' not in self.config.keys():
            print "Wrong config file for images. There no 'images' section"
            return empty.copy()
        #wrong name
        if name not in self.config['images'].keys():
            return empty.copy()
        #check loaded images
        if name in self.loaded.keys():
            return self.loaded[name]
        #load file
        filename=self.config['images'][name]
        try:
            #return scaled image
            img=pygame.image.load(filename)
            img.set_colorkey((255, 0, 255))
            img=img.convert_alpha()
            if self.config["smoothscale"]:
                img=pygame.transform.smoothscale(img, (mapviewer.TILESIZE, \
                    mapviewer.TILESIZE))
            else:
                img=pygame.transform.scale(img, (mapviewer.TILESIZE, \
                    mapviewer.TILESIZE))
        except Exception, e:
            print e
            img=empty.copy()
        self.loaded[name]=img
        return img
