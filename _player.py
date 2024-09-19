from gameobjects import *
import random
class Player:
    
    def __init__(self,id):
        self.id = id
        self.empty_hand = False
        self.timed_out = False
        self.controls = self.set_controls()
        if self.id == 0:
            self.hand = [Pile(str(id)+"-"+str(i),8,
                              ((SCREEN_WIDTH//2 -450-CARD_WIDTH//2 + 225 * i),
                               (SCREEN_HEIGHT - CARD_HEIGHT - 30))) for i in range(5)] #extra 42 allows far stacked cards and 10 pixel leeway
            self.side_pile = Pile("side"+(str(id)),36,
                                  (SCREEN_WIDTH//2-(450+CARD_WIDTH//2),
                                  (SCREEN_HEIGHT - 2* CARD_HEIGHT - 2* 30)))
            
            self.cards = Pile(str(id)+"cards",52,(1300,800))
            self.inputs = [self.controls["p1_pile1"],self.controls["p1_pile2"],self.controls["p1_pile3"],
                           self.controls["p1_pile4"],self.controls["p1_pile5"],self.controls["p1_slam1"],
                           self.controls["p1_slam2"]]
        else:
            self.hand = [Pile(str(id)+"-"+str(i),8,((SCREEN_WIDTH//2 -450-CARD_WIDTH//2 + 225 * i),10)) for i in range(5)]
            self.side_pile = Pile("side"+(str(id)),36,(SCREEN_WIDTH//2+(450-CARD_WIDTH//2),(SCREEN_HEIGHT - 2* CARD_HEIGHT - 2* 30))) 
            self.cards = Pile(str(id)+"cards",52,(1300,-100))
            self.inputs = [self.controls["p2_pile1"],self.controls["p2_pile2"],self.controls["p2_pile3"],
                           self.controls["p2_pile4"],self.controls["p2_pile5"],self.controls["p2_slam1"],
                           self.controls["p2_slam2"]]

    def set_controls(self):
        controls = {}
        with open("controls.txt",'r') as file:
            for line in file:
                input, value = line.strip().split(':',1)
                controls[input.strip()] = value.strip()
        return controls
        
class Opponent(Player):
    def __init__(self,difficulty):
        super(Opponent,self).__init__(1)
        self.delay = difficulty
        
    def make_move(self,game):
        if game.empty_hand(game.players[0]) == True or game.empty_hand(game.players[1]) == True:
            #Comparison of piles, innacuracy in comparison is proportional to the amount of cards in the pile
            if game.center_piles[0].stack_pointer + random.randint(-(game.center_piles[0].stack_pointer//7),(game.center_piles[0].stack_pointer//7)) < game.center_piles[1].stack_pointer+ random.randint(-(game.center_piles[1].stack_pointer//7),(game.center_piles[1].stack_pointer//7)):
                game.slam(self,game.center_piles[0])
            else:
                 game.slam(self,game.center_piles[1])
            return False
        pile = game.check_for_moves(self)
        if pile != False:
            game.play_card(pile, self)
        
    def flip(self):
        for stack in self.hand:
            topcard = stack._peek()
            if topcard == False:
                continue
            if topcard.faced_up == False:
                topcard.faced_up = True
                return True

class AdaptiveOpponent(Opponent):
    def __init__(self, difficulty):
        super().__init__(difficulty)
        self.round_number = 1

    def edit_delay(self): 
        self.round_number += 1
        no_cards = self.cards.stack_pointer + 1
        if no_cards >= 32:
            self.delay -= 500
        elif no_cards <= 20:
            self.delay += 500
        elif no_cards <= 10:
            self.delay -= 1000
            
        self.delay += (100 * (self.round_number // 5))
        if self.delay < 500:
            self.delay = 500

