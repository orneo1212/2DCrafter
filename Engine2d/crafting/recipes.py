import Engine2d as engine

def getrecipe(name):
    """get recipe data"""
    if engine.recipes.has_key(name):
        return engine.recipes[name]
    return False

def getrecipesnames():
    """Return recipes names"""
    return engine.recipes.keys()

def checkrecipemet(recipename,items):
    """check recipe dependencies met. Return True/False"""
    recipedata=getrecipe(recipename)
    if not recipedata:return False
    for itemid in recipedata["req"]:
        if itemid not in items:return False
    return True
