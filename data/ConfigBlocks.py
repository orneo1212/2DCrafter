blocks={}
blocks[0]={
    "name": "",
    "blocked": False,
    }

blocks[1]={
    "name": "Stone",
    "blocked": True,
    "mineitems": [17],
    }

blocks[2]={
    "name": "Mud",
    "blocked": False,
    "ongrow": 9,
}

blocks[3]={
    "name": "Water",
    "blocked": False,
    "obstacle": False,
}

blocks[4]={
    "name": "Sand",
    "blocked": False,
}

blocks[5]={
    "name": "Lava",
    "blocked": False,
    "obstacle": False,
    "lightradius": 6,
}

blocks[6]={
    "name": "Brick",
    "blocked": True,
}

blocks[7]={
    "name": "Tree",
    "blocked": True,
    "mineitems": [20,20,10,10,10,10],
}

blocks[8]={
    "name": "Torch",
    "blocked": False,
    "lightradius": 4,
    "item": True,
}

blocks[9]={
    "name": "Grass",
    "blocked": False,
    "mineitems": [2],
}

blocks[10]={
    "name": "Wood",
    "blocked": False,
}

blocks[11]={
    "name": "Stone Gate",
    "blocked": True,
    "mineitems": [11],
    "onput": 12,
}

blocks[12]={
    "name": "Stone Gate",
    "blocked": False,
    "mineitems": [11],
    "onput": 11,
}

blocks[13]={
    "name": "Coal Ore",
    "blocked": True,
}

blocks[14]={
    "name": "Iron Ore",
    "blocked": True,
}

blocks[15]={
    "name": "Stick",
    "blocked": False,
    "item": True,
}

blocks[16]={
    "name": "Gravel",
    "blocked": False,
}

blocks[17]={
    "name": "Cobblestone",
    "blocked": True,
}

blocks[18]={
    "name": "Chest",
    "blocked": True,
    "unique": True,
    "onputcall": "OpenChest",
    "item": True,
}

blocks[19]={
    "name": "Stone lamp",
    "blocked": True,
    "lightradius": 4,
}

blocks[20]={
    "name": "Sapling",
    "blocked": False,
    "ongrow": 7,
    "growtime": 600,
}

blocks[21]={
    "name": "Black marble",
    "blocked": False,
}

blocks[22]={
    "name": "Downstairs",
    "blocked": False,
    "onputcall": "MoveDown",
    "onminecall": "MineDownStairs",
    "onputemptycall": "PutDownstairs",
    "mineitems": [None],
}

blocks[23]={
    "name": "Upstairs",
    "blocked": False,
    "onputcall": "MoveUp",
    "onminecall": "MineUpstairs",
    "onputemptycall": "PutUpstairs",
    "mineitems": [None],
}
