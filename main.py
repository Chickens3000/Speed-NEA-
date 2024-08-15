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
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    QUIT,
)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("./images/backround.jpg")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game")
online = False
images = {}
def lerp(start, end, t):
    return start + t * (end - start)

def move_towards(game:Game , card:Image, target_pos):
    surf, rect = card._image()
    speed = 40
    dist_x = target_pos[0] - rect.x
    dist_y = target_pos[1] - rect.y
    distance = (dist_x ** 2 + dist_y ** 2) ** 0.5
    # Check if the sprite is close enough to the target
    if distance < speed:
        rect.topleft = target_pos
        card.card_sprite.start_pos = target_pos
        game.moving_sprites.remove(card.card_sprite)  # Snap to the target position
    else:
        # Move the sprite incrementally
        rect.x = lerp(rect.x, target_pos[0], speed / distance)
        rect.y = lerp(rect.y, target_pos[1], speed / distance)

def get_pile_under_mouse(game:Game):
    x,y = pygame.Vector2(pygame.mouse.get_pos())
    for pile in game.all_piles:
        if x > pile.pos[0] and x < (pile.pos[0] + CARD_WIDTH) and y > pile.pos[1] and y < (pile.pos[1]+CARD_HEIGHT):
            return pile
    return None  

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(0)
    player = game.players[0]
    selected_card = None
    old_pile = None
    
    game.create_sprites()
    game.start_game()
    for card in game.deck.contents:
        images[card.name] = Image(card)
    while run:
        pile_hover = get_pile_under_mouse(game)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                else:
                    game.keyboard_update(player,event.unicode)
            elif event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                if pile_hover != None:
                    selected_card = pile_hover._peek()
                    old_pile = pile_hover
            if event.type == MOUSEBUTTONUP:
                if pile_hover != None and old_pile != None:
                    game.mouse_update(old_pile,pile_hover)
                else:
                    if selected_card != None:
                        game.move_card(old_pile,old_pile)
                selected_card = None
                old_pile = None
                
        if selected_card:
            game.moving_sprites.add(selected_card)
            selected_card.pos = (pygame.Vector2(pygame.mouse.get_pos())[0]-(CARD_WIDTH/2),pygame.Vector2(pygame.mouse.get_pos())[1]-(CARD_HEIGHT/2))


        screen.blit(bg,(0,0))

        for entity in game.all_sprites:
            if entity.faced_up != images[entity.name].seen:
                images[entity.name].change_image()
            screen.blit(images[entity.name]._image()[0],images[entity.name]._image()[1])
            if entity in game.moving_sprites:
                move_towards(game,images[entity.name],entity.pos)
        
        pygame.display.flip()
     
def main_online():
    game : Game
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()
    selected_card = None
    old_pile = None
    try:
        game = n.send("get")
    except:
        print("Couldn't get game 1")
        run = False
    
    try:
        for card in game.deck.contents:
            images[card.name] = Image(card)
    except Exception as E:
        print(E)
        print("Couldn't get game 2")
        run = False 

    while run:
        
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game 3")
            break
        pile_hover = get_pile_under_mouse(game)
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                else:
                    n.send(event.unicode)
            elif event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                if pile_hover != None:
                    selected_card = pile_hover._peek()
                    old_pile = pile_hover
            if event.type == MOUSEBUTTONUP:
                if pile_hover != None and old_pile != None:
                    #game.mouse_update(old_pile,pile_hover)
                    n.send("update:"+old_pile.name+";"+pile_hover.name)
                else:
                    if selected_card != None:
                        #game.move_card(old_pile,old_pile)
                        n.send("return:"+old_pile.name)
                selected_card = None
                old_pile = None
                
       
                
        screen.blit(bg,(0,0))
        for entity in game.all_sprites:
            if entity.faced_up != images[entity.name].seen:
                images[entity.name].change_image()
            if selected_card:
                move_towards(game,images[selected_card.name],(pygame.Vector2(pygame.mouse.get_pos())[0]-(CARD_WIDTH/2),pygame.Vector2(pygame.mouse.get_pos())[1]-(CARD_HEIGHT/2)))
            elif entity in game.moving_sprites:
                move_towards(game,images[entity.name],entity.pos)
                
            screen.blit(images[entity.name]._image()[0],images[entity.name]._image()[1])

        
        
        pygame.display.flip()

if online == True:
    main_online()
else:
    main()