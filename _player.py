from gameobjects import *

class Player:
    
    def __init__(self,id):
        self.id = id
        self.empty_hand = False
        self.timed_out = False
        if self.id == 0:
            self.hand = [Pile(str(id)+"-"+str(i),8,((SCREEN_WIDTH//2 -450-CARD_WIDTH//2 + 225 * i),(SCREEN_HEIGHT - CARD_HEIGHT - 30))) for i in range(5)] #extra 42 allows far stacked cards and 10 pixel leeway
            self.side_pile = Pile("side"+(str(id)),36,(SCREEN_WIDTH//2-(450+CARD_WIDTH//2),(SCREEN_HEIGHT - 2* CARD_HEIGHT - 2* 30)))
            self.cards = Pile(str(id)+"cards",52,(1300,800))
            self.inputs = ["q","w","e","r","g","t","y"]
        else:
            self.hand = [Pile(str(id)+"-"+str(i),8,((SCREEN_WIDTH//2 -450-CARD_WIDTH//2 + 225 * i),10)) for i in range(5)]
            self.side_pile = Pile("side"+(str(id)),36,(SCREEN_WIDTH//2+(450-CARD_WIDTH//2),(SCREEN_HEIGHT - 2* CARD_HEIGHT - 2* 30))) 
            self.cards = Pile(str(id)+"cards",52,(1300,-100))
            self.inputs = ["n","j","k","l",";","b","h"]

class Opponent(Player):
    def __init__(self,difficulty):
        super(Opponent,self).__init__(1)
        self.delay = difficulty
        
    def make_move(self,game):
        pile = game.check_for_moves(self)
        if pile != False:
            game.play_card(pile, self)
    
    def flip(self):
        for stack in self.hand:
            topcard = stack._peek()
            if topcard == False:
                continue
            if topcard.faced_up == False:
                print(topcard.name)
                topcard.faced_up = True
                return True
