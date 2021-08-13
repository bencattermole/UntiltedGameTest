import os
import random
import pygame
import math
import sys
import WorldGen
import npcAi

"""
Hello!

This is a small game project I am working on. 

The current (12/08/2021) controls are as follows:
    arrow keys - move red figure
    g - generates a new map and prints values used into console, to manually change go to world gen and find Con array
        (fine tuning is required to get a 'good' map)
    t - this takes in an input from the console, this doesnt have any use at the moment
    i - prints the current window position of the red figure
    
The blue figure currently uses the movement from the npcAi.py file, go there to see the logic
    (preferred tile type is set here to water, you can change it for different behaviour)

The last bug I fixed was a crash when the blue figure went to the corner, I think my fix is working but please contact
me if you experience a crash when the blue figure moves to the corner :)

Thanks for playing!
"""

Screen_Size = 1024
block_size = 16
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)

map = WorldGen.generate_new_map(int((Screen_Size/block_size)))

screen = pygame.display.set_mode((Screen_Size, Screen_Size))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

#you may have to change the following path variables to where the sprites are

player_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Player_Character.png').convert()
player_IMG.set_colorkey((0, 0, 0, 0))
# Use the upper-left pixel color as transparent

wraith_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Wraith.png').convert()
wraith_IMG.set_colorkey((0, 0, 0, 0))

water_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Water.png').convert()
plant_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Plant.png').convert()
grass_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Grass.png').convert()
water_plant_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Water_plant.png').convert()
grass_1_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Grass_1.png').convert()
grass_2_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Grass_2.png').convert()
grass_3_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Grass_3.png').convert()
water_deep_IMG = pygame.image.load('C:/Users/Ben/PycharmProjects/UntiltedGameTest/Sprites/Water_Deep.png').convert()

spriteLookup = {'water': water_IMG, 'plant': plant_IMG, 'grass': grass_IMG, 'water_plant': water_plant_IMG, 'grass_1': grass_1_IMG, 'grass_2': grass_2_IMG, 'grass_3': grass_3_IMG, 'deep': water_deep_IMG}


class Player(object):
    def __init__(self):
        self.rect = pygame.rect.Rect((64, 64, 16, 16))
        self.color = (255, 255, 255)

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_LEFT] and (self.rect.left > 0):
           self.rect.move_ip(-16, 0)
        if key[pygame.K_RIGHT] and (self.rect.right < Screen_Size):
           self.rect.move_ip(16, 0)
        if key[pygame.K_UP] and (self.rect.top > 0):
           self.rect.move_ip(0, -16)
        if key[pygame.K_DOWN] and (self.rect.bottom < Screen_Size):
           self.rect.move_ip(0, 16)

    def draw(self, surface):
        pygame.draw.rect(screen, self.color, self.rect)


def just_a_quick_test():
    win_Con = input('hello')

    if(win_Con == 'I want to win'):
        print('You won!')


def draw_terrain_grid():
    for x in range(0, Screen_Size, block_size):
        for y in range(0, Screen_Size, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            screen.blit(spriteLookup[map[WorldGen.coord(int(x / 16), int(y / 16))].name], rect)


def get_ground_info(rect):
    print(rect)


pygame.init()


player = Player()
wraith = npcAi.NPC('wraith', Screen_Size, 'water')
clock = pygame.time.Clock()

wraith_Rect = pygame.rect.Rect((304, 304, 16, 16))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                just_a_quick_test()
            if event.key == pygame.K_g:
                map = WorldGen.generate_new_map(int((Screen_Size/block_size)))
            if event.key == pygame.K_i:
                get_ground_info(player.rect)

    screen.fill((0, 0, 0))
    draw_terrain_grid()

    #player.draw(screen)
    player.handle_keys()
    wraith.decision( WorldGen.coord(int(wraith.rect.x/16), int(wraith.rect.y/16)), map)
    screen.blit(wraith_IMG, wraith.rect)
    screen.blit(player_IMG, player.rect)
    pygame.display.update()

    clock.tick(30)