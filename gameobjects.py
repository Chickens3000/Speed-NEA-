import pygame

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
CARD_WIDTH = 144
CARD_HEIGHT = 209
FONT = "calibri"


class Card(pygame.sprite.Sprite):
    def __init__(self, code: tuple):
        super().__init__()
        self.code = code
        self.name = self.create_name()
        self.faced_up = False
        self.start_pos = (0, 1)
        self.pos = (0, 0)

    def create_name(self):
        """
        Creates the name of the card based of the code
        Used as the key for image dictionary
        and as the name for image in images folder
        """
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
            name += f"{self.code[0]}_of_"
        
        suit_names = {"S": "spades", "H": "hearts", "C": "clubs", "D": "diamonds"}
        name += suit_names.get(self.code[1], "unknown")
        return name


class Joker(Card):
    def create_name(self):
        return "red_joker"


class Pile:
    def __init__(self, name, max_size, pos):
        """Initialize a Pile instance with a given name, maximum size, and position."""
        self.stack_pointer = -1
        self.max = max_size
        self.contents = ["" for _ in range(self.max)]
        self.name = name
        self.pos = pos

    def push(self, card: tuple, all_sprites):
        """Push a card onto the pile if there is space."""
        if self.stack_pointer < self.max - 1:
            self.stack_pointer += 1
            self.contents[self.stack_pointer] = card
            all_sprites.change_layer(sprite=card, new_layer=self.stack_pointer)
        else:
            # Print a warning if the pile is full.
            print("Stack Overflow:", self.name)
            return False

    def _pop(self):
        """Remove and return the top card from the pile if it is not empty."""
        if self.stack_pointer >= 0:
            card = self.contents[self.stack_pointer]
            self.contents[self.stack_pointer] = ""
            self.stack_pointer -= 1
            return card
        else:
            # Return False if the pile is empty.
            return False

    def _peek(self):
        """Return the top card without removing it if the pile is not empty."""
        if self.stack_pointer >= 0:
            card = self.contents[self.stack_pointer]
            return card
        else:
            return False

    def push_all(self, cards: list):
        """Push a list of cards onto the pile if there is enough space."""
        if not cards:
            return False
        if self.stack_pointer < self.max - len(cards):
            self.stack_pointer += 1
            self.contents[self.stack_pointer:self.stack_pointer + len(cards)] = cards
            self.stack_pointer += len(cards) - 1
        else:
            # Print a warning if the pile cannot fit all the cards.
            print("Stack Overflow:", self.name)
            return False

    def pop_all(self):
        """Remove and return all cards from the pile if it is not empty."""
        if self.stack_pointer >= 0:
            cards = self.contents[:self.stack_pointer + 1]
            self.contents[:self.stack_pointer + 1] = ["" for _ in range(self.stack_pointer + 1)]
            self.stack_pointer = -1
            return cards
        else:
            # Return False if the pile is empty.
            return False

    def is_empty(self):
        """Check if the pile is empty."""
        return self.stack_pointer == -1


class Deck(Pile):
    """Creates a list of all cards"""
    def create_deck(self, all_sprites: pygame.sprite.Group):
        suits = ["S", "H", "D", "C"]
        for suit in suits:
            for i in range(1, 14):
                card = Card((i, suit))
                all_sprites.add(card)
                self.push(card, all_sprites)
        return all_sprites


class Image:
    def __init__(self, card: Card):
        #Get card info
        self.card_sprite = card
        self.name = card.name
        self.image = f"./images/{self.name}.png"
        self.seen = False
        
        #Load image
        self.surf = pygame.image.load(self.image)
        self.surf = pygame.transform.scale(self.surf, (CARD_WIDTH, CARD_HEIGHT)).convert()
        self.rect = self.surf.get_rect()
        
        #Load back of card image
        self.back_surf = pygame.image.load("./images/back.png")
        self.back_surf = pygame.transform.scale(self.back_surf, (CARD_WIDTH, CARD_HEIGHT)).convert()
        self.back_rect = self.back_surf.get_rect()

    def _image(self):
        """Return card image"""
        return (self.surf, self.rect) if self.seen else (self.back_surf, self.back_rect)
    
    def change_image(self):
        """Place reverse image in same position"""
        if self.seen:
            self.back_rect.topleft = self.card_sprite.start_pos
        else:
            self.rect.topleft = self.card_sprite.start_pos
        self.seen = not self.seen
    
    def lerp(self, start, end, t):
        """Linearlly interpolates between start and end positions"""
        return start + t * (end - start)

    def move_towards(self, game, target_pos):
        """Moves the card sprite towards a target position incramentally 
        with a smooth transition."""
        surf, rect = self._image()
        speed = 40
        dist_x = target_pos[0] - rect.x
        dist_y = target_pos[1] - rect.y
        distance = (dist_x ** 2 + dist_y ** 2) ** 0.5

        if distance < speed:
            rect.topleft = target_pos
            self.card_sprite.start_pos = target_pos
            game.moving_sprites.remove(self.card_sprite)
        else:
            rect.x = self.lerp(rect.x, target_pos[0], speed / distance)
            rect.y = self.lerp(rect.y, target_pos[1], speed / distance)
