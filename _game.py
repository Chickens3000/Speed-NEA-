from _player import *
from gameobjects import *
import random

class Game():
    def __init__(self,id):
        self.id = id

        #Game states
        self.ready = False
        self.flip_ready = [False,False]
        self.winner = None
        self.paused = False

        #Game object init
        self.players = [Player(0),Player(1)]
        self.center_piles = [Pile("center0",52,(SCREEN_WIDTH//2 - CARD_WIDTH - 10,(SCREEN_HEIGHT - 2* CARD_HEIGHT - 2* 30))),Pile("center1",52,(SCREEN_WIDTH//2 + 10,(SCREEN_HEIGHT - 2* CARD_HEIGHT - 2* 30)))]
        self.deck = Deck("deck",52,(0,0))
        self.moving_sprites = pygame.sprite.Group() 
        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.rules = self.set_rules()

    def create_sprites(self):
        self.all_sprites = self.deck.create_deck(self.all_sprites)

    def all_piles(self):
        return self.center_piles + self.players[0].hand + [self.players[0].side_pile] + self.players[1].hand + [self.players[1].side_pile]

    def start_game(self):
        """
        Set up game
        -Shuffle deck
        -Deal cards
        """

        random.shuffle(self.deck.contents)

        #Split cards evenly
        self.players[0].cards.push_all(self.deck.contents[0:26])
        self.players[1].cards.push_all(self.deck.contents[26:53])

        #Move all cards to hands
        for player in self.players:
            for i in range(player.cards.stack_pointer +1 ):
                card = player.cards.contents[i]
                card.pos = player.cards.pos
                self.moving_sprites.add(card)
        
        #Start the first round
        self.next_round()
        
    def next_round(self):
        """
        Apply round setup rules
        Check for if endgame round is necessary
        """

        if self.rules["shuffle_btwn_rounds"] == "True":
            for player in self.players:
                cards = player.cards.contents[0:player.cards.stack_pointer + 1]
                random.shuffle(cards)
                player.cards.contents = [*cards,*player.cards.contents[player.cards.stack_pointer + 1:]]

        #Check for engame round        
        if (self.players[0].cards.stack_pointer + 1) > 15 and (self.players[1].cards.stack_pointer + 1) > 15:
            self.round_setup()
        else:
            self.endgame_round()
    
    def round_setup(self):
        """
        Set up and begin round
        """
        #Deal cards out into 5 piles in hand
        for player in self.players:
            for i in range(0,5):
                for x in range(5-i):
                   self.move_card(player.cards,player.hand[i])
                player.hand[i]._peek().faced_up = True
            self.move_all(player.cards,player.side_pile)
        
        #Begin round
        self.flip_cards()

    def endgame_round(self):
        """
        Handle the setup for two endgame rounds
        Introduce joker round if coniditions are met
        """

        borrow,borrower_id = False,0

        for player in self.players:
            #If player cannot produce a side pile but has too many cards for a joker round, 
            #allow player to borrow a card and set up round
            if (player.cards.stack_pointer + 1) <=15 and (player.cards.stack_pointer + 1) > int(self.rules["max_cards_for_joker"]):
                borrow,borrower_id = True,player.id
                for i in range(0,5):
                    for x in range(5-i):
                        self.move_card(player.cards,player.hand[i])
                    if player.hand[i].is_empty():
                        break
                    player.hand[i]._peek().faced_up = True

            #If player has few enough cards for joker round, set up joker round
            elif (player.cards.stack_pointer + 1) <= int(self.rules["max_cards_for_joker"]):
                for i in range(0,5):
                    for x in range(5-i):
                        self.move_card(player.cards,player.hand[i])
                    if player.hand[i].is_empty():
                        break
                    player.hand[i]._peek().faced_up = True
                player.side_pile.push(self.create_joker(),self.all_sprites) 

            #Set up round as normal
            else:
                for i in range(0,5):
                    for x in range(5-i):
                        self.move_card(player.cards,player.hand[i])
                    player.hand[i]._peek().faced_up = True
                self.move_all(player.cards,player.side_pile)
        
        #Borrow card for side pile
        if borrow == True:
            self.move_card(self.players[abs(borrower_id-1)].side_pile,self.players[borrower_id].side_pile)

        #Begin round
        self.flip_cards()


    def create_joker(self):
        joker = Joker((99,"J"))
        self.all_sprites.add(joker)
        return joker    
    
    def move_card(self, start: Pile, end: Pile):
        """Moves top card from start pile to end pile"""

        card = start._pop()

        if card:
            #Change cards position
            if end.name[:4] == "side":
                card.pos = end.pos
            
            elif end.name[:6] == "center":

                #Stagger cards in pile
                if end.stack_pointer <= 8:
                    card.pos = (end.pos[0], end.pos[1] + 2 * end.stack_pointer)
                else:
                    card.pos = (end.pos[0], end.pos[1] + 16)
            else:
                #Stagger cards in pile
                if end.stack_pointer <= 8:
                    card.pos = (end.pos[0], end.pos[1] + 4 * end.stack_pointer)
                else:
                    card.pos = (end.pos[0], end.pos[1] + 32)
            
            #Move card to new stack
            end.push(card, self.all_sprites)
            
            
            self.moving_sprites.add(card)
        

    def move_all(self, start: Pile, end: Pile):
        """Moves all cards from one pile to the top of a new pile."""
        card = start._pop()
        while card:
            end.push(card, self.all_sprites)
            card.pos = end.pos
            self.moving_sprites.add(card)
            card = start._pop()

    def flip_cards(self):
        """Flips the top card of each player's side pile to the centre"""

        #Move cards from side
        if not self.players[0].side_pile.is_empty():
            self.move_card(self.players[0].side_pile, self.center_piles[0])
        
        if not self.players[1].side_pile.is_empty():
            self.move_card(self.players[1].side_pile, self.center_piles[1])
        
        #Turn cards face up
        for pile in self.center_piles:
            if not pile.is_empty():
                pile._peek().faced_up = True
        
        self.flip_ready = [False, False]

    def end_round(self):
        """
        Handles end of round
        Collects cards from hand/side back up
        """
        for player in self.players:
            #Return all cards from side pile
            player.cards.push_all(player.side_pile.pop_all())

            #Return all  hands from stack
            for stack in player.hand:
                player.cards.push_all(stack.pop_all())

            #Make all cards faced down
            for i in range(player.cards.stack_pointer + 1):
                player.cards.contents[i].faced_up = False
            
            #Adjust opponent difficulty
            if isinstance(player, AdaptiveOpponent):
                player.edit_delay()
        
        #Starts next round
        self.next_round()

    def mouse_update(self, player: Player, old_pile: Pile, new_pile: Pile):
        """
        Handles all card-mouse interactions
        Returns a pile with an available move if side pile is clicked unecessarily 
        """
        
        if old_pile.is_empty():
            return None
        
        # Player's side pile clicked: ready for flip/get hint
        if old_pile.name == "side" + str(player.id):
            move_hint_pile = self.check_for_moves(player)
            self.move_card(old_pile, old_pile)
            return move_hint_pile
        
        #Either centre pile clicked: slam
        if old_pile.name[:6] == "center":
            self.slam(self.players[0], old_pile)
            self.move_card(old_pile, old_pile)
            return None
        
        #Pile not in player's hand: return card to pile
        if old_pile.name[0] != str(player.id):
            self.move_card(old_pile, old_pile)
            return None
        
        #Card in hand is faced down: flip and return card to pile
        if not old_pile._peek().faced_up:
            old_pile._peek().faced_up = True
            self.move_card(old_pile, old_pile)
            return None
        
        #Destination pile in same hand is empty: Move all faced up cards
        if new_pile.is_empty() and new_pile.name[:4] != "side" and new_pile.name[0] == old_pile.name[0]:
            while old_pile._peek() and old_pile._peek().faced_up:
                self.move_card(old_pile, new_pile)
            return None
        
        #Destination pile's top card is faced down: Return card to pile
        if not new_pile._peek().faced_up:
            self.move_card(old_pile, old_pile)
            return None
        
        #Valid move to centre: Move card and reset flip ready
        if self.move_is_valid(old_pile._peek(), new_pile._peek()) and new_pile.name[:6] == "center":
            self.move_card(old_pile, new_pile)
            self.flip_ready = [False, False]
            return None
        
        #Piles are in the same hand
        if new_pile.name[0] == old_pile.name[0]:

            #Destination pile in hand is empty: Move all faced up cards (shift)
            if new_pile.is_empty() and new_pile.name[:4] != "side" and new_pile.name[0] == old_pile.name[0]:
                while old_pile._peek() and old_pile._peek().faced_up:
                    self.move_card(old_pile, new_pile)
                return None
            
            #Top card of destination matches number of top card: Move all faced up cards (stack)
            if old_pile._peek().code[0] == new_pile._peek().code[0]:
                while old_pile._peek() and old_pile._peek().faced_up:
                    self.move_card(old_pile, new_pile)
                return None
        
        #If no valid move is made, return card top pile
        self.move_card(old_pile, old_pile)




    def keyboard_update(self, player: Player, data: str):
        """
        Takes a key from the keyboard and makes move according
        Returns pile if theres an invalid move
        """
        #Match input to pile in hand
        if data in player.inputs[:5]:
            pile = player.hand[player.inputs.index(data)]
        
        #Slam correct pile on input
        elif data == player.inputs[5]:
            self.slam(player, self.center_piles[0])
            return False
        elif data == player.inputs[6]:
            self.slam(player, self.center_piles[1])
            return False
        else:
            #Return false if key is not in inputs
            return False
        
        #Play the card from that pile
        return self.play_card(pile, player)

    def play_card(self, pile, player):
        """
        Handles playing a card from a given pile.
        Prioritises playing to the centre
        then stacking,then shifting cards
        """

        #Pile is empty: return False
        if not pile._peek():
            return False
        
        #Card is faced down: Turn card faced up
        if not pile._peek().faced_up:
            pile._peek().faced_up = True
            return False
        
        #Card can play to one of the centre piles: Play
        for centre_pile in self.center_piles:
            if self.move_is_valid(pile._peek(), centre_pile._peek()):
                self.move_card(pile, centre_pile)
                self.flip_ready = [False, False]
                return False
        
        #Card can stack onto a pile in hand with the same number: Stack card
        if self.check_stack(pile, player):
            hand = self.check_stack(pile, player)
            while pile._peek() and pile._peek().faced_up:
                self.move_card(pile, hand)
            return False
        
        #Empty pile in hand: Shit cards
        if self.check_shift_cards(player):
            hand = self.check_shift_cards(player)
            while pile._peek() and pile._peek().faced_up:
                self.move_card(pile, hand)
            return False
        
        #Retrun pile if no moves can be made
        return pile

    def move_is_valid(self, card: Card, top_card: Card):
        """Checks if card can be played to the centre based on game rules."""

        #Check moves against rules
        if self.rules["play_same_colour"] == "False" and self.same_colour(top_card, card):
            return False
        if self.rules["play_same_number"] == "True" and top_card.code[0] == card.code[0]:
            return True
        
        #Check difference in card value is either one or 12
        return abs(top_card.code[0] - card.code[0]) in [1, 12]

    def same_colour(self, card1, card2):
        """Determines if two cards are the same color."""
        return ((card1.code[1] in "HD" and card2.code[1] in "HD") or
                (card1.code[1] in "CS" and card2.code[1] in "CS"))

    def check_stack(self, pile: Pile, player: Player):
        """Return a pile in hand which has the same top-card-value"""
        for hand in player.hand:
            top_card = hand._peek()
            if not top_card or pile == hand:
                continue
            if pile._peek().code[0] == top_card.code[0] and top_card.faced_up:
                return hand
        return False

    def check_shift_cards(self, player: Player):
        """Moves cards to an empty pile if possible."""
        for stack in player.hand:
            if stack.is_empty():
                return stack
        return False

    def check_for_moves(self, player: Player):
        """Checks if any valid moves are available for a player."""
        #Check every stack in hand
        for stack in player.hand:

            if stack.is_empty():
                continue

            #Check if player can play to centre
            for centre_pile in self.center_piles:
                if self.move_is_valid(stack._peek(), centre_pile._peek()):
                    return stack
                
            #Check if player can face up a card
            if not stack._peek().faced_up:
                return stack
            
            #Check if player can stack a card to a different pile
            if self.check_stack(stack, player):
                return stack
            
            #Check if player can shift cards
            #Only do this if it will reveal face down cards further in the pile
            #Otherwise towards the end of the round users will always be able to shift cards
            if self.check_shift_cards(player) and not stack.contents[0].faced_up:
                return stack
        
        #Check if the player has no cards
        if self.empty_hand(player):
            return False
        
        #If no move is available, set the players flip ready to true
        #If both are ready, or the other players side pile is empty, flip cards
        self.flip_ready[player.id] = True
        if self.players[abs(player.id - 1)].side_pile.is_empty():
            self.check_for_moves(self.players[abs(player.id - 1)])
        elif self.flip_ready[abs(player.id - 1)]:
            self.flip_cards()
        return False

    def slam(self, player: Player, pile: Pile):
        """Handles the slam and end of round"""
        id = int(pile.name[6])
        
        #Only slam if either pile is empty
        if (self.empty_hand(self.players[0]) or self.empty_hand(self.players[1])) and pile.name[:6] == "center":

            #Check if player has won
            if pile._peek().name == "red_joker":
                if self.check_for_win(player):
                    self.winner = player
                else:
                    #Remove joker
                    self.all_sprites.remove(pile._peek())
                    pile._pop()
            elif self.center_piles[abs(id - 1)]._peek().name == "red_joker":
                #Remove joker
                self.all_sprites.remove(self.center_piles[abs(id - 1)]._peek())
                self.center_piles[abs(id - 1)]._pop()
            
            #Distrobute cards from centre piles
            self.move_all(self.center_piles[id], player.cards)
            self.move_all(self.center_piles[abs(id - 1)], self.players[abs(player.id - 1)].cards)

            self.end_round()

    def check_for_win(self, player: Player):
        """Checks if a player has won the game."""
        return self.empty_hand(player) and player.side_pile.is_empty()

    def empty_hand(self, player: Player):
        """Checks if a player's hand is empty."""
        return all(not stack._peek() for stack in player.hand)

    def set_rules(self):
        """Loads game rules from a file into rules dict"""
        rules = {}
        with open("textfiles/rules.txt", 'r') as file:
            for line in file:
                rule, value = line.strip().split(':', 1)
                rules[rule.strip()] = value.strip()
        return rules
