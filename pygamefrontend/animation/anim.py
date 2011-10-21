import time

class AnimatedSprite:
    def __init__(self, image):
        self.image=image
        self.current_frame=0
        self.image_size=image.get_size()
        self.framewidth=32 # 32 pixels width frame
        self.noframes=self.image_size[0]/self.framewidth # number of frames
        self.started=False
        self.animlist=list(range(0,self.noframes)) # List of frames for animation
        #times
        self.starttime=0.0
        self.lastupdate=0.0
        self.animation_delay=100 # in milisecs
        #

    def set_animlist(self,newanimlist):
        """Set new animation list"""
        self.animlist=newanimlist

    def set_default_animlist(self):
        """Set default animation list"""
        self.animlist=list(range(0,self.noframes))

    def _updaterange(self):
        """Update range of frames to avoid get non existing frame"""
        if self.current_frame>len(self.animlist)-1:self.current_frame=0
        if self.current_frame<0:self.current_frame=len(self.animlist)-1

    def get_current_frame(self):
        """Return current frame"""
        self._updaterange()
        return self.get_frame(self.current_frame)

    def set_delay(self,delay):
        """Set animation delay (in milisecs)"""
        self.animation_delay=delay

    def get_frame(self,frameindex):
        """Return frame frameindex"""
        if frameindex>len(self.animlist)-1:frameindex=0
        if frameindex<0:frameindex=len(self.animlist)-1
        px=self.framewidth*frameindex
        py=self.image_size[1]
        pw=self.framewidth
        ph=self.image_size[1]
        return self.image.subsurface((px,0,pw,ph))

    def next(self):
        """Select next frame. Return current frame"""
        self.current_frame+=1
        self._updaterange()
        return self.current_frame

    def prev(self):
        """Select prev frame. Return current frame"""
        self.current_frame-=1
        self._updaterange()
        return self.current_frame

    def start_animation(self):
        """Start animation"""
        self.started=True
        self.starttime=time.time()
        self.lastupdate=time.time()

    def stop_animation(self):
        """Stop animation"""
        self.started=False
        self.starttime=0.0

    def update(self):
        """Update animation state"""
        if not self.started:return
        if time.time()-self.lastupdate>=self.animation_delay/1000.0:
            self.lastupdate=time.time()
            self.next()
