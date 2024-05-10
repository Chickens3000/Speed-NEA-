from _cards import *

class Client:
    def __init__(self,input_type) -> None:
        self.input_type = input_type

    def update(self, pressed_keys):
        pass

class Player:
    def __init__(self,id):
        self.hand = [Pile(str(id)+"-"+str(i),8) for i in range(5)]
        self.cards = []
        self.id = id