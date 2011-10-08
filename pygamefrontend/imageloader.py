import pygame
import yaml

class ImageLoader:

    def __init__(self):
        self.configfile="images.yaml"
        self.config={}
        self.loaded={}

        #load config
        self.loadconfig()

    def loadconfig(self):
        """Load config file (YAML file)"""
        try:
            conf=open(self.configfile)
        except IOError,e:
            print e
            self.config={}
            return
        #load data
        try:
            self.config=yaml.load(conf.read())
        except Exception,e:
            print e
            self.config={}
            return

    def loadimage(self,name):
        """Load image by name"""
        #check images option in yaml loaded
        if 'images' not in self.config.keys():
            print "Wrong config file for images. There no 'images' section"
            return pygame.Surface((32,32))
        #wrong name
        if name not in self.config['images'].keys():
            return pygame.Surface((32,32))
        #check loaded images
        if name in self.loaded.keys():
            return self.loaded[name]
        #load file
        filename=self.config['images'][name]
        try:
            img=pygame.image.load(filename)
            img.set_colorkey((255,0,255))
            img=img.convert_alpha()
        except Exception,e:
            print e
            img=pygame.Surface((32,32))
        self.loaded[name]=img
        return img
