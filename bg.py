#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:55:52 2024

@author: Jacob Carruth
"""


from operator import itemgetter
import numpy as np


# get pubeval weights
cntc_str = open("wt_cntc.txt", 'r').read().split()
weights_cntc = [float(s) for s in cntc_str]
race_str = open("wt_race.txt", 'r').read().split()
weights_race = [float(s) for s in race_str]



class game:
    def __init__(self):
        self.in_progress = True
        # turn is 1 for white's turn and -1 for black's
        self.turn  = 1
        # checkers on bar. 0-index is white, 1-index is black
        self.bar = [0, 0]
        # checkers beared off. 0-index is white, 1-index is black.
        self.off = [0, 0]
        # black is negative, white is positive
        self.point_counts = [0]*24
        self.point_counts[0] = 2
        self.point_counts[5] = -5
        self.point_counts[7] = -3
        self.point_counts[11] = 5
        self.point_counts[12] = -5
        self.point_counts[16] = 3
        self.point_counts[18] = 5
        self.point_counts[23] = -2

        
        
    def render(self):
        state = "\nOFF | 23 22 21 20 19 18 BAR 17 16 15 14 13 12\n"
        # Top 4 rows
        for k in range(1, 5):
            if k == 1:
                if self.off[0] < 10:
                    state += "W " + str(self.off[0]) + " | "
                elif self.off[0] >= 10:
                    state += "W" + str(self.off[0]) + " | "
            else:
                state += "    | "
            for j in range(23, 11, -1):
                if self.point_counts[j] >= k:
                    state += "W  "
                elif self.point_counts[j] <= -k:
                    state += "B  "
                else:
                    state += ".  "
                if j == 18:
                    if k == 1:
                        if self.bar[0] > 0 and self.bar[0] < 10:
                            state += "W " + str(self.bar[0]) + "  "
                        elif self.bar[0] > 10:
                            state += "W" + str(self.bar[0])
                        else:
                            state += " |   "
                    else:
                        state += " |   "
            state += "\n"
        # Last row of top half of board
        state += "    | "
        for j in range(23, 11, -1):
            if self.point_counts[j] == 5:
                state += "W  "
            elif self.point_counts[j] > 5 and self.point_counts[j] < 10:
                state += str(self.point_counts[j]) + "  "
            elif self.point_counts[j] >= 10:
                state += str(self.point_counts[j]) + " "
            elif self.point_counts[j] == -5:
                state += "B  "
            elif self.point_counts[j] < -5 and self.point_counts[j] > -10:
                state += str(-self.point_counts[j]) + "  "
            elif self.point_counts[j] <= -10:
                state += str(-self.point_counts[j]) + " "
            else:
                state += ".  "
            if j == 18:
                state += " |   "
        state += "\n--- | ---------------------------------------\n"
        # Top row of bottom half of board
        state += "    | "
        for j in range(12):
            if self.point_counts[j] == 5:
                state += "W  "
            elif self.point_counts[j] > 5 and self.point_counts[j] < 10:
                state += str(self.point_counts[j]) + "  "
            elif self.point_counts[j] >= 10:
                state += str(self.point_counts[j]) + " "
            elif self.point_counts[j] == -5:
                state += "B  "
            elif self.point_counts[j] < -5 and self.point_counts[j] > -10:
                state += str(-self.point_counts[j]) + "  "
            elif self.point_counts[j] <= -10:
                state += str(-self.point_counts[j]) + " "
            else:
                state += ".  "
            if j == 5:
                state += " |   "
        state += "\n"
        # Bottom 4 rows
        for k in range(4, 0, -1):
            if k == 1:
                if self.off[1] < 10:
                    state += "B " + str(self.off[1]) + " | "
                elif self.off[1] >= 10:
                    state += "B" + str(self.off[1]) + " | "
            else:
                state += "    | "
            for j in range(12):
                if self.point_counts[j] >= k:
                    state += "W  "
                elif self.point_counts[j] <= -k:
                    state += "B  "
                else:
                    state += ".  "
                if j == 5:
                    if k == 1:
                        if self.bar[1] > 0 and self.bar[1] < 10:
                            state += "B " + str(self.bar[1]) + "  "
                        elif self.bar[1] > 10:
                            state += "B" + str(self.bar[1])
                        else:
                            state += " |   "
                    else:
                        state += " |   "
            state += "\n"
        state += "OFF | 0  1  2  3  4  5  BAR  6  7  8  9 10 11"
        print(state)
        
        
    def turn_index(self):
        """
        Returns 0 if it's White's turn and 1 if it's Black's turn.
        """
        if self.turn == 1:
            return 0
        else:
            return 1

    
    
    def op_turn_index(self):
        """
        Returns 1 if it's White's turn and 0 if it's Black's turn.
        """
        if self.turn == 1:
            return 1
        else:
            return 0

    
    def canonicalize(self, move):
        if self.turn == 1:
            off_movs = sorted([mov for mov in move if mov[1] == 'OFF'], key=itemgetter(0))
            bar_movs = sorted([mov for mov in move if mov[0] == 'BAR'], key=itemgetter(1))
            int_movs = sorted([mov for mov in move if mov not in (off_movs + bar_movs)], key=itemgetter(0,1))
            s_move = bar_movs + int_movs + off_movs
        else:
            off_movs = sorted([mov for mov in move if mov[1] == 'OFF'], key=itemgetter(0), reverse=True)
            bar_movs = sorted([mov for mov in move if mov[0] == 'BAR'], key=itemgetter(1), reverse=True)
            int_movs = sorted([mov for mov in move if mov not in (off_movs + bar_movs)], key=itemgetter(0,1), reverse=True)
            s_move = bar_movs + int_movs + off_movs
        return s_move
    
    
    def parse(self, raw_move):
        l = raw_move.split(",")
        if len(l) % 2 == 1:
            return None
        valid = [str(i) for i in range(24)]
        valid.extend(['OFF','BAR'])
        for entry in l:
            if entry not in valid:
                return None
        move = []
        for k in range(0, len(l), 2):
            if l[k] == 'BAR':
                move.append((l[k], int(l[k+1])))
            elif l[k+1]  == 'OFF':
                move.append((int(l[k]), l[k+1]))
            else:
                move.append((int(l[k]), int(l[k+1])))
        return self.canonicalize(move)
        
        
    def update(self, move, new_turn=False):
        # Move is a list of between zero and 4 2-tuples of the form
        # (initial position, final position)
        #hits = np.zeros(24)
        hits = set()
        for mov in move:
            # Bearing off
            if mov[1] == 'OFF':
                self.point_counts[mov[0]] -= self.turn
                self.off[self.turn_index()] += 1
            else:
                # Check for hit
                if self.point_counts[mov[1]] == -self.turn:
                    #hits[mov[1]] = 1
                    hits.add(mov[1])
                    self.bar[self.op_turn_index()] += 1
                    self.point_counts[mov[1]] = 0
                # Move in from bar
                if mov[0] == 'BAR':
                    self.bar[self.turn_index()] -= 1
                    self.point_counts[mov[1]] += self.turn
                # normal move
                else:
                    self.point_counts[mov[1]] += self.turn
                    self.point_counts[mov[0]] -= self.turn
        # Is game over?
        if self.off[0] == 15 or self.off[1] == 15:
            self.in_progress = False
        elif new_turn:
            self.turn *= -1
        return hits
        
                
            
            
    def reverse_update(self, move, hits, new_turn=False):
        if self.in_progress == False:
            self.in_progress = True
        elif new_turn:
            self.turn *= -1
        for mov in reversed(move):
            # Bearing off
            if mov[1] == 'OFF':
                self.off[self.turn_index()] -= 1
                self.point_counts[mov[0]] += self.turn
            else:
                # Return to bar
                if mov[0] == 'BAR':
                    self.bar[self.turn_index()] += 1
                    self.point_counts[mov[1]] -= self.turn
                # Normal move
                else:
                    self.point_counts[mov[1]] -= self.turn
                    self.point_counts[mov[0]] += self.turn
        # Reverse hits
        for j in hits:
            self.point_counts[j] -= self.turn
            self.bar[self.op_turn_index()] -= 1

        
                
            
            
            
    def blocked(self):
        if self.turn == 1:
            return [i for i in range(0, 24) if self.turn * self.point_counts[i] < -1]
        else:
            return [i for i in range(23, -1, -1) if self.turn * self.point_counts[i] < -1]
        
        
    def active(self, start_index=None):
        if start_index == None:
            if self.turn == 1:
                start_index = 0
            else:
                start_index = 23
        if self.turn == 1:
            return [i for i in range(start_index, 24) if self.turn * self.point_counts[i] > 0]
        else:
            return [i for i in range(start_index, -1, -1) if self.turn * self.point_counts[i] > 0]

    
    def enter_from_bar(self, die):
        if self.turn == 1:
            return die - 1
        else:
            return 24 - die
        
        
    def advance(self, current_position, die):
        if self.turn == 1:
            return current_position + die
        else:
            return current_position - die
        
        
    def bearing_off(self):
        if self.turn == 1:
            back_man = min(self.active())
            if back_man > 17:
                return True
        else:
            back_man = max(self.active())
            if back_man < 6:
                return True
        return False
    
    
    def is_removable(self, j, die):
        if self.turn == 1:
            return (j + die == 24 or (j + die > 24 and j == min(self.active())))
        else:
            return (j - die == -1 or (j - die < -1 and j == max(self.active())))
            
            
            
    def get_moves_doubles(self, roll, start_index=None):
        blocked = self.blocked()
        moves = []
        die = roll[-1]
        # Men on bar
        if self.bar[self.turn_index()] != 0:
            destination = self.enter_from_bar(die)
            if destination not in blocked:
                move = [('BAR', destination), ]
                if len(roll) == 1:
                    moves.append(move)
                else:
                    hits = self.update(move)
                    next_moves = self.get_moves_doubles(roll[:-1])
                    self.reverse_update(move, hits)
                    if len(next_moves) == 0:
                        moves.append(move)
                    else:
                        for next_move in next_moves:
                            moves.append(move + next_move)
        # No men on bar
        else:
            active = self.active(start_index)
            if active == []:
                return []
            bearing_off = self.bearing_off()
            for j in active:
                destination = self.advance(j, die)
                if destination not in blocked and destination < 24 and destination > -1:
                    move = [(j, destination), ]
                    if len(roll) == 1:
                        moves.append(move)
                    else:
                        hits = self.update(move)
                        next_moves = self.get_moves_doubles(roll[:-1], j)
                        self.reverse_update(move, hits)
                        if len(next_moves) == 0:
                            moves.append(move)
                        else:
                            for next_move in next_moves:
                                moves.append(move + next_move)
                if bearing_off and self.is_removable(j, die):
                    move = [(j, 'OFF'), ]
                    if len(roll) == 1:
                        moves.append(move)
                    else:
                        hits = self.update(move)
                        next_moves = self.get_moves_doubles(roll[:-1], j)
                        self.reverse_update(move, hits)
                        if len(next_moves) == 0:
                            moves.append(move)
                        else:
                            for next_move in next_moves:
                                moves.append(move + next_move)
        if len(moves) == 0:
            return []
        else:
            max_len = max([len(move) for move in moves])
            return [move for move in moves if len(move) == max_len]        
        
        
    def std_two_dice_helper(self, main_roll_index, roll):
        blocked = self.blocked()
        active = self.active()
        main_die = roll[main_roll_index]
        other_die = roll[main_roll_index - 1]
        one_die_moves = []
        two_dice_moves = []
        # Man on bar
        if self.bar[self.turn_index()] != 0:
            destination = self.enter_from_bar(main_die)
            if destination not in blocked:
                move = [('BAR', destination), ]
                next_moves = self.next_moves(move, other_die)
                if len(next_moves) == 0:
                    one_die_moves.append(move)
                else:
                    for next_move in next_moves:
                        two_dice_moves.append(move + next_move)
        else:
            bearing_off = self.bearing_off()
            for j in active:
                destination = self.advance(j, main_die)
                # regular move
                if destination not in blocked and destination < 24 and destination > -1:
                    move = [(j, destination), ]
                    next_moves = self.next_moves(move, other_die, j + self.turn*(1 - main_roll_index))
                    if len(next_moves) == 0:
                        one_die_moves.append(move)
                    else:
                        for next_move in next_moves:
                            two_dice_moves.append(move + next_move)
                # bearing off
                if bearing_off and self.is_removable(j, main_die):
                    move = [(j, 'OFF'), ]
                    next_moves = self.next_moves(move, other_die, j + self.turn*(1 - main_roll_index))
                    if len(next_moves) == 0:
                        one_die_moves.append(move)
                    else:
                        for next_move in next_moves:
                            two_dice_moves.append(move + next_move)
        return one_die_moves, two_dice_moves
    
    
    def next_moves(self, move, die, start_index=None):
        hits = self.update(move)
        result = self.std_one_die_helper(die, start_index)
        self.reverse_update(move, hits)
        return result
        
    
    def std_one_die_helper(self, die, start_index=None):
        moves = []
        if not self.in_progress:
            return moves
        active = self.active(start_index)
        blocked = self.blocked()
        # never a man on bar for one die
        for j in active:
            destination = self.advance(j, die)
            if destination not in blocked and destination < 24 and destination > -1:
                move = [(j, destination), ]
                moves.append(move)
            if self.bearing_off() and self.is_removable(j, die):
                move = [(j, 'OFF'), ]
                moves.append(move)
        return moves
    
    
    def loaded_bar(self, roll):
        destinations = [self.enter_from_bar(roll[1]), self.enter_from_bar(roll[0])]
        blocked = self.blocked()
        moves = []
        for destination in destinations:
            if destination not in blocked:
                moves.append(('BAR', destination),)
        return [moves]
    
    
    def get_moves_std(self, roll):
        # check if game over
        if not self.in_progress:
            return []
        # 2 or more men on bar
        if self.bar[self.turn_index()] >= 2:
            return self.loaded_bar(roll)
        # check larger die first
        high_die_moves, moves = self.std_two_dice_helper(1, roll)
        # check if forced to remove pieces
        if len(moves) == 0 and len(high_die_moves) == 1 and high_die_moves[0][0][1] == 'OFF':
            return high_die_moves
        elif len(moves) == 1 and moves[0][0][1] == 'OFF' and moves[0][1][1] == 'OFF':
            return moves
        # check smaller die
        low_die_moves, new_moves = self.std_two_dice_helper(0, roll)
        moves = moves + new_moves
        # if there exist 2 die moves
        if len(moves) > 0:
            return moves
        elif len(high_die_moves) > 0:
            return high_die_moves
        else:
            return low_die_moves

        
        
    def available_moves(self, roll):
        # Doubles
        if (roll[0] == roll[1]):
            if roll[0] == roll[1]:
                roll = [roll[0]]*4
            moves = self.get_moves_doubles(roll)
        else:
        # Not doubles
            roll.sort()
            moves = self.get_moves_std(roll)
        #c_moves = [self.canonicalize(move) for move in moves]
        c_moves = []
        for move in moves:
            if isinstance(move, tuple):
                print(move)
            c_moves.append(self.canonicalize(move))
        return c_moves
            


                        
                
    def get_state(self):
        state = np.zeros(198, dtype=np.float32)
        for i in range(24):
            count = self.point_counts[i]
            ind = 8*i
            if count == 1:
                state[ind] = 1
            elif count == 2:
                state[ind + 1] = 1
            elif count == 3:
                state[ind + 2] = 1
            elif count > 3:
                state[ind + 3] = count / 2
            elif count == -1:
                state[ind + 4] = 1
            elif count == -2:
                state[ind + 5] = 1
            elif count == -3:
                state[ind + 6] = 1
            elif count < -3:
                state[ind + 7] = abs(count) / 2
        if self.turn == 1:
            state[192] = 1
        else:
            state[193] = 1
        state[194] = self.bar[0] / 2
        state[195] = self.bar[1] / 2
        state[196] = self.off[0] / 15
        state[197] = self.off[1] / 15
        return state
    
    
    def get_state_w_race(self):
        state = np.zeros(199, dtype=np.float32)
        state[:-1] = self.get_state()
        state[-1] = self.is_race()
        return state
    
    
    def get_pubeval_state(self):
        state = np.zeros(122, dtype = np.float32)
        # when pubeval plays as Black
        if self.turn == 1:
            for j in range(24):
                n = self.point_counts[23 - j]
                if n != 0:
                    if n == 1:
                        state[5*j] = 1
                    if n == -1:
                        state[5*j + 1] = 1
                    if n <= -2:
                        state[5*j + 2] = 1
                    if n == -3:
                        state[5*j + 3] = 1
                    if n <= -4:
                        state[5*j + 4] = (abs(n) - 3) / 2
            state[120] = self.bar[0] / 2
            state[121] = self.off[1] / 15
        # when pubeval plays as White
        else:
            for j in range(24):
                n = self.point_counts[j]
                if n != 0:
                    if n == -1:
                        state[5*j] = 1
                    if n == 1:
                        state[5*j + 1] = 1
                    if n >= 2:
                        state[5*j + 2] = 1
                    if n == 3:
                        state[5*j + 3] = 1
                    if n >= 4:
                        state[5*j + 4] = (abs(n) - 3) / 2
            state[120] = self.bar[1] / 2
            state[121] = self.off[0] / 15
        return state
    
    
    def is_race(self):
        # Missing case of men on bar, no men in play
        active_black = [i for i in range(24) if self.point_counts[i] < 0]
        active_white = [i for i in range(24) if self.point_counts[i] > 0]
        if len(active_black) != 0 and len(active_white) != 0:
            if max(active_black) < min(active_white):
                return 1
            else:
                return 0
        else:
            return 0
        
        
    def pubeval_score(self):
        if not self.in_progress:
            return float('inf')
        race = self.is_race()
        state = self.get_pubeval_state()
        if race:
            return np.dot(weights_race, state)
        else:
            return np.dot(weights_cntc, state)
        

                

