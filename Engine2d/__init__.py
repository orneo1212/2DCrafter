import yaml
import random

import environment
import crafting
import map
import player
import tools
import ui
import dataobj

#Main path
mainpath=""

#Load engine config
try:
    fp=open("data/engineconfig.yaml", "r")
except IOError, e:
    print "Cannot load config file.", e
    fp=None

#TODO: Defaults config

#yaml load
if fp != None:
    Config=yaml.load(fp)
else:
    #make temp config
    Config={"SS":32,seed:0}

#update seed
import time
if Config["seed"]==0:Config["seed"]=int(time.time())

#blocks
blocks=yaml.load(open("data/blocks.yaml"))
#Recipes
recipes=yaml.load(open("data/recipes.yaml"))

seed=Config['seed']
