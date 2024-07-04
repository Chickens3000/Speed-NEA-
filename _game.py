from _player import *
from _cards import *
import random

class Game():
    def __init__(self,id):
        self.id = id
        self.ready = False
        self.players = [Player(0),Player(1)]
        self.center_piles = [Pile("center1",52,(450,230)),Pile("center2",52,(606,230))]
        self.deck = Deck("deck",52,(0,0))
        self.moving_sprites = pygame.sprite.Group() 
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.flip_ready = [False,False]

    def create_sprites(self):
        self.all_sprites = self.deck.create_deck(self.all_sprites)

    def start_game(self):
        random.shuffle(self.deck.contents)
        self.players[0].cards.push_all(self.deck.contents[0:26])
        self.players[1].cards.push_all(self.deck.contents[26:53])
        for player in self.players:
            for i in range(player.cards.stack_pointer +1 ):
                card = player.cards.contents[i]
                card.pos = player.cards.pos
                self.moving_sprites.add(card)
        self.round_setup()
        

    def round_setup(self):
        for player in self.players:
            for i in range(0,5):
                for x in range(5-i):
                   self.move_card(player.cards,player.hand[i])
                player.hand[i]._peek().faced_up = True
            self.move_all(player.cards,player.side_pile)
        self.flip_cards()

    
    def lerp(self, start, end, t):
        return start + t * (end - start)

    def move_card(self,start:Pile,end:Pile):
        #Subroutine added to make animation easier
            card = start._pop()
            if card == False:
                print(start.name,"Empty!")
            else:
                end.push(card, self.all_sprites)
                card.pos = end.pos
                self.moving_sprites.add(card)

    def move_all(self,start:Pile,end:Pile):
        card = start._pop()
        while card != False:
            end.push(card, self.all_sprites)
            card.pos = end.pos
            self.moving_sprites.add(card)
            card = start._pop()

    def flip_cards(self):
        self.move_card(self.players[0].side_pile,self.center_piles[0])
        self.move_card(self.players[1].side_pile,self.center_piles[1])
        for pile in self.center_piles:
            pile._peek().faced_up = True

    def end_round(self): # Assuming slammed pile has allready been added to cards
        for player in self.players:
            player.cards.push_all(player.side_pile.pop_all())
            for stack in player.hand:
                player.cards.push_all(stack.pop_all())
            for i in range(player.cards.stack_pointer):
                player.cards.contents[i].faced_up = False
        self.round_setup()

    def update(self,player: Player,data: str):
        if data in self.players[1].inputs:
            player = self.players[1]
        
        if data == player.inputs[0]:
            pile = player.hand[0]
        elif data ==  player.inputs[1]:
            pile = player.hand[1]
        elif data ==  player.inputs[2]:
            pile = player.hand[2]
        elif data ==  player.inputs[3]:
            pile = player.hand[3]
        elif data ==  player.inputs[4]:
            pile = player.hand[4]
        elif data == player.inputs[5] or data == player.inputs[6]:
            self.slam(player, data)
            return False
        else:
            return False            # If input is invalid, end procedure
        if pile._peek() == False: # If pile is empty, end procedure
            return False
        if pile._peek().faced_up == False: #If card is not revealed, reveal card
            pile._peek().faced_up =True
            return False
        for centre_pile in self.center_piles: # if card can be played, play card
            if self.move_is_valid(pile._peek(),centre_pile._peek()) == True:
                self.move_card(pile,centre_pile)
                self.flip_ready =  [False,False]
                return False
        if self.stack(pile,player) != False: 
            hand  = self.stack(pile,player)
            while pile._peek() != False and pile._peek().faced_up == True:
                    self.move_card(pile,hand)
            return False
        if self.shift_cards(pile,player) != False:# Moves cards to empty pile if possible 
            hand  = self.shift_cards(pile,player)
            while pile._peek() != False and pile._peek().faced_up == True:
                    self.move_card(pile,hand)
            return False
        self.check_for_moves(player)

    def move_is_valid(self,card:Card,top_card:Card):
        if abs(top_card.code[0] - card.code[0]) == 1 or abs(top_card.code[0] - card.code[0])== 12:
            return True
        
    def stack(self,pile:Pile ,player:Player):
        for hand in player.hand:
            top_card = hand._peek()
            if top_card == False:
                continue
            elif pile == hand:
                continue
            elif pile._peek().code[0] == top_card.code[0] and top_card.faced_up == True: # This was a fix that can come up in testing
                return hand
            
        return False

    def shift_cards(self, pile:Pile, player:Player):
        count = 0 
        for i in range(pile.stack_pointer+1):
            if pile.contents[i].faced_up == True:
                count+= 1
        if count == pile.stack_pointer +1:
            return False
        for hand in player.hand:
            if hand._peek() == False:
                return hand
        return False

    def check_for_moves(self, player:Player):
        for stack in player.hand:
            if stack._peek() == False:
               continue
            for centre_pile in self.center_piles: # if card can be played, return that card
                if self.move_is_valid(stack._peek(),centre_pile._peek()) == True:
                    return stack._peek()
            if stack._peek().faced_up == False: #If card is not revealed, reveal card
                return stack._peek()
            if self.stack(stack,player) != False: 
                return stack._peek()
            if self.shift_cards(stack,player) != False:# Moves cards to empty pile if possible 
                return stack._peek()
        
        if self.empty_hand(player) == True:
            return False
        self.flip_ready[player.id] = True
        if self.flip_ready[abs(player.id-1)] == True:
            self.flip_cards()
        
    def slam(self, player:Player, data):
        if self.empty_hand(self.players[0]) == True or self.empty_hand(self.players[1]) == True:
            if data == player.inputs[5]:
                self.move_all(self.center_piles[0],player.cards)
                self.move_all(self.center_piles[1],self.players[abs(player.id -1)].cards)
            elif data == player.inputs[6]:
                self.move_all(self.center_piles[1],player.cards)
                self.move_all(self.center_piles[0],self.players[abs(player.id -1)].cards)
            else:
                return False
            self.end_round()

    def empty_hand(self, player:Player):
        for stack in player.hand:
            if stack._peek() != False:
                return False
        return True


        



class Queue:
    # Constructor
    def __init__(self):
        self.FrontPointer = 0
        self.BackPointer = -1
        self.Max = 4
        self.Contents = ["" for Elements in range(self.Max)]
    # Add an item to the queue
    def Enqueue(self, Item):
        print(self.Contents.count(""))
        print(self.items_in_queue())
        if self.items_in_queue() != self.Max:
            self.BackPointer = self.increment_pointer(self.BackPointer)
            self.Contents[self.BackPointer] = Item
            return True
        else:
            return False
    # Remove an item from the queue
    def Dequeue(self):
        if self.items_in_queue() == 0:
            return False
        else:
            Item = self.Contents[self.FrontPointer]
            self.Contents[self.FrontPointer] = ""
            self.FrontPointer= self.increment_pointer(self.FrontPointer)
            return Item
            
    # Look at the next item in the queue without removing it      
    def Peek(self):
        if self.items_in_queue() == 0:
            return None
        else:
            return self.Contents[self.FrontPointer]
    
    def outputQ(self):
        print(self.Contents)

    def increment_pointer(self,pointer):
        if pointer < self.Max-1:
            pointer += 1
        else:
            pointer = 0
        return pointer
    
    def items_in_queue(self):
        return (self.Max)-(self.Contents.count(""))