import socket
from _thread import *
import pickle
from _game import Game

server = "192.168.1.118"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.sendall(pickle.dumps(games[gameId].players[p]))

    reply = ""
    while True:
        try:
            data = conn.recv(2048*16).decode()

            if gameId in games:
                game = games[gameId]
                
                if not data:
                    break
                else:
                    if data != "get":
                        game.update(game.players[p], data)
                    try:
                        conn.sendall(pickle.dumps(game))
                    except Exception as E:
                        print(E)
                
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



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
        games[gameId].ready = True
        #games[gameId].create_sprites()
        games[gameId].start_game()
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))