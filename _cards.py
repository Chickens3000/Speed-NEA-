class Card:
    def __init__(self, code:tuple):
        self.code = code
        self.name = self.create_name()
        self.image = self.name + ".png"
        self.seen = True

    def create_name(self):
        name = ""

        if self.code[0] == 1:
            name += "ace_of_"
        elif self.code[0] == 11:
            name += "jack_of_"
        elif self.code[0] == 12:
            name += "queen_of_"
        elif self.code[0] == 13:
            name += "king_of_"
        else:
            name += str(self.code[0]) +"_of_"
        
        if self.code[1] == "S":
            name+= "spades"
        elif self.code[1] == "H":
            name+= "hearts"
        elif self.code[1] == "C":
            name+= "clubs"
        elif self.code[1] == "D":
            name+= "diamonds"
        return name
        
class Pile:
    def __init__(self,name,max) -> None:
        self.stack_pointer = -1
        self.max = max
        self.contents = ["" for Elements in range(self.max)]
        self.name = name

    def push(self, card: tuple):
        if self.stack_pointer < self.max -1:
            self.stack_pointer += 1
            self.contents[self.stack_pointer] = card
        else:
            print("Stack Overflow:",self.name)
            return False
    
    def pop(self):
        if self.stack_pointer >= 0:
            self.stack_pointer -= 1
            card = self.contents[self.stack_pointer + 1]
            return card
        else:
            return None
    
    def peek(self):
      if self.stack_pointer >= 0:
        card = self.contents[self.stack_pointer]
        return card

class Deck(Pile):
    def create_deck(self):
        suits =["S","H","D","C"]
        for suit in suits:
            for i in range(1,14):
                self.push(Card((i,suit)))