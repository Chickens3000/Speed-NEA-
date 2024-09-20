import pygame
import random
import subprocess
from time import sleep
from network import Network
from _game import * 
from gameobjects import *
from screencards import *
from _thread import *

pygame.init() 
pygame.font.init()
pygame.display.init()
from pygame.locals import *

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.image.load("./images/backround.jpg")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game")
scr = ScreenCard() 
images = {}

def run_server_script():
    subprocess.Popen(["python","Server.py"])

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
        card.move_towards(game, (start_pos[0]+10,start_pos[1]))
        sleep(0.05)
        card.move_towards(game, (start_pos[0]-10,start_pos[1]))
        card.move_towards(game, (start_pos[0]-10,start_pos[1]))
        sleep(0.05)
        card.move_towards(game,start_pos)
  
    player.timed_out = False

def button_action(text):
    if text == "Singleplayer":
        scr.singleplayer_menu()
    elif text == "2 Player":
        scr.two_player_menu()
    elif text == "Local":
        scr.empty()
        main_2_player()
    elif text == "Online":
        scr.online_menu()
    elif text == "Host":
        main_online("Host")
    elif text == "Join":
        scr.empty()
        join_menu()
    elif text == "Theo":
        scr.empty()
        main_1_player(5000)
    elif text == "Sophie":
        scr.empty()
        main_1_player(2000)
    elif text == "Harvey":
        scr.empty()
        main_1_player(1000)
    elif text == "Robin":
        scr.empty()
        main_1_player(750)
    elif text == "Gilly":
        scr.empty()
        main_1_player(-1)

def main_1_player(delay):
    run = True
    clock = pygame.time.Clock()
    game = Game(0)
    player = game.players[0]
    if delay == -1:
        game.players[1] = AdaptiveOpponent(2000)
    else:
        game.players[1] = Opponent(delay)
    
    selected_card = None
    old_pile = None
    AI_MOVE = pygame.USEREVENT + 1
    AI_FLIP = pygame.USEREVENT + 2
    pygame.time.set_timer(AI_MOVE,game.players[1].delay)
    pygame.time.set_timer(AI_FLIP,game.players[1].delay//2 + random.randint(10,25)*17)
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

        if game.players[1].delay != delay:
            pygame.time.set_timer(AI_MOVE,game.players[1].delay)
            pygame.time.set_timer(AI_FLIP,game.players[1].delay//2 + random.randint(10,25)*17)
            delay = game.players[1].delay

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.paused = True
                    scr.paused()
                    run = paused_screen(game,images)
                    game.paused = False
                else:
                    if player.timed_out == False:
                        _return = game.keyboard_update(player,event.unicode)
                        if _return != False:
                            start_new_thread(time_out,(player,game,images[_return._peek().name],_return._peek().pos))
            if event.type == AI_FLIP:
                game.players[1].flip()
            if event.type == AI_MOVE:
                game.players[1].make_move(game)
            if event.type == QUIT:
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

        win.blit(bg,(0,0))
        scr.game_texts(game,win)
        scr.display_cards(game,images,win,selected_card)
        pygame.display.flip()
    scr.main_menu()

def main_2_player():
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
                    game.paused = True
                    scr.paused()
                    run = paused_screen(game,images)
                    game.paused = False
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

        win.blit(bg,(0,0))
        scr.game_texts(game,win)
        scr.display_cards(game,images,win,selected_card)

        pygame.display.flip()
    scr.main_menu()
     
def main_online(HostIP):
    game : Game
    run = True
    clock = pygame.time.Clock()
    n = Network()
    if HostIP == "Host":
        run_server_script()
    ip = n.set_ip(HostIP)
    player = n.getP()
    selected_card = None
    old_pile = None
    try:
        game = n.send("get")
        for card in game.deck.contents:
            images[card.name] = Image(card)
            images["red_joker"] = Image(Joker((99,"J")))
    except:
        return False

    while run:
        
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            scr.online_quit()
            menu()
            break
        if game.ready == False:
            if player.id == 0:
                scr.waiting_for_game(win,bg,ip)
            else:
                scr.press_to_start(win,bg)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN: 
                    if event.key == K_ESCAPE:
                        run = False
                    else:
                        n.send(event.unicode)
        elif game.paused == True:
            scr.opponent_paused(game,images,win,bg)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN: 
                    if event.key == K_ESCAPE:
                        run = False
        else:
            pile_hover = get_pile_under_mouse(game)
            if game.winner:
                scr.win_card(game.winner,player)
                menu()
                run = False

            for event in pygame.event.get():

                if event.type == KEYDOWN: # Timeoutes online to be done server side
                    if event.key == K_ESCAPE:
                        n.send("pause")
                        scr.paused()
                        run = paused_screen(game,images)
                        n.send("pause")
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
            scr.game_texts(game,win)
            scr.display_cards(game,images,win,selected_card)

        
        
        pygame.display.flip()
    scr.main_menu()
    return True

def paused_screen(game:Game,images):
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                   return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in scr.buttons:
                    if button.click(pos):
                        if button.name == "Resume":
                            return True
                        elif button.name == "Quit":
                            return False
        
        win.blit(bg,(0,0))
        for entity in game.all_sprites:
            win.blit(images[entity.name]._image()[0],images[entity.name]._image()[1])
            
        haze =pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        haze.fill((128,128,128))
        haze.set_alpha(200)
        win.blit(haze,(0,0))
        scr.display(win)
        pygame.display.flip()

def join_menu():
    scr.empty()
    run = True
    clock = pygame.time.Clock()
    ip_valid = False
    text = ""
    while ip_valid == False:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if scr.screen == "main_menu":
                        exit()
                    else:
                        scr.main_menu()
                        menu()
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    ip_valid = main_online(text)
                    if ip_valid == False:
                        text = ""
                        invalid_text = Text("Server with this IP does not exist",60)
                        invalid_text.set_pos(SCREEN_WIDTH//2-invalid_text.width//2,SCREEN_HEIGHT//2 - invalid_text.height//2 - 200)
                        scr.texts.add(invalid_text)
                    else:
                        ip_valid = True
                elif event.key == K_SPACE or event.unicode == "":
                    pass
                else:
                    text += event.unicode



        win.blit(bg,(0,0))
        typed = Text("IP:"+text,80)
        typed.set_pos(SCREEN_WIDTH//2-typed.width//2,SCREEN_HEIGHT//2 - typed.height//2)
        typed.draw(win)
        scr.display(win)
        pygame.display.flip()

def menu():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if scr.screen == "main_menu":
                        exit()
                    else:
                        scr.main_menu()
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

#make waiting for opponent, opponend paused, paused menus
#Do not make games menus, are either in a menu, or in a game

