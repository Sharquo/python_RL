import libtcodpy as libtcod

from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from input_handlers import handle_keys
from entity import Entity, blocking_entities
from fov_functions import initialize_fov, recompute_fov
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from map_objects.swatch import Swatch
from scheduling_system import TimeSchedule

from render_functions import clear_all, render_all, RenderOrder

def main():
    """
    This is main!
    """
    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 2

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 1

    fighter_component = Fighter(hp=30, defense=2, power=5, speed=2)

    player = Entity(0, 0, '@', Swatch.colors.get('DbSun'), 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]

    schedule = TimeSchedule()

    libtcod.console_set_custom_font(
        'terminal8x8.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

    libtcod.console_init_root(screen_width, screen_height, 'Generic RL', False)

    con = libtcod.console_new(screen_width, screen_height)
    panel = libtcod.console_new(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    for entity in entities:
        schedule.scheduleEvent(entity, entity.actionDelay())

    tick = schedule.nextEvent()

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN   

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, 
                   screen_height, bar_width, panel_height, panel_y, mouse, Swatch.colors)

        fov_recompute = False
        
        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        close = action.get('close') 
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        if move and tick.name == 'Player':
            game_state = GameStates.PLAYERS_TURN
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = blocking_entities(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)

                else:
                    player.move(dx, dy)
                    fov_recompute = True
        
                game_state = GameStates.ENEMY_TURN
                schedule.scheduleEvent(player, player.actionDelay())
                tick = schedule.nextEvent()

        if close:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    schedule.cancelEvent(dead_entity)
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        if tick.ai:
            game_state = GameStates.ENEMY_TURN
            ''' This is looping through every entity in the list of entities and executing their turn but we should just be executing the turn
            for this individual entity '''
            ''' for entity in entities: '''
            entity = tick
                
            if entity.ai:
                enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                for enemy_turn_result in enemy_turn_results:
                    message = enemy_turn_result.get('message')
                    dead_entity = enemy_turn_result.get('dead')                       

                    if message:
                        message_log.add_message(message)

                    if dead_entity:
                        if dead_entity == player:
                            message, game_state = kill_player(dead_entity)
                        else:
                            message = kill_monster(dead_entity)
                            schedule.cancelEvent(dead_entity)

                        message_log.add_message(message)

                        if game_state == GameStates.PLAYER_DEAD:
                            break

                if game_state == GameStates.PLAYER_DEAD:
                    break

                schedule.scheduleEvent(entity, entity.actionDelay())
                tick = schedule.nextEvent()
        else:
            game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()
