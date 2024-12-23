# External imports
import pygame
import random
import subprocess
from time import sleep
from _thread import *

# Internal imports
from network import Network
from _game import * 
from gameobjects import *
from display import *

# Pygame initialization
pygame.init() 
pygame.font.init()
pygame.display.init()

from pygame.locals import *
pygame.display.set_caption("Speed/Split: You decide")

# Display and image dictionary
scr = Display() 
images = {}


def run_server_script():
    """Run the server script for online multiplayer."""
    subprocess.Popen(["python", "Server.py"])


def get_pile_under_mouse(game: Game):
    """
    Get the pile under the mouse pointer.
    
    This function checks if the mouse position is within the bounds
    of any pile in the game and returns that pile.
    """
    x, y = pygame.Vector2(pygame.mouse.get_pos())
    
    for pile in game.all_piles():
        if (
            x > pile.pos[0]
            and x < (pile.pos[0] + CARD_WIDTH)
            and y > pile.pos[1]
            and y < (pile.pos[1] + CARD_HEIGHT)
        ):
            return pile
    return None  


def time_out(player: Player, game: Game, card: Image, start_pos):
    """
    Handle player time-out animations.
    
    The player's card is animated to move slightly and return
    to the start position to visually indicate the time-out.
    """
    player.timed_out = True
    for i in range(5):
        sleep(0.05)
        card.move_towards(game, (start_pos[0] + 10, start_pos[1]))
        sleep(0.05)
        card.move_towards(game, (start_pos[0] - 10, start_pos[1]))
        card.move_towards(game, (start_pos[0] - 10, start_pos[1]))
        sleep(0.05)
        card.move_towards(game, start_pos)
    player.timed_out = False


def button_action(button):
    """
    Handle button click actions in the game menus.
    
    Depending on the button clicked, different game modes or menus
    are launched.
    """
    text = button.name
    scr.empty()
    if isinstance(button, Setting_Button):
        change_setting(button)
    elif text == "Singleplayer":
        scr.set_screen("singleplayer_menu")
    elif text == "2 Player":
        scr.set_screen("two_player_menu")
    elif text == "Settings":
        scr.set_screen("settings")
    elif text == "How to Play":
        scr.set_screen("H2P page 1")
    elif text == "Next Page":
        scr.set_screen("H2P page 2")
    elif text == "Local":
        main_2_player()
    elif text == "Online":
        scr.set_screen("online_menu")
    elif text == "Host":
        main_online("Host")
    elif text == "Join":
        join_menu()
    elif text == "Theo":
        main_1_player(5000)
    elif text == "Sophie":
        main_1_player(2000)
    elif text == "Harvey":
        main_1_player(1000)
    elif text == "Robin":
        main_1_player(750)
    elif text == "Gilly":
        main_1_player(-1)

def main_1_player(delay):
    # Initial setup
    run = True
    clock = pygame.time.Clock()
    game = Game(0)
    player = game.players[0]
    scr.setup_game_screen(game,player)

    # Determine opponent type based on delay
    if delay == -1:
        game.players[1] = AdaptiveOpponent(2000)
    else:
        game.players[1] = Opponent(delay)

    # Initialize selected card and pile variables
    selected_card = None
    old_pile = None

    # Custom events for AI move and AI flip
    # AI flip occurs at a random set interval, allows AI to have "2 hands"
    AI_MOVE = pygame.USEREVENT + 1
    AI_FLIP = pygame.USEREVENT + 2
    pygame.time.set_timer(AI_MOVE, game.players[1].delay)
    pygame.time.set_timer(
        AI_FLIP,
        game.players[1].delay // 2 + random.randint(10, 25) * 17
    )

    # Create game sutes and start the game
    game.create_sprites()
    game.start_game()

    # Load images for cards and jokers
    for card in game.deck.contents:
        images[card.name] = Image(card)
    images["red_joker"] = Image(Joker((99, "J")))

    # Main game loop
    while run:
        pile_hover = get_pile_under_mouse(game)
        clock.tick(60)

        # Check for a winner
        if game.winner:
             scr.set_winner_screen(player,game.winner,"win_card")
             menu()
             run = False

        # Adjust AI timers if delay changes
        if game.players[1].delay != delay:
            pygame.time.set_timer(AI_MOVE, game.players[1].delay)
            pygame.time.set_timer(
                AI_FLIP,
                game.players[1].delay // 2 + random.randint(10, 25) * 17
            )
            delay = game.players[1].delay

        # Event handling
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Handle pause menu
                    game.paused = True
                    run = paused_screen(game,images,player)
                    game.paused = False
                else:
                    if not player.timed_out:
                        #Pile only returned if an invalid move was made
                        pile = game.keyboard_update(player, event.unicode)
                        if pile:
                            start_new_thread(
                                time_out,
                                (player, game, images[pile._peek().name], 
                                pile._peek().pos)
                            )

            if event.type == AI_FLIP:
                game.players[1].flip()
            if event.type == AI_MOVE:
                game.players[1].make_move(game)

            if event.type == QUIT:
                run = False

            if event.type == MOUSEBUTTONDOWN:
                #Select card on click
                if pile_hover:
                    selected_card = pile_hover._peek()
                    game.moving_sprites.add(selected_card)
                    old_pile = pile_hover

            if event.type == MOUSEBUTTONUP:
                #Move card on release
                if pile_hover and old_pile:
                    game.mouse_update(player,old_pile, pile_hover)
                else:
                    if selected_card:
                        game.move_card(old_pile, old_pile)
                selected_card = None
                old_pile = None

        # Update game screen
        scr.game_display(game,images,selected_card,player)
        pygame.display.flip()

    # Return to main menu at the end
    scr.set_screen("main_menu")

