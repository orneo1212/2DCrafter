from pygamefrontend import imageloader, mapviewer
import Engine2d as engine
import pygame
from pgu import gui

"""GameGUI page"""
class GameGUI:
    def __init__(self, screen):
        self.screen=screen

        self.pguapp=gui.App()
        self.c = gui.Container(align=-1,valign=-1)
        label=gui.Label("2D Building Game",color=(255,255,255))
        self.button=gui.Button("Menu")
        self.c.add(label,0,0)
        self.c.add(self.button,0,450)
        self.pguapp.init(self.c)

    def update(self):
        pass

    def events(self,event):
        self.pguapp.app.event(event)

    def redraw(self):
        self.pguapp.paint()
