from _player import *
from _cards import *

import random

class Game():
    def __init__(self,id):
        self.id = id
        self.ready = False
        self.players = [Player(0),Player(1)]
        self.center_piles = [Pile("center1",52),Pile("center2",52)]
        self.online = False
    
    def start_game(self,deck):
        deck.create_deck()
        random.shuffle(deck.contents)
        self.players[0].cards.push_all(deck.contents[0:26])
        self.players[1].cards.push_all(deck.contents[26:53])


    def round_setup(self):
        for player in self.players:
            for i in range(0,5):
                for x in range(5-i):
                   card = player.cards._pop()
                   if card == False:
                       break
                   player.hand[i].push(card)
            cards = player.cards.pop_all()    
            player.side_pile.push_all(cards)

    def move_card(self,_from:Pile,_to:Pile): #Subroutine added to make animation easier
        _to.push(_from._pop())

    def flip_cards(self):
        self.move_card(self.players[0].side_pile,self.center_piles[0])
        self.move_card(self.players[1].side_pile,self.center_piles[1])

    def end_round(self): # Assuming slammed pile has allready been added to cards
        for player in self.players:
            player.cards.push_all(player.side_pile.pop_all())
            for stack in player.hand:
                player.cards.push_all(stack.pop_all())

    def play(self,p,data):
        self.players[p].inputs.Enqueue(data)
        print(self.players[p].inputs.Contents)