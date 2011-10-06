
class Inventory:
    """Inventory. All items are stored by ID only."""
    def __init__(self):
        self.items={} # {ID:count]}

    def additem(self,itemid):
        if itemid in self.items.keys():
            self.items[itemid]+=1
        else:self.items[itemid]=1

    def removeitem(self,itemid):
        if itemid in self.items.keys():
            #if there is a stock
            if self.items[itemid]>1:
                self.items[itemid]-=1
                return 0 # Done
            else:
                self.items.pop(itemid)
                return 0 # Done
        else:return 1 #  Item not in Inventory

    def haveitem(self,itemid):
        """Check if there is a item in inventory"""
        if itemid in self.items.keys():
            return True # have item
        else: return False


