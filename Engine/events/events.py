class Event:
    type="noevent"

#################################
#      EVENTS DEFINITION        #
#################################
EVENTS=[] # Events queue
def poll():
    """Poll one event from queue"""
    global EVENTS
    if len(EVENTS)==0:return Event() # return noevent event
    return EVENTS.pop(-1)

def clear(type=None):
    """Clear event queue. if type was given only events with that type will be removed"""
    global EVENTS
    if type:
        for event in EVENTS[:]:
            if event.type==type:EVENTS.remove(event)
        return
    EVENTS=[]

def addevent(event):
    """Add event to queue"""
    global EVENTS
    EVENTS.append(event)

def makeevent(eventtype):
    event=Event()
    event.type=eventtype
    return event
