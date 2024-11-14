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
class Display():
    def __init__(self) -> None:

        # Set up game window
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.texts = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.current_screen = "main_menu" 
        self.bg = self.set_background()
        self.haze = self.set_haze()
        self.diplay_haze = False

        #Screen configurations
        self.screens ={
            "main_menu" : {
                "buttons" : [Button("Singleplayer",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2- 120),80),
                       Button("2 Player",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),80),
                       Button("Settings",(160,SCREEN_HEIGHT- 80),60)],
            },
            "two_player_menu" : {
                "buttons" : [Button("Local",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2- 120),80),
                       Button("Online",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),80)]
            },
            "singleplayer_menu" : {
                "buttons" : [Button("Theo",(SCREEN_WIDTH//2-450,SCREEN_HEIGHT//2),60),
                        Button("Sophie",(SCREEN_WIDTH//2-150,SCREEN_HEIGHT//2),60),
                        Button("Harvey",(SCREEN_WIDTH//2 + 150,SCREEN_HEIGHT//2),60),
                        Button("Robin",(SCREEN_WIDTH//2 + 450,SCREEN_HEIGHT//2),60),
                        Button("Gilly",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2 + 120),60)]
            },
            "online_menu" : {
                "buttons" : [Button("Host",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2- 120),80),
                       Button("Join",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),80)]
            },
            "paused" : {
                "buttons" : [Button("Resume",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2- 120),80),
                       Button("Quit",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),80)],
                "haze" : True
            },
            "oppenent_paused" : {
                "texts" : [Text("Opponent Paused...",100).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT//2))],
                "haze" : True
                },
            "change_keybind_screen" : {
                "texts" : [Text("Press any key to change",80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2)),
                           Text("Press Esc to return to Menu",30).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT-40 ))]
            },
            "server_offline" : {
                "texts" : [Text("Server is offline at the moment",80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2)),
                           Text("Press Esc to return to Menu",30).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT-40 ))]
            },
            "online_quit" : {
                "texts" : [Text("Opponent disconnected",80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2)),
                           Text("You win?...ig?",60).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT - 200)),
                           Text("Press Esc to return to Menu",30).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT-40 ))]
            },
            "waiting_for_game" : {
                "texts" : [Text("Waiting for opponent...",80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2)),
                           Text("Press Esc to return to Menu",30).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT-40 ))]
            },
            "press_to_start" : {
                "texts" : [Text("Press any key to start.",80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2)),
                           Text("Press Esc to return to Menu",30).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT-40 ))]
            },
            "settings" : {
                "buttons": [Setting_Button(":Reset to Defaults",(SCREEN_WIDTH//2 , SCREEN_HEIGHT -100) ,60)],
                "texts" : [Text("Settings",80).centre_abt((SCREEN_WIDTH//2,50)),
                           Text("P1",60).centre_abt((50,180)),
                           Text("P2",60).centre_abt((50,270))],
                "haze" : True
            },
            "win_card" : {
                "texts" : [Text("You Win!",80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2)),
                           Text("You Lose!",80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2)),
                           Text("Press Esc to return to Menu",30).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT-40 ))],
                "haze": True
            },
            "2_player_win_card" : {
                "texts" : [Text("Player 1 Wins",80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2)),
                           Text("Player 2 Wins",80).centre_abt((SCREEN_WIDTH//2,SCREEN_HEIGHT//2)),
                           Text("Press Esc to return to Menu",30).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT-40))],
                "haze": True
            }
        }

    def set_haze(self):
        haze = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        haze.fill((128,128,128))
        haze.set_alpha(200)
        return haze
    
    def set_background(self):
        bg = pygame.image.load("./images/backround.jpg")
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return bg

    def is_current_screen(self,screen):
        if screen == self.current_screen:
            return True
        return False

    def add_screen_objects(self,objects):
        for object in objects:
            if isinstance(object,Text):
                self.texts.add(object)
            if isinstance(object,Button):
                self.buttons.add(object)
    
    def empty(self):
        self.current_screen = ""
        self.diplay_haze = False
        self.texts.empty()
        self.buttons.empty()
    
    def set_screen(self,name):
        self.empty()
        if self.current_screen == name:
            return False
        self.current_screen = name
        screen = self.screens.get(name)
        buttons,texts,haze = screen.get("buttons"),screen.get("texts"),screen.get("haze")
        if buttons:
            for button in buttons:
             self.buttons.add(button)
        if texts:
            for text in texts:
                self.texts.add(text)
        if haze:
             self.diplay_haze = True
        
        if name == "settings":
            self.setup_settings_screen()
    
    def setup_settings_screen(self):
        counter = 0
        with open("controls.txt",'r') as file:
            for line in file:
                input, key = line.strip().split(':',1)
                if input[0:2] == "p1":
                    text = Text(input.strip()[3:],50)
                    text.set_pos((SCREEN_WIDTH//2 -450-text.width//2 + 150 * counter),
                               90)
                    self.texts.add(text)
                    self.buttons.add(Setting_Button(line,(SCREEN_WIDTH//2 -450 + 150 * counter,180),40))
                elif input[0:2] == "p2":
                    self.buttons.add(Setting_Button(line,(SCREEN_WIDTH//2 -450 + 150 * counter, 270),40))

                counter += 1
                if counter ==7:
                    counter = 0
        with open("rules.txt",'r') as file:
            counter = 0
            for line in file:
                input, key = line.strip().split(':',1)
                input = input.replace("_"," ")
                text = Text(input.strip(),50)
                
                text.set_pos(20 + (400-text.width)//2 + SCREEN_WIDTH//2 * (counter % 2),
                             SCREEN_HEIGHT//2 + 75 * (counter //2))
                self.texts.add(text)
                self.buttons.add(Setting_Button(line,(SCREEN_WIDTH//2  * (counter % 2 + 1) - 90, SCREEN_HEIGHT//2 + 75 * (counter //2)+30) ,40))

                counter += 1

    def display_cards(self,game,images,selected_card):
        for entity in game.all_sprites:
            if entity.faced_up != images[entity.name].seen:
                images[entity.name].change_image()
            if selected_card:
                images[selected_card.name].move_towards(game,(pygame.Vector2(pygame.mouse.get_pos())[0]-(CARD_WIDTH/2),pygame.Vector2(pygame.mouse.get_pos())[1]-(CARD_HEIGHT/2)))
            elif entity in game.moving_sprites:
                images[entity.name].move_towards(game,entity.pos)
                
            self.win.blit(images[entity.name]._image()[0],images[entity.name]._image()[1])
        
    
    def screen_display(self):
        self.win.blit(self.bg,(0,0))
        if self.diplay_haze:
            self.win.blit(self.haze,(0,0))
        for button in self.buttons:
            button.draw(self.win)
        for text in self.texts:
            text.draw(self.win)
    
    def game_display(self,game,images,selected_card):
        self.win.blit(self.bg,(0,0))
        self.display_cards(game,images,selected_card)
        self.game_texts(game)
        if self.diplay_haze:
            self.win.blit(self.haze,(0,0))

        for button in self.buttons:
            button.draw(self.win)
        for text in self.texts:
            text.draw(self.win)
    
    def game_texts(self,game:Game):#
        if game.flip_ready[0] == True:
            text = Text("ready",50)
            text.set_pos((game.players[0].side_pile.pos[0] + CARD_WIDTH + 20),game.players[0].side_pile.pos[1])
            text.draw(self.win)
        if game.flip_ready[1] == True:
            text = Text("ready",50)
            text.set_pos((game.players[1].side_pile.pos[0] - text.width - 20),game.players[1].side_pile.pos[1])
            text.draw(self.win)
        if game.empty_hand(game.players[0]) == True or game.empty_hand(game.players[1]) == True:
            text1 = Text(game.players[0].inputs[5] + "/" +game.players[1].inputs[5],80)
            text2 = Text(game.players[0].inputs[6] + "/" +game.players[1].inputs[6           ],80)
            text1.set_pos(SCREEN_WIDTH//2-CARD_WIDTH - text1.width - 20,SCREEN_HEIGHT//2 - text1.height//2)
            text2.set_pos(SCREEN_WIDTH//2+CARD_WIDTH + 20 ,SCREEN_HEIGHT//2 - text2.height//2)
            text1.draw(self.win)
            text2.draw(self.win)
    
    def set_winner_screen(self,player,winner,screen_name):
        if screen_name == "2_player_win_card":
            screen = self.screens.get("2_player_win_card")
            screen["texts"] =  [screen["texts"][winner.id], screen["texts"][2]]
        else:
            screen = self.screens.get("win_card")
            if player.id == winner.id:
                screen["texts"] =  [screen["texts"][0], screen["texts"][2]]
                print(screen["texts"])
            else:
                screen["texts"] =  [screen["texts"][1], screen["texts"][2]]
        self.set_screen(screen_name)

class Button(pygame.sprite.Sprite):
    def __init__(self, name, pos,font_size):
        super(Button,self).__init__()
        self.name = name
        font = pygame.font.SysFont(FONT,font_size )
        self.text = font.render(name, 1, (255,255,255))
        self.width, self.height = self.text.get_width() + 70,self.text.get_height() + 20
        self.x,self.y = pos[0] - self.text.get_width()//2,pos[1] -self.text.get_height()//2

    def draw(self, win):
        pygame.draw.rect(win,(255,255,255),(self.x -35, self.y -10,self.width, self.height),5,10)
        win.blit(self.text, (self.x , self.y ))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

class Setting_Button(Button):
    def __init__(self, line,pos,font_size):
        self.line = line
        self.input, self.key = line.strip().split(':',1)
        self.input, self.key = self.input.strip(), self.key.strip()
        super(Setting_Button,self).__init__(self.key, pos,font_size)

    def click(self,pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
        

class Text(pygame.sprite.Sprite):

    def __init__(self, script,font_size):
        super(Text,self).__init__()
        font = pygame.font.SysFont(FONT,font_size)
        self.text = font.render(script, 1, (255,255,255))
        self.width,self.height = self.text.get_width(),self.text.get_height()
        self.x,self.y = 0,0

    def draw(self, win):
        win.blit(self.text, (self.x , self.y))

    def centre_abt(self,pos):
        self.x,self.y = pos[0] - self.text.get_width()//2,pos[1] -self.text.get_height()//2
        return self
    def set_pos(self,x,y):
        self.x,self.y = x,y
