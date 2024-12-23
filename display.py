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
                       Button("Settings",(160,SCREEN_HEIGHT- 80),60),
                       Button("How to Play",(SCREEN_WIDTH -220,SCREEN_HEIGHT- 80),60)],
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
            },
            "H2P page 1" : {
                "texts" : [BlockofText("how2play_pg1.txt",25)],
                "buttons": [Button("Next Page",(SCREEN_WIDTH//2,SCREEN_HEIGHT- 65),50)],
                "haze": True
            },
            "H2P page 2" : {
                "texts" : [BlockofText("how2play_pg2.txt",25),
                           Text("Press Esc to return to Menu",30).centre_abt((SCREEN_WIDTH//2 ,SCREEN_HEIGHT-40))],
                "haze": True
            }
        }
        self.game_texts = {}


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
    def setup_game_screen(self,game:Game,display_player:Player):
        self.game_texts = {
            "p1ready" : Text("ready",50).set_pos((game.players[0].side_pile.pos[0] + CARD_WIDTH + 20),game.players[0].side_pile.pos[1]),
            "p2ready" : Text("ready",50).set_pos((game.players[1].side_pile.pos[0] - 133),game.players[1].side_pile.pos[1]),
            "2player_slam": [Input_Button((game.players[0].inputs[5] + "/" +game.players[1].inputs[5]),
                                          (game.center_piles[0].pos[0] + CARD_WIDTH//2,game.center_piles[0].pos[1] +CARD_HEIGHT),
                                          50),
                             Input_Button(game.players[0].inputs[6] + "/" +game.players[1].inputs[6],
                                          (game.center_piles[1].pos[0] + CARD_WIDTH//2,game.center_piles[1].pos[1] +CARD_HEIGHT),
                                          50)],
            "slam": [Input_Button(display_player.inputs[5],
                                 (game.center_piles[0].pos[0] + CARD_WIDTH//2,game.center_piles[0].pos[1] +CARD_HEIGHT),
                                  50),
                     Input_Button(display_player.inputs[6],
                                 (game.center_piles[1].pos[0] + CARD_WIDTH//2,game.center_piles[1].pos[1] +CARD_HEIGHT),
                                  50)],
            "player1_controls" : [Input_Button(game.players[0].inputs[i],(game.players[0].hand[i].pos[0] + CARD_WIDTH//2,game.players[0].hand[i].pos[1] +CARD_HEIGHT),30) for i in range(len(game.players[0].hand))],
            "player2_controls" : [Input_Button(game.players[1].inputs[i],(game.players[1].hand[i].pos[0] + CARD_WIDTH//2,game.players[1].hand[i].pos[1] +CARD_HEIGHT),30) for i in range(len(game.players[1].hand))]
        }
    def display_cards(self,game,images,selected_card):
        for entity in game.all_sprites:
            if entity.faced_up != images[entity.name].seen:
                images[entity.name].change_image()
            if selected_card:
                images[selected_card.name].move_towards(game,(pygame.Vector2(pygame.mouse.get_pos())[0]-(CARD_WIDTH/2),pygame.Vector2(pygame.mouse.get_pos())[1]-(CARD_HEIGHT/2)))
            if entity in game.moving_sprites:
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
    
    def game_display(self,game,images,selected_card,display_player):
        self.win.blit(self.bg,(0,0))
        self.display_cards(game,images,selected_card)
        self.display_game_texts(game,display_player)
        if self.diplay_haze:
            self.win.blit(self.haze,(0,0))

        for button in self.buttons:
            button.draw(self.win)
        for text in self.texts:
            text.draw(self.win)
    
    def display_game_texts(self,game:Game,display_player:Player):#
        if game.flip_ready[0] == True:

            self.game_texts["p1ready"].draw(self.win)
        if game.flip_ready[1] == True:
            self.game_texts["p2ready"].draw(self.win)
        if game.empty_hand(game.players[0]) == True or game.empty_hand(game.players[1]) == True:
            if display_player == "2player":
                for button in self.game_texts["2player_slam"]:
                    button.draw(self.win)
            else:
                for button in self.game_texts["slam"]:
                    button.draw(self.win)
        if display_player == "2player":
            for button in self.game_texts["player1_controls"]:
                    button.draw(self.win)
            for button in self.game_texts["player2_controls"]:
                    button.draw(self.win)
        elif display_player.id == 0:
            for button in self.game_texts["player1_controls"]:
                    button.draw(self.win)
        elif display_player.id == 1:
            for button in self.game_texts["player2_controls"]:
                    button.draw(self.win)

    
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
        
class Input_Button(Button):
    def __init__(self, name, pos, font_size):
        super().__init__(name, pos, font_size)

    def draw(self, win):
        s = pygame.Surface((self.width-9,self.height-9))
        s.set_alpha(200)
        s.fill((128,128,128))               
        win.blit(s, (self.x -30, self.y -5))
        pygame.draw.rect(win,(255,255,255),(self.x -35, self.y -10,self.width, self.height),5,10)
        win.blit(self.text, (self.x , self.y )) 



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
        return self

class BlockofText(pygame.sprite.Sprite):
    def __init__(self,file, font_size):
        super(BlockofText,self).__init__()
        self.font_size = font_size
        self.font = pygame.font.SysFont(FONT,self.font_size)
        script = self.create_script(file)
        self.text = self.create_text(script)

    def create_script(self,textfile):
        with open(textfile,'r') as file:
            script = ""
            for line in file:
                script += line
        return script

    def create_text(self,script):
        text = []
        final_line = False
        while not final_line:
            if "\n" in script:
                linebreak = script.index("\n")
            else:
                final_line = True
                linebreak = len(script)
            line = script[:linebreak]
            if self.font.size(line)[0]  > SCREEN_WIDTH - 20:
                current_line = ""
                words = line.split()
                for word in words:
                    test_line = current_line + " " +  word
                    if self.font.size(test_line)[0]  > SCREEN_WIDTH - 20:
                        text.append(Text(current_line,self.font_size))
                        current_line = word
                    else:
                        current_line = test_line
                if current_line:
                    text.append(Text(current_line,self.font_size))
            else:
                text.append(Text(line,self.font_size))
            script = script[linebreak+ 1:]
        return text
    
    def draw(self,win):
        x,y = 10,20
        for line in self.text:
            line.set_pos(x,y)
            line.draw(win)
            y += self.font_size + 10

