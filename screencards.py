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
    
    def empty(self):
        self.texts.empty()
        self.buttons.empty()

    def main_menu(self):
        self.empty()
        self.buttons.add(Button("Singleplayer",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2- 120),80),
                       Button("2 Player",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),80))
    
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
    
    def display(self,win):
        for item in self.texts:
            item.draw(win)
        for item in self.buttons:
            item.draw(win)
        
        





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
