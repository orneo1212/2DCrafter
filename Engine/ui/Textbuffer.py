from pluginsystem import basePluginSystem
import Engine

class TextBuffer:
    def __init__(self):
        self.tbuffer=[]

    def addtext(self, text):
        if len(self.tbuffer)>1024:self.clear()
        self.tbuffer.append(text)
        basePluginSystem.emit_event("messageadded",
            message=text)

    def getlast(self,n=1):
        """get n last texts from buffer"""
        if len(self.tbuffer)<n:n=len(self.tbuffer)
        if n>0:
            messages=self.tbuffer[-n:]
            return messages
        else:return []

    def clear(self):
        self.tbuffer=[]

msgbuffer=TextBuffer()
