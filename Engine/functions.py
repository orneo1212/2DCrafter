import Engine

def create_block(blockID):
    """Create block by ID"""
    if blockID==None:return None
    if blockID==1:return None
    return Engine.map.Block(blockID)
