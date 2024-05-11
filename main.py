from _game import * 

Game1 = Game(0)
Game1.start_game()
Game1.start_round()
print(Game1.players[1].side_pile.stack_pointer)
for pile in Game1.players[1].hand:
    print(pile.stack_pointer)
#13 cards in side pile