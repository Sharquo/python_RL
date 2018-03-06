import libtcodpy as libtcod

from game_states import GameStates

def handle_keys(key, game_state):
    if game_state != GameStates.PLAYER_DEAD:
        return handle_player_turn_keys(key)
    else:
        return handle_player_dead_keys(key)

    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # Movement keys
    if key.vk == libtcod.KEY_KP8:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_KP6:
        return {'move': (1, 0)}
    elif key.vk == libtcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key.vk == libtcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key.vk == libtcod.KEY_KP1:
        return {'move': (-1, 1)}
    elif key.vk == libtcod.KEY_KP3:
        return {'move': (1, 1)}

    if key_char == 'g':
        return {'pickup': True}

    elif key_char == 'i':
        return {'show_inventory': True}    

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt + Enter: Toggles the fullscreen.
        return {'fullscren': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game.
        return {'close': True}

    # No key was pressed.
    return {}

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt + Enter: Toggles the fullscreen.
        return {'fullscren': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game.
        return {'close': True}

    # No key was pressed.
    return {}