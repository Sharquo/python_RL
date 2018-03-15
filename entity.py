import libtcodpy as libtcod
import math

from render_functions import RenderOrder
from scheduling_system import TimeSchedule


class Entity:
    """
    A generic object to represent characters, items, spells, etc.
    """

    # Testing priority with a maximum speed of 10
    base_time = 10.0

    def __init__(self, x, y, group, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, 
                 item=None, inventory=None, stairs=None):
        self.x = x
        self.y = y
        self.group = group
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                blocking_entities(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map.
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable.
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scann all the objects to see if there are objects that must be navigated around.
        # Check also that the object isn't self or the target so that the start and end points are free.
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway.
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a all so it must be navigated around.
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate A* path.
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited.
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates.
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles.
        # The path size matters if you want the monster to use alternative longer paths if for example the player is in a corridor
        # It makes sense to keep the path size relatively low to keep the monsters from runnning around the map if there's an alternative path really far away.

        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path.
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile.
                self.x = x
                self.y = y
            else:
                # Keep the old move function as a backup so that if there are no paths it will still try and move towards the player.
                self.move_towards(target.x, target.y, game_map, entities)

                # Delete the path to free memory.
            libtcod.path_delete(my_path)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def actionDelay(self):
        return Entity.base_time / self.fighter.speed
        
def blocking_entities(self, destination_x, destination_y):
    for entity in self:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None