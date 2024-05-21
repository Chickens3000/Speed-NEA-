from _cards import *

class Player:
    
    def __init__(self,id):
        self.hand = [Pile(str(id)+"-"+str(i),8) for i in range(5)]
        self.side_pile = Pile((str(id) + "side"),36) 
        self.cards = Pile(str(id)+"cards",52)
        self.id = id
        self.pressed_keys = None
        self.inputs = Queue()

class Queue:
    # Constructor
    def __init__(self):
        self.FrontPointer = 0
        self.BackPointer = -1
        self.Max = 4
        self.Contents = ["" for Elements in range(self.Max)]
    # Add an item to the queue
    def Enqueue(self, Item):
        print(self.Contents.count(""))
        print(self.items_in_queue())
        if self.items_in_queue() != self.Max:
            self.BackPointer = self.increment_pointer(self.BackPointer)
            self.Contents[self.BackPointer] = Item
            return True
        else:
            return False
    # Remove an item from the queue
    def Dequeue(self):
        if self.items_in_queue() == 0:
            return False
        else:
            Item = self.Contents[self.FrontPointer]
            self.Contents[self.FrontPointer] = ""
            self.FrontPointer= self.increment_pointer(self.FrontPointer)
            return Item
            
    # Look at the next item in the queue without removing it      
    def Peek(self):
        if self.items_in_queue() == 0:
            return None
        else:
            return self.Contents[self.FrontPointer]
    
    def outputQ(self):
        print(self.Contents)

    def increment_pointer(self,pointer):
        if pointer < self.Max-1:
            pointer += 1
        else:
            pointer = 0
        return pointer
    
    def items_in_queue(self):
        return (self.Max)-(self.Contents.count(""))