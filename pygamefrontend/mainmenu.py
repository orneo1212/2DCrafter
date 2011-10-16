import pygamefrontend

class MainMenu:
    def __init__(self):
        #new game button
        self.ngbtn=pygamefrontend.gui.Button("New Game",(100,100))
        self.qbtn=pygamefrontend.gui.Button("Quit",(100,200))

    def redraw(self,surface):
        self.ngbtn.draw(surface)
        self.qbtn.draw(surface)

    def events(self,event):
        self.ngbtn.events(event)
        self.qbtn.events(event)
