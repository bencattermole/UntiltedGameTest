import os
import random
import pygame
import math
import sys
import WorldGen
import npcAi

COLOR_INACTIVE = pygame.Color('gray30')
COLOR_ACTIVE = pygame.Color('white')
path = str(os.path.dirname(__file__))

def draw_controls(screen, Screen_Size):
    #font selection

    font_norm = pygame.font.Font(f'{path}/kongtext.ttf', 15)
    font = pygame.font.Font(f'{path}/kongtext.ttf', 8)

    '''
    [ codeman38 | cody@zone38.net | http://www.zone38.net/ ]

    this font is made by the above and is free to use I found it from this website:
    https://www.1001fonts.com/pixel-fonts.html?page=4

    '''

    # Initialing Color
    color = (255, 0, 0)

    # Drawing Rectangle
    #pygame.draw.rect(screen, color, pygame.Rect(Screen_Size + 5, 5, 60, 60))

    screen.blit(font_norm.render('Menu', True, (255, 255, 255)), (Screen_Size + 5, 5))
    screen.blit(font_norm.render('World Generation', True, (255, 255, 255)), (Screen_Size + 5, 40))
    screen.blit(font_norm.render('______________________', True, (255, 255, 255)), (Screen_Size + 5, 45))
    screen.blit(font_norm.render('Chance of water', True, (255, 255, 255)), (Screen_Size + 5, 80))
    screen.blit(font_norm.render('Generations', True, (255, 255, 255)), (Screen_Size + 5, 180))
    screen.blit(font.render('Num of Adj. for water to remain', True, (255, 255, 255)), (Screen_Size + 5, 290))
    screen.blit(font.render('Num of Adj. for grass to water', True, (255, 255, 255)), (Screen_Size + 5, 390))


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font = pygame.font.Font(f'{path}/kongtext.ttf', 20)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)



