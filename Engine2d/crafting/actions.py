import Engine2d as engine

def craft(player,recipename):
    """Do player craft"""
    if engine.crafting.checkrecipemet(recipename,\
        player.inventory.getitems()):
        #can craft
        recipe=engine.crafting.getrecipe(recipename)
        for item in recipe["req"]:
            player.inventory.removeitem(item)
        for cc in range(recipe["count"]):
            player.inventory.additem(recipe["result"])
        return 0 # Done
    else:return 1 # cannot craft
