#TODO: check for items stackable.
class Inventory:
    """Inventory. All items are stored by ID only."""
    def __init__(self):
        #slot=[itemid,count]
        self.slots=[None]*32 # number of slots in inventory
        self.maxstack=99

    def additem(self,itemid,simulate=False):
        """Add item to inventory"""
        #check inventory capacity
        if self.isfull():return 1 # inventory is full
        #check if there is a slot with item
        for slot in range(len(self.slots)):
            if self.slots[slot]:
                if self.slots[slot][0]==itemid and self.slots[slot][1]<self.maxstack:
                    if not simulate:self.slots[slot][1]+=1
                    return 0 # Done
        #find empty slot and add item
        for slot in range(len(self.slots)):
            if self.slots[slot]==None:
                if not simulate:self.slots[slot]=[itemid,1]
                return 0 # Done

    def getfirstrow(self):
        """Return first 8 slots"""
        if len(self.slots)>=8:return self.slots[:8]
        else:return []

    def getslot(self,slotid):
        """Return slot content or None"""
        if not slotid in range(0,len(self.slots)):return None
        return self.slots[slotid]

    def getslotid(self,itemid):
        """Return first slotid with given itemid"""
        for slot in range(len(self.slots)):
            if self.slots[slot]:
                if self.slots[slot][0]==itemid:return slot
        return 0

    def freeslot(self):
        """Check if there is empty slot"""
        freeslots=self.slots.count(None)
        if freeslots>0:return True
        else:return False

    def isempty(self):
        return self.slots.count(None)==32

    def isfull(self):
        """Is inventory full?"""
        return self.slots.count(None)==0

    def getitems(self):
        """Return items ids in inventory"""
        items=[]
        for slot in range(len(self.slots)):
            if self.slots[slot]:
                for count in range(self.slots[slot][1]):
                    items.append(self.slots[slot][0])
        return items

    def removeitem(self,itemid,simulate=False):
        """remove item from inventory"""
        if not self.haveitem(itemid):return 1 # Item not in inventory
        for slot in range(len(self.slots)):
            if self.slots[slot]:
                if self.slots[slot][0]==itemid:
                    #found item check for last one
                    if self.slots[slot][1]==1:
                        if not simulate:self.slots[slot]=None
                    #item is not last in stock
                    else:
                        if not simulate:self.slots[slot][1]-=1
                    return 0 # Done

    def removeitem_fromslot(self,slotid,itemid):
        """Remove item from given slot. Item must exist in that slot"""
        slot=self.getslot(slotid)
        if not slot:return 1 # cant remove item/ slot empty
        if slot[0]!=itemid:return 2 # Item with given id not in this slot
        #if not last item in stack
        if slot[1]>1:slot[1]-=1
        else:self.slots[slotid]=None # Clear the slot after last item remove

    def haveitem(self,itemid):
        """Check if there is a item in inventory"""
        for slot in range(len(self.slots)):
            if self.slots[slot]:
                if self.slots[slot][0]==itemid:return True
        return False

    def clear(self):
        self.slots=[None]*32


