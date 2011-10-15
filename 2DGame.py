#!/usr/bin/python
import pygame
import sys
import os

from pygamefrontend import game
import Engine2d as engine

pygame.init()
pygame.key.set_repeat(100, 100)

mainpath=os.path.dirname(__file__)
engine.mainpath=mainpath

if __name__=="__main__":
    game=game.Game()
    game.mainloop()
