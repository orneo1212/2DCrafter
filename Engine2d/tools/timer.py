import time

class Timer:
    def __init__(self):
        self.lasttick=0.0
        self.tickcount=-1

    def tick(self):
        """Tick a timer"""
        self.lasttick=time.time()
        self.tickcount+=1
        if self.tickcount>=65000:self.tickcount=0

    def tickpassed(self,count):
        """Return True every count tick"""
        if self.tickcount%count==0:return True
        else:return False

    def timepassed(self,timepassed):
        if time.time()>self.lasttick+timepassed:
            return True
        else:return False

    def reset(self):
        """reset timer"""
        self.lasttick=0.0
        self.tickcount=0