def main_2_player():
    run = True
    clock = pygame.time.Clock()
    game = Game(0)
    player = game.players[0]
    scr.setup_game_screen(game,player)
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
             scr.set_winner_screen(player,game.winner,"2_player_win_card")
             menu()
             run = False


        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game.paused = True
                    run = paused_screen(game,images,"2player")
                    game.paused = False
                else:
                    if event.unicode not in player.inputs:
                        player = game.players[abs(player.id -1)]
                    if not player.timed_out:
                        #Pile only returned if an invalid move was made
                        pile = game.keyboard_update(player, event.unicode)
                        if pile:
                            start_new_thread(
                                time_out,
                                (player, game, images[pile._peek().name], 
                                pile._peek().pos)
                            )

            elif event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                if pile_hover != None:
                    selected_card = pile_hover._peek()
                    game.moving_sprites.add(selected_card)
                    old_pile = pile_hover
            if event.type == MOUSEBUTTONUP:
                if pile_hover != None and old_pile != None:
                    if old_pile.name[0] == "1" or old_pile.name == "side1":
                        game.mouse_update(game.players[1],old_pile,pile_hover)
                    else:
                         game.mouse_update(player,old_pile,pile_hover)
                else:
                    if selected_card != None:
                        game.move_card(old_pile,old_pile)
                selected_card = None
                old_pile = None
        scr.game_display(game,images,selected_card,"2player")

        pygame.display.flip()
    scr.set_screen("main_menu")
     
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
        scr.setup_game_screen(game,player)
    except:
        return False

    while run:
        
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            scr.set_screen("online_quit")
            menu()
            break
        if game.ready == False:
            if player.id == 0:
                scr.set_screen("waiting_for_game")
                scr.add_screen_objects([Text(ip,40).centre_abt((SCREEN_WIDTH//2,20))])

            elif player.id == 1:
                scr.set_screen("press_to_start")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN: 
                    if event.key == K_ESCAPE:
                        run = False
                    else:
                        n.send(event.unicode)
            scr.screen_display()
        elif game.paused == True:
            scr.set_screen("oppenent_paused")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN: 
                    pass
            scr.game_display(game,images,None,player)
        else:
            if not scr.is_current_screen(""):
                scr.empty()
            pile_hover = get_pile_under_mouse(game)

            if game.winner:
                scr.set_winner_screen(player,game.winner,"win_card")
                menu()
                run = False

            for event in pygame.event.get():

                if event.type == KEYDOWN: # Timeoutes online to be done server side
                    if event.key == K_ESCAPE:
                        n.send("pause")
                        run = paused_screen(game,images,player)
                        n.send("pause")
                    else:
                        n.send(event.unicode)
                elif event.type == QUIT:
                    run = False
                if event.type == MOUSEBUTTONDOWN: 
                    if pile_hover:
                        selected_card = pile_hover._peek()
                        old_pile = pile_hover
                if event.type == MOUSEBUTTONUP:
                    if pile_hover   and old_pile :
                        n.send("mouse_update:"+old_pile.name+";"+pile_hover.name)
                    else:
                        if selected_card:
                            n.send("return:"+old_pile.name)
                    selected_card = None
                    old_pile = None
                    
        
                    
            scr.game_display(game,images,selected_card,player)
        pygame.display.flip()
    scr.set_screen("main_menu")
    return True

def paused_screen(game:Game,images,display_player):
    run = True
    clock = pygame.time.Clock()
    scr.set_screen("paused")
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                   scr.empty()
                   return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in scr.buttons:
                    if button.click(pos):
                        if button.name == "Resume":
                            scr.empty()
                            return True
                        elif button.name == "Quit":
                            scr.empty()
                            return False
        
        scr.game_display(game,images,None,display_player)
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
                    if scr.is_current_screen("main_menu"):
                        exit()
                    else:
                        scr.set_screen("main_menu")
                        menu()
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    ip_valid = main_online(text) #this can be made better
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

       
        scr.screen_display()
        typed = Text("IP:"+text,80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        typed.draw(scr.win)

        pygame.display.flip()

def change_setting(button:Setting_Button):
    File = "rules.txt"
    if button.input == "max_cards_for_joker":
        options = ["3","5","10","15"]
        i = options.index(button.key)
        if i== 3:
            new_value = options[0]
        else:
            new_value = options[i + 1]
    elif button.name == "Reset to Defaults":
        with open("default.txt",'r') as file:
            data = file.readlines()
        with open("rules.txt","w") as file:
            for line in data:
                if line.strip() == "controls":
                    data = data[data.index(line) + 1:]
                    break
                else:
                    file.write(line)
        with open("controls.txt","w") as file:
            for line in data:
                    file.write(line)
    elif button.key == "True":
        new_value = False
    elif button.key == "False":
        new_value = True
    else:
        File = "controls.txt"
        scr.empty()
        scr.set_screen("change_keybind_screen")
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    new_value = event.unicode
                    run = False
            
            scr.screen_display()
            pygame.display.flip()

        
    with open(File,'r') as file:
        data = file.readlines()
    with open(File,"w") as file:
        for line in data:
            if button.line == line:
                input, value = line.strip().split(':',1)
                file.write(input + ":"+ str(new_value) + "\n")
            else:
                file.write(line)
    scr.set_screen("settings")
        
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
                    if scr.is_current_screen("main_menu"):
                        exit()
                    else:
                        scr.set_screen("main_menu")
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in scr.buttons:
                    if button.click(pos):
                        button_action(button)
        
        scr.screen_display()
        pygame.display.flip()
scr.set_screen("main_menu")
menu() 