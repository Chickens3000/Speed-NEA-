import socket
from _thread import *
import pickle
from _game import * 
from gameobjects import *
from time import sleep

games = {}
idCount = 0

def time_out(player : Player, card: Card, start_pos):
    player.timed_out = True
    sleep(0.1)
    card.pos = (card.pos[0] + 10,card.pos[1])
    sleep(0.05)
    card.pos = start_pos
    card.pos = (card.pos[0] - 10,card.pos[1])
    sleep(0.05)
    card.pos = start_pos
    card.pos = (card.pos[0] + 10,card.pos[1])
    sleep(0.05)
    card.pos = start_pos
    card.pos = (card.pos[0] - 10,card.pos[1])
    sleep(0.05)
    card.pos = start_pos
    sleep(0.05)

    player.timed_out = False

def threaded_client(conn, p, gameId):
    global idCount
    conn.sendall(pickle.dumps(games[gameId].players[p]))


    while True:
        try:
            data = conn.recv(2048).decode()
            if gameId in games:
                game= games[gameId]
                player = game.players[p]
                if not data:
                    break
                else:
                    if data != "get":
                        if data == "pause":
                            game.paused = not game.paused
                        elif data[0:6] == "update":
                            colon = data.index(":")
                            semi_colon = data.index(";")
                            for pile in game.all_piles:
                                if data[colon+1:semi_colon] == pile.name:
                                    old_pile = pile
                                if data[semi_colon+1:] == pile.name:
                                    new_pile = pile
                            game.mouse_update(old_pile,new_pile)
                        elif data[0:6] == "return":
                            for pile in game.all_piles:
                                if data[7:] == pile.name:
                                    game.move_card(pile,pile)
                        else:
                            if games[gameId].ready == False:# waits until first set of data from p1 until starting game
                                if p == 1:
                                    games[gameId].ready = True
                                    games[gameId].start_game()
                            elif player.timed_out == False:
                                _return = game.keyboard_update(player,data)
                                if _return != False:
                                    start_new_thread(time_out,(player,_return._peek(),_return._peek().pos))
                    try:
                        conn.sendall(pickle.dumps(game))
                    except Exception as E:
                        print(E)
                
            else:
                break
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


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
    conn, addr = s.accept()
    print("Connected to:", addr)
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
        games[gameId].create_sprites()
    else:
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))