import pygame
import Engine
import pygamefrontend
from data import ConfigImages

class ImageLoader:

    def __init__(self):
        self.config=ConfigImages.images
        self.loaded={}

        #empty image
        self.ts=pygamefrontend.TILESIZE
        self.empty=pygame.Surface((self.ts, self.ts))

    def loadimages(self):
        """Load all images"""
        for item in self.config.keys():
            self.loadimage(item)
        return self.loaded

    def loadimage(self, name,scale=True):
        """Load image by name"""

        #wrong name
        try:self.config[name]
        except KeyError:return self.empty.copy()
        #check loaded images
        try: return self.loaded[name]
        except KeyError:pass

        #load file
        filename=self.config[name]
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
