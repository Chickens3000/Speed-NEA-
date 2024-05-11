from _player import *
from _cards import *

import random

class Game():
    def __init__(self,id):
        self.id = id
        self.ready = False
        self.players = [Player(0),Player(1)]
        self.center_piles = [Pile("center1",52),Pile("center2",52)]
    
    def start_game(self):
        deck = Deck("deck",52)
        deck.create_deck()
        random.shuffle(deck.contents)
        self.players[0].cards.push_all(deck.contents[0:26])
        self.players[1].cards.push_all(deck.contents[26:53])


    def start_round(self):
        for player in self.players:
            for i in range(0,5):
                for x in range(5-i):
                   card = player.cards._pop()
                   if card == False:
                       break
                   player.hand[i].push(card)
            player.side_pile.push_all(player.cards.pop_all())