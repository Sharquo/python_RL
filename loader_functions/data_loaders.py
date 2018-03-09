import os

import shelve

def save_game(player, entities, game_map, message_log, game_state, tick, schedule):
    with shelve.open('savegame.dat', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        data_file['tick'] = tick
        data_file['schedule'] = schedule

def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame.dat', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        tick = data_file['tick']
        schedule = data_file['schedule']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state, tick, schedule