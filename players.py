#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:25:55 2024

@author: Jacob Carruth
"""


import torch
import torch.nn as nn
import random



class Human:
    def get_move(self, game, roll, moves):
        game.render()
        roll_string = str(roll[0]) + ', ' + str(roll[1])
        if game.turn == 1:
            print('White to play ' + roll_string)
        else:
            print('Black to play ' + roll_string)
        txt = input('Select a move:')
        chosen_move = game.parse(txt)
        while chosen_move == None:
            txt = input('Invalid format, try again:')
            chosen_move = game.parse(txt)
        while chosen_move not in moves:
            print('Invalid move, try again')
            chosen_move = game.parse(input('Select a move:'))
        return chosen_move
    
    
    
class Random:
    def get_move(self, game, roll, moves, loud=False):
        return random.choice(moves)
    
    
    
class TDGammon(nn.Module):
    def __init__(self, num_nodes=50, file_path = "TDGammon.pt"):
        super(TDGammon, self).__init__()
        self.layer1 = nn.Linear(198, num_nodes)
        self.sigmoid = nn.Sigmoid()
        self.layer2 = nn.Linear(num_nodes, 1)
        self.sigmoid = nn.Sigmoid()
        if file_path != None:
            self.load_state_dict(torch.load(file_path, weights_only=True))
        
        
    
    def forward(self, x):
        x = self.layer1(x)
        x = self.sigmoid(x)
        x = self.layer2(x)
        x = self.sigmoid(x)
        return x
    
    
    def init_es(self):
        self.es = [torch.zeros(weights.shape, requires_grad = False) for weights in self.parameters()]
        
        
    def set_opt_params(self, alpha, lam):
        self.alpha = alpha
        self.lam = lam
    
    
    def update_weights(self, V_current, V_next):
        self.zero_grad()
        V_current.backward()
        
        with torch.no_grad():
            for i, weight in enumerate(self.parameters()):
                self.es[i] = self.lam * self.es[i] + weight.grad
                new_weight = weight + self.alpha*(V_next - V_current)*self.es[i]
                weight.copy_(new_weight)
                
                
    def get_move(self, game, roll, moves):
        with torch.no_grad():
            if game.turn == 1:
                states = torch.zeros([len(moves), 198])
                for i, move in enumerate(moves):
                    hits = game.update(move, new_turn=True)
                    states[i, :] = torch.from_numpy(game.get_state())
                    game.reverse_update(move, hits, new_turn=True)
                probs = self.forward(states)
                best_move = moves[torch.argmax(probs)]
                return best_move
            else:
                states = torch.zeros([len(moves), 198])
                for i, move in enumerate(moves):
                    hits = game.update(move, new_turn=True)
                    states[i, :] = torch.from_numpy(game.get_state())
                    game.reverse_update(move, hits, new_turn=True)
                probs = self.forward(states)
                best_move = moves[torch.argmin(probs)]
                return best_move
            
            

            
            
        
    
class pubeval:
    def get_move(self, game, roll, moves):
        max_score = - float('inf')
        for move in moves:
            hits = game.update(move, new_turn=True)
            score = game.pubeval_score()
            game.reverse_update(move, hits, new_turn=True)
            if score > max_score:
                max_score = score
                best_move = move
        return best_move
        
    
    
    
    
    
    