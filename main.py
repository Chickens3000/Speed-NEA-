import pygame
from network import Network
from _game import * 
from _cards import *
pygame.init()
pygame.font.init()
pygame.display.init()
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
online = True
images = {}
def lerp(start, end, t): # change this
    return start + t * (end - start)

def move_towards(game:Game , card, target_pos):
    speed = 40
    dist_x = target_pos[0] - card.rect.x
    dist_y = target_pos[1] - card.rect.y
    distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
    # Check if the sprite is close enough to the target
    if distance < speed:
        card.rect.topleft = target_pos
        game.moving_sprites.remove(card)  # Snap to the target position
    else:
        # Move the sprite incrementally
        card.rect.x = lerp(card.rect.x, target_pos[0], speed / distance)
        card.rect.y = lerp(card.rect.y, target_pos[1], speed / distance)

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(0)
    player = game.players[0]
    game.create_sprites()
    game.start_game()
    for card in game.deck.contents:
        images[card.name] = Image(card.name)
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

        screen.blit(bg,(0,0))
        for entity in game.moving_sprites:
            move_towards(game,images[entity.name],entity.pos)
        for entity in game.all_sprites:
            screen.blit(images[entity.name].surf, images[entity.name].rect)
        

        pygame.display.flip()
     
def main_online():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()
    try:
        game = n.send("get")
    except:
        print("Couldn't get game1 ")
        run = False
    try:
        game = n.send("start")
    except:
        print("Couldn't get game 2")
        run = False
    for card in game.deck.contents:
        images[card.name] = Image(card.name)
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game 3")
            break
       
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                else:
                    n.send(event.unicode)
            elif event.type == QUIT:
                run = False
                
        screen.blit(bg,(0,0))
        for entity in game.moving_sprites:
            move_towards(game,images[entity.name],entity.pos)
        for entity in game.all_sprites:
            screen.blit(images[entity.name].surf, images[entity.name].rect)
        

        pygame.display.flip()

if online == True:
    main_online()
else:
    main()

#Decelerator