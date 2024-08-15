import pygame
from pygame.locals import (
    RLEACCEL
)
CARD_WIDTH = 144
CARD_HEIGHT = 209

class Card(pygame.sprite.Sprite):
    def __init__(self, code:tuple):
        super(Card, self).__init__()
        self.code = code
        self.name = self.create_name()
        self.faced_up = False
        # self.image = "./images/"+self.name + ".png"
        # self.seen = True
        # self.surf = pygame.image.load(self.image)
        # self.surf= pygame.transform.scale(self.surf, (144,209)).convert()
        # self.rect = self.surf.get_rect()
        self.start_pos = (0,1)
        self.pos = (0,0)
    def create_name(self):
        name = ""

        if self.code[0] == 1:
            name += "ace_of_"
        elif self.code[0] == 11:
            name += "jack_of_"
        elif self.code[0] == 12:
            name += "queen_of_"
        elif self.code[0] == 13:
            name += "king_of_"
        else:
            name += str(self.code[0]) +"_of_"
        
        if self.code[1] == "S":
            name+= "spades"
        elif self.code[1] == "H":
            name+= "hearts"
        elif self.code[1] == "C":
            name+= "clubs"
        elif self.code[1] == "D":
            name+= "diamonds"
        return name
        
class Pile:

    def __init__(self,name,max,pos) -> None:
        self.stack_pointer = -1
        self.max = max
        self.contents = ["" for Elements in range(self.max)]
        self.name = name
        self.pos = pos


    def push(self, card: tuple,all_sprites):
        if self.stack_pointer < self.max -1:
            self.stack_pointer += 1
            self.contents[self.stack_pointer] = card
            all_sprites.change_layer(sprite = card,new_layer=self.stack_pointer)
        else:
            print("Stack Overflow:",self.name)
            return False
    
    def _pop(self):
        if self.stack_pointer >= 0:
            self.stack_pointer -= 1
            card = self.contents[self.stack_pointer + 1]
            self.contents[self.stack_pointer + 1] = ""
            return card
        else:
            return False
    
    def _peek(self):
      if self.stack_pointer >= 0:
        card:Card = self.contents[self.stack_pointer]
        return card
      else:
          return False

    def push_all(self, cards: list):
        if cards == False:
            print("Empty")
            return False
        if self.stack_pointer < self.max - len(cards):
            self.stack_pointer += 1
            self.contents[self.stack_pointer:(self.stack_pointer +len(cards))] = cards
            self.stack_pointer =self.stack_pointer +(len(cards)-1)
        else:
            print("Stack Overflow:",self.name)
            return False
        
    def pop_all(self):
        if self.stack_pointer >= 0:
            cards = self.contents[0:(self.stack_pointer+1)]
            self.contents[0:(self.stack_pointer+1)] = ["" for Elements in range(self.stack_pointer+1)]
            self.stack_pointer = -1
            return cards
        else:
            return False

class Deck(Pile):
    def create_deck(self,all_sprites :pygame.sprite.Group):
        suits =["S","H","D","C"]
        for suit in suits:
            for i in range(1,14):
                card = Card((i,suit))
                all_sprites.add(card)
                self.push(card,all_sprites)  
        return all_sprites

class Image():
    def __init__(self,card: Card):
        self.card_sprite = card
        self.name = card.name
        self.image = "./images/"+self.name + ".png"
        self.seen = False
        self.surf = pygame.image.load(self.image)
        self.surf= pygame.transform.scale(self.surf, (CARD_WIDTH,CARD_HEIGHT)).convert()
        self.rect = self.surf.get_rect()
        self.back_surf= pygame.image.load("./images/back.png")
        self.back_surf= pygame.transform.scale(self.back_surf, (CARD_WIDTH,CARD_HEIGHT)).convert()
        self.back_rect = self.back_surf.get_rect()

    def _image(self):
        if self.seen == True:
            return self.surf, self.rect
        else:
            return self.back_surf, self.back_rect
        
    def change_image(self):
        if self.seen == False:
            self.rect.topleft = self.card_sprite.start_pos
            self.seen = True
        else:
            self.back_rect.topleft = self.card_sprite.start_pos
            self.seen = False