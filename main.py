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
    
    This function checks if the mouse position is within the bounds of any
    pile in the game and returns that pile.
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
    
    The player's card is animated to move slightly and return to the start
    position to visually indicate the time-out.
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
    
    Depending on the button clicked, different game modes or menus are
    launched.
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
    """
    Run single player game

    This function manages user inputs, changes to the game state and
    displaying changes to the user

    It also manages the AI opponent and its changes to the game
    """
    # Initial setup
    run = True
    clock = pygame.time.Clock()
    game = Game(0)
    player = game.players[0]
    selected_card = None
    old_pile = None

    # Setup AI opponent
    if delay == -1:
        game.players[1] = AdaptiveOpponent(2000)
    else:
        game.players[1] = Opponent(delay)

    AI_MOVE = pygame.USEREVENT + 1
    AI_FLIP = pygame.USEREVENT + 2  # AI flip occurs at a random set interval, allows AI to have "2 hands"
    pygame.time.set_timer(AI_MOVE, game.players[1].delay)
    pygame.time.set_timer(AI_FLIP,game.players[1].delay // 2 + random.randint(10, 25) * 17)

    # Create game display and start the game
    scr.setup_game_screen(game,player)
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

        # Adjust adaptive AI timers 
        if game.players[1].delay != delay:
            pygame.time.set_timer(AI_MOVE, game.players[1].delay)
            pygame.time.set_timer(
                AI_FLIP,
                game.players[1].delay // 2 + random.randint(10, 25) * 17
            )
            delay = game.players[1].delay


        for event in pygame.event.get():

            if event.type == KEYDOWN:
                #Handle pausing
                if event.key == K_ESCAPE:
                    game.paused = True
                    run = paused_screen(game,images,player)
                    game.paused = False
                else:
                    #Send move to game
                    if not player.timed_out:
                        move_hint_pile = game.keyboard_update(player, event.unicode.lower())
                        if move_hint_pile:  #Hint only returned if an invalid move was made. Timeout started
                            start_new_thread(
                                time_out,
                                (player, game, images[move_hint_pile._peek().name], 
                                move_hint_pile._peek().pos)
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
                    old_pile = pile_hover

            if event.type == MOUSEBUTTONUP:
                #Move card on release
                if pile_hover and old_pile:
                    move_hint_pile = game.mouse_update(player,old_pile, pile_hover)
                    if move_hint_pile: #Hint only returned if an invalid move was made. Timeout started 
                        start_new_thread(
                                time_out,
                                (player,game, images[move_hint_pile._peek().name], 
                                move_hint_pile._peek().pos)
                            )
                elif selected_card:
                    game.move_card(old_pile, old_pile)
                    
                selected_card = None
                old_pile = None

        # Update game screen
        scr.game_display(game,images,selected_card,player)
        pygame.display.flip()

    # Return to main menu after end/quit 
    scr.set_screen("main_menu")

def main_2_player():
    """
    Run two player game

    This function manages user inputs, changes to the game state and
    displaying changes to the user

    It also differentiates between two users inputs on the same devices
    """
    run = True
    clock = pygame.time.Clock()
    game = Game(0)
    player = game.players[0]
    selected_card = None
    old_pile = None
    
    # Create game display and start the game
    scr.setup_game_screen(game,player)
    game.create_sprites()
    game.start_game()
    
    #load images for cards
    for card in game.deck.contents:
        images[card.name] = Image(card)
    images["red_joker"] = Image(Joker((99, "J")))
    
    #Main game loop
    while run:
        pile_hover = get_pile_under_mouse(game)
        clock.tick(60)
        
        #Check for winner
        if game.winner:
            scr.set_winner_screen(player, game.winner, "2_player_win_card")
            menu()
            run = False
        

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #Handle pausing
                if event.key == K_ESCAPE:
                    game.paused = True
                    run = paused_screen(game, images, "2player")
                    game.paused = False
                else:
                    #Change which player made the move based of input
                    if event.unicode.lower() not in player.inputs:
                        player = game.players[abs(player.id - 1)]
                    
                    #Send move to game
                    if not player.timed_out:
                        move_hint_pile = game.keyboard_update(player, event.unicode.lower())
                        if move_hint_pile:  #Hint only returned if an invalid move was made. Timeout started
                            start_new_thread(
                                time_out,
                                (
                                    player, game, images[move_hint_pile._peek().name],
                                    move_hint_pile._peek().pos
                                )
                            )
            
            elif event.type == QUIT:
                run = False
            
            elif event.type == MOUSEBUTTONDOWN:
                #Select card on click
                if pile_hover:
                    selected_card = pile_hover._peek()
                    old_pile = pile_hover
            
            elif event.type == MOUSEBUTTONUP:
                #Move card on release
                if pile_hover and old_pile:
                    if old_pile.name[0] == "1" or old_pile.name == "side1":
                        move_hint_pile = game.mouse_update(game.players[1], old_pile, pile_hover)
                    else:
                        move_hint_pile = game.mouse_update(player, old_pile, pile_hover)
                    
                    if move_hint_pile:  #Hint only returned if an invalid move was made. Timeout started
                        start_new_thread(
                            time_out,
                            (
                                player if old_pile.name[0] != "1" else game.players[1],
                                game, images[move_hint_pile._peek().name],
                                move_hint_pile._peek().pos
                            )
                        )
                
                elif selected_card:
                    game.move_card(old_pile, old_pile)
                
                selected_card = None
                old_pile = None
        
        #Update display
        scr.game_display(game, images, selected_card, "2player")
        pygame.display.flip()
    
    #Return to main menu after end/quit
    scr.set_screen("main_menu")


def main_online(HostIP):
    """
    Run online game.

    This function manages sending requests to server, receiving the game
    state and displaying changes to the user
    """
    game: Game
    run = True
    clock = pygame.time.Clock()
    n = Network()
    selected_card = None
    old_pile = None

    #Set IP for connection
    if HostIP == "Host":
        #Runs server on host device
        run_server_script()

    ip = n.set_ip(HostIP)
    player = n.getP()
    
    #Establish connection and receive game
    try:
        game = n.send("get")
        
        for card in game.deck.contents:
            images[card.name] = Image(card)
        
        images["red_joker"] = Image(Joker((99, "J")))
        scr.setup_game_screen(game, player)
    
    except:
        #Exit and return False if no connection established
        return False
    
    #Main game loop
    while run:
        clock.tick(60)
        
        #Handle lost connection to the server. Displays online quit screen
        try:
            game = n.send("get")
        except:
            run = False
            scr.set_screen("online_quit")
            menu()
            break
        
        
        if not game.ready:
            #Display waiting screen until player 2 joins
            if player.id == 0:
                scr.set_screen("waiting_for_game")
                scr.add_screen_objects([Text(ip, 40).centre_abt((SCREEN_WIDTH // 2, 20))])
            
            #Display player 2 screen until ready to start
            elif player.id == 1:
                scr.set_screen("press_to_start")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                elif event.type == KEYDOWN:
                    #Quit
                    if event.key == K_ESCAPE:
                        run = False
                    else:
                        #Send input to start game to server
                        n.send(event.unicode.lower())
            
            scr.screen_display()
        
        #Pause game if opponent pauses
        elif game.paused:
            scr.set_screen("oppenent_paused")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            scr.game_display(game, images, None, player)
        
            #Normal game loop
        
        else:
            #Remove all previous screen objects
            if not scr.is_current_screen(""):
                scr.empty()
            
            pile_hover = get_pile_under_mouse(game)
            
            #Check for winner
            if game.winner:
                scr.set_winner_screen(player, game.winner, "win_card")
                menu()
                run = False
            
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    #Handle pausing
                    if event.key == K_ESCAPE:
                        n.send("pause")
                        run = paused_screen(game, images, player)
                        n.send("pause")
                    else:
                        #Send move to server
                        n.send(event.unicode.lower())
                
                elif event.type == QUIT:
                    run = False
                
                elif event.type == MOUSEBUTTONDOWN:
                    #Select card on click
                    if pile_hover:
                        selected_card = pile_hover._peek()
                        old_pile = pile_hover
                
                elif event.type == MOUSEBUTTONUP:
                    #Send mouse move to server
                    if pile_hover and old_pile:
                        n.send(f"mouse_update:{old_pile.name};{pile_hover.name}")
                    
                    elif selected_card:
                        n.send(f"return:{old_pile.name}")
                    
                    selected_card = None
                    old_pile = None

            #update game screen
            scr.game_display(game, images, selected_card, player)
        pygame.display.flip()
    
    #Return to main menu after end/quit
    scr.set_screen("main_menu") 
    return True 


def paused_screen(game: Game, images, display_player):
    """Display pause screen and allow user to quit game"""
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
                    #Returns back to game
                    return True
            
            #Decide which button is pressed on mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                for button in scr.buttons:
                    if button.click(pos):
                        if button.name == "Resume":
                            #Returns back to game
                            scr.empty()
                            return True
                        elif button.name == "Quit":
                            #Quits game
                            scr.empty()
                            return False
        
        #Updates screen
        scr.game_display(game, images, None, display_player)
        pygame.display.flip()


def join_menu():
    """
    Screen which allows the user to enter an IP and attmept to connect.
    This can be done as many times until valid
    """
    scr.empty()
    run = True
    clock = pygame.time.Clock()
    ip_valid = False
    text = ""
    
    #Ensuring correct IP
    while not ip_valid:
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

                #Try to connect with IP. If fails, display error message to
                #screen
                elif event.key in [K_RETURN, K_KP_ENTER]:
                    ip_valid = main_online(text)
                    
                    if not ip_valid:
                        text = ""
                        invalid_text = Text("Server with this IP does not exist", 60)
                        invalid_text.set_pos(SCREEN_WIDTH // 2 - invalid_text.width // 2, SCREEN_HEIGHT // 2 - invalid_text.height // 2 - 200)
                        scr.texts.add(invalid_text)

                #Takes users IP input as text               
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
                elif event.key == K_SPACE or event.unicode == "":
                    pass
                else:
                    text += event.unicode.lower()
        
        #Update display with typed text
        scr.screen_display()
        typed = Text("IP:" + text, 80).centre_abt((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        typed.draw(scr.win)
        
        pygame.display.flip()


def change_setting(button: Setting_Button):
    """
    Change settings
    
    This function takes the setting button pressed as a paramater and makes
    changes to either the rules or controls accordingly
    """
    #Iterate through options for the maximum number of cards, in a hand,
    #required for a joker round
    if button.input == "max_cards_for_joker":
        options = ["3", "5", "10", "15"]
        i = options.index(button.key)
        new_value = options[0] if i == 3 else options[i + 1]
        edited_file = "textfiles/rules.txt"
    
    #Toggles boolean settings 
    elif button.key == "True":
        new_value = False
        edited_file = "textfiles/rules.txt"
    elif button.key == "False":
        new_value = True
        edited_file = "textfiles/rules.txt"
    
    #Resets all settings files values to the default file values
    elif button.name == "Reset to Defaults":
        with open("textfiles/default.txt", 'r') as file:
            data = file.readlines()
        
        with open("textfiles/rules.txt", "w") as file:
            for line in data:
                #The string controls is used as a divider between rules and
                #controls
                if line.strip() == "controls": 
                    data = data[data.index(line) + 1:]
                    break
                else:
                    file.write(line)
        
        with open("textfiles/controls.txt", "w") as file:
            for line in data:
                file.write(line)
        edited_file = None
    
    #Changes keybind
    else:
        edited_file = "textfiles/controls.txt"
        run = True
        clock = pygame.time.Clock()

        #Changes to set keybind screen
        scr.empty()
        scr.set_screen("change_keybind_screen")

        #Waits for a new input to change it to
        while run:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == KEYDOWN:
                    new_value = event.unicode.lower()
                    run = False
            
            scr.screen_display()
            pygame.display.flip()
    
    #Rewite edited file
    if edited_file:
        with open(edited_file, 'r') as file:
            data = file.readlines()
        
        with open(edited_file, "w") as file:
            for line in data:
                if button.line == line:
                    input, value = line.strip().split(':', 1)
                    file.write(input + ":" + str(new_value) + "\n")
                else:
                    file.write(line)
    
    #Redraw settings screen
    scr.set_screen("settings")


def menu():
    """
    A default template for menus

    Each menu has its own objects, texts and buttons which are loaded
    before the function is called

    This function displays all objects and, on click, checks if any button
    has been clicked

    """
    run = True
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            #Handle quits
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if scr.is_current_screen("main_menu"):
                        exit()
                    else:
                        scr.set_screen("main_menu")
            
            #Check for a button being pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                for button in scr.buttons:
                    if button.click(pos):
                        button_action(button)
        
        #Update display
        scr.screen_display()
        pygame.display.flip()


#Main program starts
scr.set_screen("main_menu")
menu()
