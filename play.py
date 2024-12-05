#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:36:42 2024

@author: Jacob Carruth
"""

import bg
import random
import players


# Choose White player
# Options: Human, TDGammon, pubeval, Random
playerW = players.Human()

# Choose Black player
playerB = players.TDGammon()



current_game = bg.game()
while current_game.in_progress:
    roll = [random.randint(1,6), random.randint(1,6)]
    roll_string = str(roll[0]) + ', ' + str(roll[1])
    moves = current_game.available_moves(roll)
    if len(moves) == 0:
        if isinstance(playerW, players.Human) or isinstance(playerB, players.Human):
            if current_game.turn == 1:
                player_str = "W"
            else:
                player_str = "B"
            current_game.render()
            print(player_str + ' to play ' + roll_string)
            print('No available moves.')
        current_game.turn *= -1
    else:
        if current_game.turn == 1:
            chosen_move = playerW.get_move(current_game, roll, moves)
            if isinstance(playerB, players.Human):
                current_game.render()
                print('W to play ' + roll_string)
                print('W plays ' + str(chosen_move))
        else:
            chosen_move = playerB.get_move(current_game, roll, moves)
            if isinstance(playerW, players.Human):
                current_game.render()
                print('B to play ' + roll_string)
                print('B plays ' + str(chosen_move))
        current_game.update(chosen_move, new_turn=True)


if current_game.turn == 1:
    print('White wins!')
else:
    print('Black wins!')
