from _player import *
from gameobjects import *
import random

class Game():
    def __init__(self,id):
        self.id = id
        self.ready = False
        self.players = [Player(0),Player(1)]
        self.center_piles = [Pile("center0",52,(SCREEN_WIDTH//2 - CARD_WIDTH - 10,(SCREEN_HEIGHT - 2* CARD_HEIGHT - 2* 30))),Pile("center1",52,(SCREEN_WIDTH//2 + 10,(SCREEN_HEIGHT - 2* CARD_HEIGHT - 2* 30)))]
        self.deck = Deck("deck",52,(0,0))
        self.moving_sprites = pygame.sprite.Group() 
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.flip_ready = [False,False]
        self.all_piles = self.center_piles + self.players[0].hand + [self.players[0].side_pile] + self.players[1].hand + [self.players[1].side_pile]
        self.winner = None

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
        self.next_round()
        
    def next_round(self):
        if (self.players[0].cards.stack_pointer + 1) > 15 and (self.players[1].cards.stack_pointer + 1) > 15:
            self.round_setup()
        else:
            self.endgame_round()
    def round_setup(self):
        for player in self.players:
            for i in range(0,5):
                for x in range(5-i):
                   self.move_card(player.cards,player.hand[i])
                player.hand[i]._peek().faced_up = True
            self.move_all(player.cards,player.side_pile)
        self.flip_cards()

    def endgame_round(self):
        borrow,borrower_id = False,0
        for player in self.players:
            if (player.cards.stack_pointer + 1) <=15 and (player.cards.stack_pointer + 1) >= 10:
                borrow,borrower_id = True,player.id
                for i in range(0,5):
                    for x in range(5-i):
                        self.move_card(player.cards,player.hand[i])
                    if player.hand[i].is_empty():
                        break
                    player.hand[i]._peek().faced_up = True
            elif (player.cards.stack_pointer + 1) < 10:
                for i in range(0,5):
                    for x in range(5-i):
                        self.move_card(player.cards,player.hand[i])
                    if player.hand[i].is_empty():
                        break
                    player.hand[i]._peek().faced_up = True
                player.side_pile.push(self.create_joker(),self.all_sprites) 
            else:
                for i in range(0,5):
                    for x in range(5-i):
                        self.move_card(player.cards,player.hand[i])
                    player.hand[i]._peek().faced_up = True
                self.move_all(player.cards,player.side_pile)
        if borrow == True:
            print(borrower_id)
            self.move_card(self.players[abs(borrower_id-1)].side_pile,self.players[borrower_id].side_pile)
        self.flip_cards()


    def create_joker(self):
        joker = Joker((99,"J"))
        self.all_sprites.add(joker)
        return joker    
    
    def lerp(self, start, end, t):
        return start + t * (end - start)

    def move_card(self,start:Pile,end:Pile):
        #Subroutine added to make animation easier
            card = start._pop()
            if card == False:
                print(start.name,"Empty!")
            else:
                if end.name[0:4] == "side":
                    card.pos = end.pos
                elif end.name[0:6] == "center":
                    if end.stack_pointer <= 8:
                        card.pos = (end.pos[0],end.pos[1] + 2*end.stack_pointer)
                    else:
                        card.pos = (end.pos[0],end.pos[1] + 16)
                else:
                    if end.stack_pointer <= 8:
                        card.pos = (end.pos[0],end.pos[1] + 4*end.stack_pointer)
                    else:
                        card.pos = (end.pos[0],end.pos[1] + 32)
                end.push(card, self.all_sprites)
              

                self.moving_sprites.add(card)

    def move_all(self,start:Pile,end:Pile):
        card = start._pop()
        while card != False:
            end.push(card, self.all_sprites)
            card.pos = end.pos
            self.moving_sprites.add(card)
            card = start._pop()

    def flip_cards(self):
        if self.players[0].side_pile.is_empty() != True:
            self.move_card(self.players[0].side_pile,self.center_piles[0])
        if self.players[1].side_pile.is_empty() != True:
            self.move_card(self.players[1].side_pile,self.center_piles[1])        
        for pile in self.center_piles:
            if pile.is_empty != True:
                pile._peek().faced_up = True
        
        self.flip_ready = [False,False]

    def end_round(self): # Assuming slammed pile has allready been added to cards
        for player in self.players:
            print(player.cards, player.cards.stack_pointer)
            player.cards.push_all(player.side_pile.pop_all())
            for stack in player.hand:
                player.cards.push_all(stack.pop_all())
            for i in range(player.cards.stack_pointer):
                player.cards.contents[i].faced_up = False
            print(player.cards,player.cards.stack_pointer)
        self.next_round()

    def mouse_update(self,old_pile:Pile,new_pile:Pile):#should probably add a player check
        if old_pile._peek() == False: # If pile is empty or if new piles card is faced down, end procedure
            return False
        
        if old_pile.name[0:4] == "side": # If user clicks side pile, check for moves and flip card
            self.check_for_moves(self.players[int(old_pile.name[4])])
            self.move_card(old_pile,old_pile)
            return False
        
        if old_pile.name[0:6] == "center": 
            self.slam(self.players[0],old_pile)

        if old_pile._peek().faced_up == False: #If card is not revealed, reveal card
            old_pile._peek().faced_up = True
            self.move_card(old_pile,old_pile)
            return False
        
        if new_pile._peek() == False and new_pile.name[0] == old_pile.name[0] and new_pile.name[0:4] != "side":
            while old_pile._peek() != False and old_pile._peek().faced_up == True:
                    self.move_card(old_pile,new_pile)
            return False
        
        if new_pile._peek() == False:
            self.move_card(old_pile,new_pile)
            return False
        
        if new_pile._peek().faced_up == False:
            self.move_card(old_pile,old_pile)
            return False
       
        
        if self.move_is_valid(old_pile._peek(),new_pile._peek()) == True and new_pile.name[0:6]== "center":
            self.move_card(old_pile,new_pile)
            self.flip_ready =  [False,False]
            return False
        
        if old_pile._peek().code[0] == new_pile._peek().code[0] and new_pile.name[0] == old_pile.name[0]: # If the number is the same, stack
            self.move_card(old_pile,new_pile)
            return False
        #self.check_for_moves(player)
        self.move_card(old_pile,old_pile)



    def keyboard_update(self,player: Player,data: str): # returns pile if input is valid but not valid move
        
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
        elif data == player.inputs[5]:
            self.slam(player, self.center_piles[0])
            return False
        elif data == player.inputs[6]:
            self.slam(player, self.center_piles[1])
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
        return pile

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
        if self.players[abs(player.id-1)].side_pile.is_empty():
            self.check_for_moves(self.players[abs(player.id-1)])
        elif self.flip_ready[abs(player.id-1)] == True:
            self.flip_cards()
        
    def slam(self, player:Player, pile: Pile):
        id = int(pile.name[6])
        if (self.empty_hand(self.players[0]) == True or self.empty_hand(self.players[1]) == True) and pile.name[0:6] == "center":
            if pile._peek().name == "red_joker":
                if self.check_for_win(player) == True:
                    self.winner = player
                else:
                    self.all_sprites.remove(pile._peek())
                    pile._pop()
            elif self.center_piles[abs(id-1)]._peek().name == "red_joker":
                self.all_sprites.remove(self.center_piles[abs(id-1)]._peek())
                self.center_piles[abs(id-1)]._pop()
            self.move_all(self.center_piles[id],player.cards)
            self.move_all(self.center_piles[abs(id-1)],self.players[abs(player.id -1)].cards)
            
            self.end_round()

    def check_for_win(self,player:Player):
        if self.empty_hand(player) == True and player.side_pile.is_empty() == True:
            return True
        else:
            return False

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