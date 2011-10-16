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
        self.screen=pygame.display.set_mode((SW, SH), pygame.DOUBLEBUF)
        pygame.display.set_caption("2DCrafter")
        self.page=mainmenu.MainMenu(self.screen)

    def mainloop(self):
        while 1:
            if self.page:
                self.page.events()
                page=self.page.update()
                if page:self.page=page
                self.page.redraw(self.screen)
                #redraw screen
                pygame.display.update()

if __name__=="__main__":
    m=MainApp()
    m.mainloop()
