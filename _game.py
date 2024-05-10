from _player import *
from _cards import *

import random

class Game():
    def __init__(self,id):
        self.id = id
        self.ready = False
        self.players = [Player(0),Player(1)]
    
    def start_game(self):
        deck = Deck("deck",52)
        deck.create_deck()
        random.shuffle(deck.contents)
        self.players[0].cards = deck.contents[0:27]
        self.players[1].cards = deck.contents[26:53]

    def start_round(self):
        for player in self.players:
            for i in range(5):
                for x in range(5-i):
                   card = player.cards.pop()
                   player.hand[i].push(card)
        print(player.hand[4].contents)