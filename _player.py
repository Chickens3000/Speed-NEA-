from gameobjects import *
import random

class Player:
    def __init__(self, id):
        self.id = id
        self.empty_hand = False
        self.timed_out = False
        self.controls = self.set_controls()
        
        if self.id == 0:
            #Create player 1s piles
            self.hand = [Pile(f"{id}-{i}", 8, ((SCREEN_WIDTH // 2 - 450 - CARD_WIDTH // 2 + 225 * i),(SCREEN_HEIGHT - CARD_HEIGHT - 30))) for i in range(5)]

            self.side_pile = Pile(f"side{id}", 36, (SCREEN_WIDTH // 2 - (450 + CARD_WIDTH // 2), SCREEN_HEIGHT - 2 * CARD_HEIGHT - 2 * 30))

            self.cards = Pile(f"{id}cards", 52, (1300, 800))
            
            #Get p1 keybinds as an attribute 
            self.inputs = [
                self.controls["p1_pile1"], self.controls["p1_pile2"], 
                self.controls["p1_pile3"],self.controls["p1_pile4"], 
                self.controls["p1_pile5"], self.controls["p1_slam1"],
                self.controls["p1_slam2"]
            ]
        else:
            #Create player 2s piles
            self.hand = [Pile(f"{id}-{i}", 8, ((SCREEN_WIDTH // 2 - 450 - CARD_WIDTH // 2 + 225 * i), 10)) for i in range(5)]

            self.side_pile = Pile(f"side{id}", 36, (SCREEN_WIDTH // 2 + (450 - CARD_WIDTH // 2), SCREEN_HEIGHT - 2 * CARD_HEIGHT - 2 * 30))

            self.cards = Pile(f"{id}cards", 52, (1300, -100))
            
            #Get p2 keybinds as an attribute
            self.inputs = [
                self.controls["p2_pile1"], self.controls["p2_pile2"], 
                self.controls["p2_pile3"],self.controls["p2_pile4"], 
                self.controls["p2_pile5"], self.controls["p2_slam1"],
                self.controls["p2_slam2"]
            ]
    
    def set_controls(self):
        """Loads keybinds into dict"""
        controls = {}
        with open("textfiles/controls.txt", 'r') as file:
            for line in file:
                input_key, value = line.strip().split(':', 1)
                controls[input_key.strip()] = value.strip()
        return controls

class Opponent(Player):
    def __init__(self, difficulty):
        #Inherit all player attributes
        super(Opponent, self).__init__(1)
        self.delay = difficulty
    
    def make_move(self, game):
        """
        Determines wether an AI can make a move and makes it
        Priotitises slamming over other moves
        """
        #Checks for slam
        if game.empty_hand(game.players[0]) or game.empty_hand(game.players[1]):
            #Adds inaccuracy to determining the size of pile
            #Inaccuracy in comparison is proportional to the amount of cards in the pile
            bias_0 = random.randint(-(game.center_piles[0].stack_pointer // 7), (game.center_piles[0].stack_pointer // 7))
            bias_1 = random.randint(-(game.center_piles[1].stack_pointer // 7), (game.center_piles[1].stack_pointer // 7))
            
            if game.center_piles[0].stack_pointer + bias_0 < game.center_piles[1].stack_pointer + bias_1:
                game.slam(self, game.center_piles[0])
            else:
                game.slam(self, game.center_piles[1])
            return False
        
        #Makes any available moves with same priority as keyboard inputs
        pile = game.check_for_moves(self)
        if pile:
            game.play_card(pile, self)
    
    def flip(self):
        """Reveals a facedown card in hand"""
        for stack in self.hand:
            topcard = stack._peek()
            if topcard and not topcard.faced_up:
                topcard.faced_up = True
                return True

class AdaptiveOpponent(Opponent):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.round_number = 1

    def edit_delay(self):
        """Changes delay depending on the number of cards the opponent 
        has at the start of the round"""
        self.round_number += 1
        no_cards = self.cards.stack_pointer + 1
        
        print(no_cards)
        if no_cards >= 32:
            self.delay -= 500
        elif no_cards <= 20:
            self.delay += 500
        elif no_cards <= 10:
            self.delay += 800
        
        #Gradually increases delay over time
        self.delay += (100 * (self.round_number // 3))
        
        #Sets a minimum delay of 500
        if self.delay < 500:
            self.delay = 500
        print(self.delay)