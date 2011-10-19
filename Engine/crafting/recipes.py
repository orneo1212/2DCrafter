import Engine

def getrecipesnames():
    """Return recipes names"""
    return Engine.recipes.keys()

def getrecipe(name):
    """get recipe data"""
    if name in getrecipesnames():
        return Engine.recipes[name]
    return False

def checkrecipemet(recipename,items):
    """check recipe dependencies met. Return True/False"""
    recipedata=getrecipe(recipename)
    items=items[:]

    if not recipedata:return False

    for itemid in recipedata["req"]:
        if itemid not in items:return False
        else:items.remove(itemid)
    return True

def getpossiblerecipes(items):
    """Return list of possible recipes names"""
    result=[]
    for recipename in getrecipesnames():
        if checkrecipemet(recipename,items):result.append(recipename)
    return result
