class Daytime:
    def __init__(self):
        self.daylength=40*60 # day+night length in secs
        self.daytime=self.daylength*0.1# time in secs
        self.lightlevel=255 # light level 0-255
        #time to change from day to night
        #sunset sunrise take 10% of time
        self.daydelta=255.0/(self.daylength*0.1)
        self.daystate="Day"

    def getlightlevel(self):
        """Return current light level 0-255"""
        #avoid wrong lightlevel
        self.lightlevel=max(0,self.lightlevel)
        self.lightlevel=min(self.lightlevel,230)
        return self.lightlevel

    def updatedaytime(self):
        """Update daytime cycle should be called in each sec"""
        self.daytime+=1

        #time tu sunrise or sunset
        dd=(self.daylength*0.1)

        #sunrise
        if self.daytime<=dd:
            self.lightlevel=255-self.daydelta*self.daytime
            self.daystate="Sunrise"
        #day
        if self.daytime>=dd and self.daytime<self.daylength/2:
            self.lightlevel=0
            self.daystate="Day"
        #sunset
        if self.daytime>=self.daylength/2:
            lightdelta=self.daytime-self.daylength/2
            self.lightlevel=self.daydelta*lightdelta
            self.daystate="Sunset"
        #night
        if self.daytime>=self.daylength/2+dd:
            self.lightlevel=255
            self.daystate="Night"

        #limit
        if self.daytime>self.daylength:self.daytime=0
        if self.daytime<0:self.daytime=self.daylength

#Global object
DAYTIME=Daytime()
