import socket
from _thread import start_new_thread
import pickle
from _game import Game
from gameobjects import Player, Card
from time import sleep

# Dictionary to store game instances
games = {}
idCount = 0

def time_out(player: Player, card: Card, start_pos):
    """Temporarily shakes a card to indicate an invalid move."""
    player.timed_out = True
    
    for i in range(2):
        card.pos = (start_pos[0] + 10, start_pos[1])
        sleep(0.05)
        card.pos = (start_pos[0] - 10, start_pos[1])
        sleep(0.05)
    
    card.pos = start_pos
    player.timed_out = False

def threaded_client(conn, p, gameId):
    """Handles client-server communication for a game session."""
    global idCount
    
    #Send player to client
    conn.sendall(pickle.dumps(games[gameId].players[p]))
    
    while True:
        try:
            #Receive data from client
            data = conn.recv(2048).decode()
            
            #Find game from dict
            if gameId in games:
                game = games[gameId]
                player = game.players[p]
                
                if not data:
                    break
                
                if data != "get":
                    
                    #Pause/unpause Game
                    if data == "pause":
                        game.paused = not game.paused
                    
                    #Take mouse move
                    elif data.startswith("mouse_update"):
                        colon = data.index(":")
                        semi_colon = data.index(";")
                        
                        #Get params from string
                        old_pile = new_pile = None
                        for pile in game.all_piles():
                            if data[colon+1:semi_colon] == pile.name:
                                old_pile = pile
                            if data[semi_colon+1:] == pile.name:
                                new_pile = pile
                        
                        #Make move
                        move_hint_pile = game.mouse_update(player, old_pile, new_pile)
                        
                        if move_hint_pile:
                            start_new_thread(
                                time_out,
                                (player, move_hint_pile._peek(), move_hint_pile._peek().pos)
                            )
                    
                    #Return card after invalid mouse move
                    elif data.startswith("return"):
                        for pile in game.all_piles():
                            if data[7:] == pile.name:
                                game.move_card(pile, pile)
                    
                    else:
                        #Keyboard inputs

                        #Waits until first set of data from P1 before starting
                        if not games[gameId].ready:  #
                            if p == 1:
                                games[gameId].ready = True
                                games[gameId].start_game()
                        elif not player.timed_out:

                            #Make keyboard move
                            move_hint_pile = game.keyboard_update(player, data)
                            
                            if move_hint_pile:
                                start_new_thread(
                                    time_out,
                                    (player, move_hint_pile._peek(), move_hint_pile._peek().pos)
                                )
                
                try:
                    #Send game back to client
                    conn.sendall(pickle.dumps(game))
                except Exception as e:
                    print(e)
                    print("Cannot send game to client")
            else:
                break
        
        except Exception as e:
            print(e)
            print("Cannot receive data from client")
            break
    
    print("Lost connection")
    
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except KeyError:
        pass
    
    idCount -= 1
    conn.close()

# Server setup
server = socket.gethostbyname(socket.gethostname())
port = 5050
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()

while True:
    #Wait for connection
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    #Create player
    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    
    #Join game if available or begin new game
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
        games[gameId].create_sprites()
    else:
        p = 1
    
    start_new_thread(threaded_client, (conn, p, gameId))
