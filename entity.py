class Entity:
    """
    A generic object to represent characters, items, spells, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy
        
def blocking_entities(self, destination_x, destination_y):
    for entity in self:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None