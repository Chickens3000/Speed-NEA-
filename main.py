import pygame
from network import Network
from _game import * 
from gameobjects import *
from screencards import *
from _thread import *
from time import sleep
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

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("./images/backround.jpg")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game")
scr = ScreenCard() 
online = True
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

def time_out(player : Player,game:Game, card:Image, start_pos):
    player.timed_out = True
    for i in range(5):
        sleep(0.05)
        move_towards(game, card, (start_pos[0]+10,start_pos[1]))
        sleep(0.05)
        move_towards(game, card, (start_pos[0]-10,start_pos[1]))
        move_towards(game, card, (start_pos[0]-10,start_pos[1]))
        sleep(0.05)
        move_towards(game, card,start_pos)
  
    player.timed_out = False

def load_text(string, size, colour):
    font = pygame.font.SysFont(FONT,size)
    text = font.render(string, 1, colour)
    return text
def fonts(game:Game):
    if game.flip_ready[0] == True:
        text = Text("ready",50)
        text.set_pos((game.players[0].side_pile.pos[0] + CARD_WIDTH + 20),game.players[0].side_pile.pos[1])
        text.draw(win)
    if game.flip_ready[1] == True:
        text = Text("ready",50)
        text.set_pos((game.players[1].side_pile.pos[0] - text.width - 20),game.players[1].side_pile.pos[1])
        text.draw(win)
    if game.empty_hand(game.players[0]) == True or game.empty_hand(game.players[1]) == True:
        text1 = Text("T / B",80)
        text2 = Text("Y / H",80)
        text1.set_pos(SCREEN_WIDTH//2-CARD_WIDTH - text1.width - 20,SCREEN_HEIGHT//2 - text1.height//2)
        text2.set_pos(SCREEN_WIDTH//2+CARD_WIDTH + 20 ,SCREEN_HEIGHT//2 - text2.height//2)
        text1.draw(win)
        text2.draw(win)

def button_action(text):
    if text == "Singleplayer":
        scr.empty()
        main()
        scr.main_menu()
    elif text == "2 Player":
        scr.empty()
        main_online()
        scr.main_menu()

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
    images["red_joker"] = Image(Joker((99,"J")))
    while run:
        
        pile_hover = get_pile_under_mouse(game)
        clock.tick(60)
        if game.winner:
            scr.win_card(game.winner,player)
            menu()
            run = False


        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                else:
                    if event.unicode not in player.inputs:
                        player = game.players[abs(player.id -1)]
                    if player.timed_out == False:
                        _return = game.keyboard_update(player,event.unicode)
                        if _return != False:
                            start_new_thread(time_out,(player,game,images[_return._peek().name],_return._peek().pos))

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


        win.blit(bg,(0,0))
        fonts(game)
        for entity in game.all_sprites:
            if entity.faced_up != images[entity.name].seen:
                images[entity.name].change_image()
            win.blit(images[entity.name]._image()[0],images[entity.name]._image()[1])
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
            images["red_joker"] = Image(Joker((99,"J")))
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
        if game.winner:
            scr.win_card(game.winner,player)
            menu()
            run = False

        for event in pygame.event.get():

            if event.type == KEYDOWN: # Timeoutes online to be done server side
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
                    n.send("update:"+old_pile.name+";"+pile_hover.name)
                else:
                    if selected_card != None:
                        n.send("return:"+old_pile.name)
                selected_card = None
                old_pile = None
                
       
                
        win.blit(bg,(0,0))
        fonts(game)
        for entity in game.all_sprites:
            if entity.faced_up != images[entity.name].seen:
                images[entity.name].change_image()
            if selected_card:
                move_towards(game,images[selected_card.name],(pygame.Vector2(pygame.mouse.get_pos())[0]-(CARD_WIDTH/2),pygame.Vector2(pygame.mouse.get_pos())[1]-(CARD_HEIGHT/2)))
            elif entity in game.moving_sprites:
                move_towards(game,images[entity.name],entity.pos)
                
            win.blit(images[entity.name]._image()[0],images[entity.name]._image()[1])

        
        
        pygame.display.flip()

def menu():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in scr.buttons:
                    if button.click(pos):
                        button_action(button.name)
        
        win.blit(bg,(0,0))
        scr.display(win)
        pygame.display.flip()

scr.main_menu()
menu()
