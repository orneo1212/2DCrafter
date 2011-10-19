import random

import environment
import crafting
import map
import player
import tools
import ui

#Main paths
mainpath=""
worldsdir=""

#Default config
Config={
    "SS":32,
    "seed":0,
    "maxfps":30,
    "circlelight":True
    }

#update seed
import time
if Config["seed"]==0:Config["seed"]=int(time.time())

from data import ConfigBlocks, ConfigRecipes
#blocks
blocks=ConfigBlocks.blocks
#Recipes
recipes=ConfigRecipes.recipes

seed=Config['seed']
