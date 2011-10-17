import pygame
import yaml
import Engine2d as engine
import pygamefrontend

class ImageLoader(engine.dataobj.DataLoader):

    def __init__(self,filename):
        engine.dataobj.DataLoader.__init__(self,filename)
        self.config={}
        self.loaded={}

        #empty image
        self.ts=pygamefrontend.TILESIZE
        self.empty=pygame.Surface((self.ts, self.ts))
        #load config
        self.loadconfig()

    def loadconfig(self):
        """Load config file (YAML file)"""
        try:
            conf=open(self.filename)
            self.config=yaml.load(conf.read())

        except Exception, e:
            print e
            self.config={}
            return

    def loadimages(self):
        """Load all images"""
        for item in self.config["images"].keys():
            self.loadimage(item)
        return self.loaded

    def loadimage(self, name,scale=True):
        """Load image by name"""

        #check images option in yaml loaded
        if 'images' not in self.config.keys():
            print "Wrong config file for images. There no 'images' section"
            return self.empty.copy()
        #wrong name
        try:self.config['images'][name]
        except KeyError:return self.empty.copy()
        #check loaded images
        try: return self.loaded[name]
        except KeyError:pass

        #load file
        filename=self.config['images'][name]
        try:
            #return scaled image
            img=pygame.image.load(filename)
            img.set_colorkey((255, 0, 255))
            img=img.convert_alpha()
        except Exception, e:
            print e
            img=self.empty.copy()
        self.loaded[name]=img
        return img
