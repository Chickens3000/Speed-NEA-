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
moving_sprites = pygame.sprite.Group()
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

deck = Deck("deck",52,(0,0))


def lerp(start, end, t): # change this
    return start + t * (end - start)

def move_towards(card, target_pos):
    speed = 40
    dist_x = target_pos[0] - card.rect.x
    dist_y = target_pos[1] - card.rect.y
    distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
    # if distance < 100:
    #         speed = 5
    # Check if the sprite is close enough to the target
    if distance < speed:
        card.rect.topleft = target_pos
        moving_sprites.remove(card)  # Snap to the target position
    else:
        # Move the sprite incrementally
        card.rect.x = lerp(card.rect.x, target_pos[0], speed / distance)
        card.rect.y = lerp(card.rect.y, target_pos[1], speed / distance)

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(0)
    player = game.players[0]
    game.start_game(deck)
    while run:
        clock.tick(60)
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                else:
                    game.update(player,event.unicode)
            elif event.type == QUIT:
                run = False

            if event.type == MOVECARD:
                move = event.move
                card = move[0]
                card.target_pos = move[1]
                moving_sprites.add(card)
                

        screen.blit(bg,(0,0))
        for entity in moving_sprites:
            move_towards(entity,entity.target_pos)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        

        pygame.display.flip()
     
def main_online():

    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()
    try:
        game = n.send("get")
    except:
        print("Couldn't get game")
        run = False
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
    
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                else:
                    n.send(event.unicode)
            elif event.type == QUIT:
                run = False

            if event.type == MOVECARD:
                move = event.move
                card = move[0]
                card.target_pos = move[1]
                moving_sprites.add(card)
                

        screen.blit(bg,(0,0))
        for entity in moving_sprites:
            move_towards(entity,entity.target_pos)
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        

        pygame.display.flip()

if online == True:
    main_online()
else:
    main()

#Decelerator