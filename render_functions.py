import libtcodpy as libtcod

from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, bar_width,
               panel_height, panel_y, colors):
    # Draw all the tiles in the game map.
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, '#', colors.get('SecondaryLighter'), colors.get('SecondaryDarker'))
                        #libtcod.console_set_char_background(con, x, y, colors.get('SecondaryLighter'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_put_char_ex(con, x, y, '.', colors.get('Alternate'), colors.get('DbDark'))
                        #libtcod.console_set_char_background(con, x, y, colors.get('Alternate'), libtcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, '#', colors.get('Secondary'), colors.get('SecondaryDarkest'))
                        #libtcod.console_set_char_background(con, x, y, colors.get('Secondary'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_put_char_ex(con, x, y, '.', colors.get('AlternateDarkest'), libtcod.black)
                        #libtcod.console_set_char_background(con, x, y, colors.get('AlternateDarkest'), libtcod.BKGND_SET)

    entity_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entites in the list.
    for entity in entity_render_order:
        draw_entity(con, entity, fov_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, 
               colors.get('Primary'), colors.get('PrimaryDarkest'))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # Erase the character that represents this object.
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
