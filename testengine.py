import Engine2d as engine

def showsector(tmap):
    for yy in range(engine.Config['SS']):
        for xx in range(engine.Config['SS']):
            print tmap.getblock((xx, 10+yy, 0)).id,
        print

map=engine.map.loadmap("world")
player=engine.player.Player("test")
map.addentity(player)

#map.render() # TODO: map renderer

player.move("n", 0.3)
print map.getsector([0, 0, 0])
map.setblock([100, 100, 0], None)
showsector(map)