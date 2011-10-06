
class Inventory:
    def __init__(self):
        self.items={} # {ID:count]}

    def additem(self,item):
        if item.ID in self.items.keys():
            self.items[item.ID]+=1
        else:self.items[item.ID]=1

    def removeitem(self,item):
        if item.ID in self.items.keys():
            #if there is a stock
            if self.items[item.ID]>1:
                self.items[item.ID]-=1
                return 0
            else:
                self.items.remove(item.ID)
                return 0
        else:return 1 #  Item not in Inventory


