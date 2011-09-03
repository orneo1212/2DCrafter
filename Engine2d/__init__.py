import map
import player
import tools
import yaml
import random

#Load engine config
try:
    fp=open("engineconfig.yaml", "r")
except IOError, e:
    print "Cannot load config file.", e
    fp=None

#TODO: Defaults config

#yaml load
if fp != None:
    Config=yaml.load(fp)
else:
    #make temp config
    Config={"SS":64}

seed=random.randint(10,65535)