#!/usr/bin/python
#Copyright (C) <2011>  <Marcin Swierczynski> <orneo1212@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import pygame
import sys
import os

import pygamefrontend
from pygamefrontend import mainmenu
import Engine2d as engine

pygame.init()
pygame.key.set_repeat(100, 100)

#set main path
mainpath=os.path.dirname(__file__)
engine.mainpath=mainpath

SW, SH=pygamefrontend.SW, pygamefrontend.SH

class MainApp:
    def __init__(self):
        #init application
        self.screen=pygame.display.set_mode((SW, SH),\
            pygame.DOUBLEBUF&pygame.HWSURFACE&pygame.HWACCEL)
        pygame.display.set_caption("2DCrafter")
        #Set mainmenu as current page
        pygamefrontend.CURRPAGE=mainmenu.MainMenu(self.screen)
        self.gametimer=pygame.time.Clock()

    def mainloop(self):
        while pygamefrontend.CURRPAGE:
                self.gametimer.tick(engine.Config["maxfps"])
                pygamefrontend.CURRPAGE.events()
                pygamefrontend.CURRPAGE.update()
                pygamefrontend.CURRPAGE.redraw(self.screen)
                #redraw screen
                pygame.display.flip()

if __name__=="__main__":
    m=MainApp()
    m.mainloop()
