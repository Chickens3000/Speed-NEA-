import pygame
from network import Network
from _game import * 
from _cards import *

pygame.font.init()

from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
width = 1200
height = 720
screen = pygame.display.set_mode((width, height))
bg = pygame.image.load("./images/backround.jpg")
bg = pygame.transform.scale(bg, (width,height))
pygame.display.set_caption("Game")

all_sprites = pygame.sprite.Group()
online = True


class Deck(Pile):
    def create_deck(self,):
        global all_sprites
        suits =["S","H","D","C"]
        for suit in suits:
            for i in range(1,14):
                card = Card((i,suit))
                self.push(card)
                all_sprites.add(card)

deck = Deck("deck",52)
deck.create_deck()

def main():
    run = True
    clock = pygame.time.Clock()
    if online == True:
        n = Network()
        player = n.getP()
    else:
        player = 0

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            if online == False:
                game = Game(0)
            else:
                run = False
                print("Couldn't get game")
                break
        
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                else:
                    if online == True:
                        n.send(event.unicode)
                    else:
                        player.inputs.Enqueue(event.unicode)
            elif event.type == QUIT:
                run = False
        
        screen.blit(bg,(0,0))
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        pygame.display.flip()
# Game1 = Game(0)
# Game1.start_game()
# Game1.round_setup()
# print(Game1.players[1].side_pile.stack_pointer)
# for pile in Game1.players[1].hand:
#     print(pile.stack_pointer)

main()
#cand send scancodewrappers to server