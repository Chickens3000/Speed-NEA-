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
        self.all_sprites = pygame.sprite.Group()


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
        self.flip_cards()

    def round_setup(self):
        for player in self.players:
            for i in range(0,5):
                for x in range(5-i):
                   self.move_card(player.cards,player.hand[i])
            self.move_all(player.cards,player.side_pile)

    
    def lerp(self, start, end, t):
        return start + t * (end - start)

    def move_card(self,start:Pile,end:Pile):
        #Subroutine added to make animation easier
            card = start._pop()
            if card == False:
                print("Empty!")
            else:
                end.push(card)
                card.pos = end.pos
                self.moving_sprites.add(card)

    def move_all(self,start:Pile,end:Pile):
        card = start._pop()
        while card != False:
            end.push(card)
            card.pos = end.pos
            self.moving_sprites.add(card)
            card = start._pop()

    def flip_cards(self):
        self.move_card(self.players[0].side_pile,self.center_piles[0])
        self.move_card(self.players[1].side_pile,self.center_piles[1])

    def end_round(self): # Assuming slammed pile has allready been added to cards
        for player in self.players:
            player.cards.push_all(player.side_pile.pop_all())
            for stack in player.hand:
                player.cards.push_all(stack.pop_all())

    def update(self,p: Player,data: str):
        player = p
        if data == "q":
            self.move_card(player.cards,player.hand[0])
        if data == "w":
            self.move_card(player.cards,player.hand[1])
        if data == "e":
            self.move_card(player.cards,player.hand[2])
        if data == "r":
            self.move_card(player.cards,player.hand[3])
        if data == "g":
            self.move_card(player.cards,player.hand[4])
            

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