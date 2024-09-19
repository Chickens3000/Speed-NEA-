import pygame
from _game import * 
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    QUIT,
)

class ScreenCard():
    def __init__(self) -> None:
        self.texts = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.screen = "main_menu"
    
    def empty(self):
        self.texts.empty()
        self.buttons.empty()

    def main_menu(self):
        self.empty()
        self.buttons.add(Button("Singleplayer",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2- 120),80),
                       Button("2 Player",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),80))
        self.screen = "main_menu"
    def two_player_menu(self):
        self.empty()
        self.buttons.add(Button("Local",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2- 120),80),
                       Button("Online",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),80))
        self.screen = "two_player_menu"
    def singleplayer_menu(self):
        self.empty()
        self.buttons.add(Button("Theo",(SCREEN_WIDTH//2-450,SCREEN_HEIGHT//2),60),
                        Button("Sophie",(SCREEN_WIDTH//2-150,SCREEN_HEIGHT//2),60),
                        Button("Harvey",(SCREEN_WIDTH//2 + 150,SCREEN_HEIGHT//2),60),
                        Button("Robin",(SCREEN_WIDTH//2 + 450,SCREEN_HEIGHT//2),60),
                        Button("Gilly",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2 + 120),60))
        self.screen = "singleplayer_menu"

    def online_menu(self):
        self.empty()
        self.buttons.add(Button("Host",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2- 120),80),
                       Button("Join",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),80))
        self.screen = "online_menu"
    def win_card(self,winner,player):
        self.empty()
        if player.id == winner.id:
            text = Text(("Player"+str(player.id +1)+" Wins!!"),80)
        else:
            text = Text(("Unlucky, Player"+str(player.id +1)+" Wins!"),80)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT//2 - text.height//2)
        self.texts.add(text)
        text = Text("Press Esc to return to Menu",30)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT - text.height-40)
        self.texts.add(text)
        self.screen = "win_card"

    def server_offline(self):
        self.empty()
        text = Text("Server is offline at the moment",100)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT//2 - text.height//2)
        self.texts.add(text)
        text = Text("Press Esc to return to Menu",30)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT - text.height-40)
        self.texts.add(text)
        self.screen = "server_offline"
    
    def online_quit(self):
        self.empty()
        text = Text("Opponent disconnected",100)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT//2 - text.height//2)
        self.texts.add(text)
        text = Text("You win?...ig?",60)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT - text.height - 200)
        self.texts.add(text)
        text = Text("Press Esc to return to Menu",30)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT - text.height-40)
        self.texts.add(text)
        self.screen = "Online_quit"
        
    def paused(self):
        self.buttons.add(Button("Resume",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2- 120),80),
                       Button("Quit",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),80))
        self.screen = "paused"
    
    def opponent_paused(self,game,images,win,bg):
        self.empty()
        win.blit(bg,(0,0))
        self.display_cards(game,images,win,None)
        haze =pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        haze.fill((128,128,128))
        haze.set_alpha(200)
        win.blit(haze,(0,0))
        text = Text("Opponent Paused...",100)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT//2-text.height//2)
        text.draw(win)


    def waiting_for_game(self,win,bg,ip):
        self.empty()
        win.blit(bg,(0,0))
        text = Text("Waiting for opponent...",100)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT//2-text.height//2)
        text.draw(win)
        text = Text("IP:"+str(ip),40)
        text.set_pos(SCREEN_WIDTH - text.width,0)
        text.draw(win)
        text = Text("Press Esc to return to Menu",30)
        text.set_pos(SCREEN_WIDTH//2 - text.width//2,SCREEN_HEIGHT - text.height-40)
        text.draw(win)
        self.screen = "waiting_for_game"

    def display(self,win):
        for item in self.texts:
            item.draw(win)
        for item in self.buttons:
            item.draw(win)
    
    def game_texts(self,game:Game,win):
        if game.flip_ready[0] == True:
            text = Text("ready",50)
            text.set_pos((game.players[0].side_pile.pos[0] + CARD_WIDTH + 20),game.players[0].side_pile.pos[1])
            text.draw(win)
        if game.flip_ready[1] == True:
            text = Text("ready",50)
            text.set_pos((game.players[1].side_pile.pos[0] - text.width - 20),game.players[1].side_pile.pos[1])
            text.draw(win)
        if game.empty_hand(game.players[0]) == True or game.empty_hand(game.players[1]) == True:
            text1 = Text(game.players[0].inputs[5] + "/" +game.players[1].inputs[5],80)
            text2 = Text(game.players[0].inputs[6] + "/" +game.players[1].inputs[6           ],80)
            text1.set_pos(SCREEN_WIDTH//2-CARD_WIDTH - text1.width - 20,SCREEN_HEIGHT//2 - text1.height//2)
            text2.set_pos(SCREEN_WIDTH//2+CARD_WIDTH + 20 ,SCREEN_HEIGHT//2 - text2.height//2)
            text1.draw(win)
            text2.draw(win)
    
    def display_cards(self,game,images,win,selected_card):
         for entity in game.all_sprites:
                if entity.faced_up != images[entity.name].seen:
                    images[entity.name].change_image()
                if selected_card:
                    game.moving_sprites.add(selected_card)
                    images[selected_card.name].move_towards(game,(pygame.Vector2(pygame.mouse.get_pos())[0]-(CARD_WIDTH/2),pygame.Vector2(pygame.mouse.get_pos())[1]-(CARD_HEIGHT/2)))
                elif entity in game.moving_sprites:
                    images[entity.name].move_towards(game,entity.pos)
                    
                win.blit(images[entity.name]._image()[0],images[entity.name]._image()[1])
        
        
        





class Button(pygame.sprite.Sprite):
    def __init__(self, name, pos,font_size):
        super(Button,self).__init__()
        self.name = name
        font = pygame.font.SysFont(FONT,font_size )
        self.text = font.render(name, 1, (255,255,255))
        self.width, self.height = self.text.get_width() + 70,self.text.get_height() + 20
        self.x,self.y = self.repos(pos)

    def draw(self, win):
        pygame.draw.rect(win,(255,255,255),(self.x, self.y,self.width, self.height),5,10)
        win.blit(self.text, (self.x + round(self.width/2) - round(self.text.get_width()/2), self.y + round(self.height/2) - round(self.text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

    def repos(self,pos):
        new_pos = (pos[0]- self.width//2,pos[1]- self.height//2)
        return new_pos



class Text(pygame.sprite.Sprite):

    def __init__(self, script,font_size):
        super(Text,self).__init__()
        font = pygame.font.SysFont(FONT,font_size)
        self.text = font.render(script, 1, (255,255,255))
        self.width,self.height = self.text.get_width(),self.text.get_height()
        self.x,self.y = 0,0

    def draw(self, win):
        win.blit(self.text, (self.x , self.y))

    def set_pos(self,x,y):
        self.x,self.y = x,y
