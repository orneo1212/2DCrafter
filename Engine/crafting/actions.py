import Engine

def craft(player,recipename):
    """Do player craft"""
    if Engine.crafting.checkrecipemet(recipename,\
        player.inventory.getitems()):
        #can craft
        recipe=Engine.crafting.getrecipe(recipename)
        #simulate add result
        for cc in range(recipe["count"]):
            err=player.inventory.additem(recipe["result"],True)
            if err:break
        if err:return 1 # cannot craft
        else:
            #real add items
            for cc in range(recipe["count"]):
                err=player.inventory.additem(recipe["result"])
            #remove items
            for item in recipe["req"]:
                player.inventory.removeitem(item)
        return 0 # Done
    else:return 1 # cannot craft
