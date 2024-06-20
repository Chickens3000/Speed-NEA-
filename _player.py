from _cards import *

class Player:
    
    def __init__(self,id):
        self.id = id
        if self.id == 0:
            self.hand = [Pile(str(id)+"-"+str(i),8,(((i+2)*200)-300,480)) for i in range(5)]
            self.side_pile = Pile((str(id) + "side"),36,(100,230)) 
            self.cards = Pile(str(id)+"cards",52,(1300,800))
            self.inputs = ["q","w","e","r","g"]
        else:
            self.hand = [Pile(str(id)+"-"+str(i),8,(((i+2)*200)-300,10)) for i in range(5)]
            self.side_pile = Pile((str(id) + "side"),36,(956,230)) 
            self.cards = Pile(str(id)+"cards",52,(1300,-100))
            self.inputs = ["n","j","k","l",";"]
