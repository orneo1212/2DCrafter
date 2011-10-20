
class AnimatedSprite:
    def __init__(self, image):
        self.image=image
        self.current_frame=0
        self.image_size=image.get_size()
        self.framewidth=32 # 32 pixels width frame
        self.noframes=self.image_size[0]/self.framewidth # number of frames

    def _updaterange(self):
        """Update range of frames to avoid get non existing frame"""
        if self.current_frame>self.noframes:self.current_frame=0
        if self.current_frame<0:self.current_frame=self.noframes

    def get_current_frame(self):
        """Return current frame"""
        self._updaterange()
        return self.get_frame(self.current_frame)

    def get_frame(self,frameindex):
        """Return frame frameindex"""
        if frameindex>self.noframes:frameindex=0
        if frameindex<0:frameindex=self.noframes
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
