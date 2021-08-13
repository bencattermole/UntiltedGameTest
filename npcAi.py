import pygame
import random
import WorldGen

'''
important notes at the bottom
'''

class NPC(object):
    def __init__(self, name, bound_box, pref_tile):
        self.rect = pygame.rect.Rect((64, 64, 16, 16))
        self.color = (255, 255, 255)
        self.name = name
        self.bound_box = bound_box
        self.pref_tile = pref_tile
        self.facing = 'N'

    def new_facing(self):
        self.make_random_facing_change()

    def can_see(self, pos, map):
        '''
        take in current pos
        take in map
        using current facing get the three coords of the tiles
        return a dict key: tile name, stored: sqaure label
        '''

        can_see_these = {}

        if 0 < pos.x <= ((self.bound_box/16)-2) and  0 < pos.y <= ((self.bound_box/16)-2):
            if self.facing == 'N':
                can_see_these[map[WorldGen.coord(pos.x-1, pos.y-1)].name] = '7'
                can_see_these[map[WorldGen.coord(pos.x, pos.y-1)].name] = '0'
                can_see_these[map[WorldGen.coord(pos.x+1, pos.y-1)].name] = '1'
            elif self.facing == 'E':
                can_see_these[map[WorldGen.coord(pos.x + 1, pos.y - 1)].name] = '1'
                can_see_these[map[WorldGen.coord(pos.x + 1, pos.y)].name] = '2'
                can_see_these[map[WorldGen.coord(pos.x + 1, pos.y + 1)].name] = '3'
            elif self.facing == 'S':
                can_see_these[map[WorldGen.coord(pos.x + 1, pos.y + 1)].name] = '3'
                can_see_these[map[WorldGen.coord(pos.x, pos.y + 1)].name] = '4'
                can_see_these[map[WorldGen.coord(pos.x - 1, pos.y + 1)].name] = '5'
            elif self.facing == 'W':
                can_see_these[map[WorldGen.coord(pos.x - 1, pos.y + 1)].name] = '5'
                can_see_these[map[WorldGen.coord(pos.x - 1, pos.y)].name] = '6'
                can_see_these[map[WorldGen.coord(pos.x - 1, pos.y - 1)].name] = '7'
            return can_see_these
        elif 0 == pos.x and 0 == pos.y:
            can_see_these[map[WorldGen.coord(pos.x + 1, pos.y + 1)].name] = '3'
            return can_see_these
        elif pos.x == ((self.bound_box/16)-1) and 0 == pos.y:
            can_see_these[map[WorldGen.coord(pos.x - 1, pos.y + 1)].name] = '5'
            return can_see_these
        elif pos.y == ((self.bound_box/16)-1) and pos.x == 0:
            can_see_these[map[WorldGen.coord(pos.x + 1, pos.y - 1)].name] = '1'
            return can_see_these
        elif pos.y == ((self.bound_box/16)-1) and pos.x == ((self.bound_box/16)-1):
            can_see_these[map[WorldGen.coord(pos.x - 1, pos.y - 1)].name] = '7'
            return can_see_these
        elif 0 == pos.x:
            can_see_these[map[WorldGen.coord(pos.x + 1, pos.y - 1)].name] = '1'
            can_see_these[map[WorldGen.coord(pos.x + 1, pos.y)].name] = '2'
            can_see_these[map[WorldGen.coord(pos.x + 1, pos.y + 1)].name] = '3'
            return can_see_these
        elif pos.x == ((self.bound_box/16)-1):
            can_see_these[map[WorldGen.coord(pos.x - 1, pos.y + 1)].name] = '5'
            can_see_these[map[WorldGen.coord(pos.x - 1, pos.y)].name] = '6'
            can_see_these[map[WorldGen.coord(pos.x - 1, pos.y - 1)].name] = '7'
            return can_see_these
        elif 0 == pos.y:
            can_see_these[map[WorldGen.coord(pos.x + 1, pos.y + 1)].name] = '3'
            can_see_these[map[WorldGen.coord(pos.x, pos.y + 1)].name] = '4'
            can_see_these[map[WorldGen.coord(pos.x - 1, pos.y + 1)].name] = '5'
            return can_see_these
        elif pos.y == ((self.bound_box/16)-1):
            can_see_these[map[WorldGen.coord(pos.x - 1, pos.y - 1)].name] = '7'
            can_see_these[map[WorldGen.coord(pos.x, pos.y - 1)].name] = '0'
            can_see_these[map[WorldGen.coord(pos.x + 1, pos.y - 1)].name] = '1'
            return can_see_these

    def decision(self, pos, map):
        current_tile_type = map[pos].name
        can_see_these = self.can_see(pos, map)

        if current_tile_type != self.pref_tile:
            if self.pref_tile in can_see_these:
                #move self to prefered tile you can see
                self.move_self(can_see_these[self.pref_tile])
            else:
                #move self to random choice of tiles you can see
                self.move_self(can_see_these[random.choice(list(can_see_these.keys()))])
        else:
            choice = random.uniform(0, 1)

            if choice < 0.03:
                #move to random tile you can see, regardless of preference (others would never leave pref tiles)
                self.move_self(can_see_these[random.choice(list(can_see_these.keys()))])
            elif choice < 0.66:
                #change to face new direction
                self.make_random_facing_change()
            elif choice <= 1:
                #wait in place (should change this probably a better way to impliment waiting
                pass

        choice_to_rand_change_facing = random.uniform(0, 1)

        if choice_to_rand_change_facing <= 0.2:
            self.make_random_facing_change()

    def make_random_facing_change(self):
        choice = random.uniform(0, 1)

        if choice < 0.25:
            self.facing = 'N'
        elif choice < 0.5:
            self.facing = 'E'
        elif choice < 0.75:
            self.facing = 'S'
        elif choice <= 1:
            self.facing = 'W'

    def move_self(self, adj_to_move_to):

        if adj_to_move_to == '6' and self.rect.left > 0:
            self.rect.move_ip(-16, 0)
        elif adj_to_move_to == '2' and self.rect.right < self.bound_box:
            self.rect.move_ip(16, 0)
        elif adj_to_move_to == '0' and self.rect.top > 0:
            self.rect.move_ip(0, -16)
        elif adj_to_move_to == '4' and self.rect.bottom < self.bound_box:
            self.rect.move_ip(0, 16)
        elif adj_to_move_to == '7' and self.rect.left > 0 and self.rect.top > 0:
            self.rect.move_ip(-16, -16)
        elif adj_to_move_to == '1' and self.rect.right < self.bound_box and self.rect.top > 0:
            self.rect.move_ip(16, -16)
        elif adj_to_move_to == '3' and self.rect.right < self.bound_box and self.rect.bottom < self.bound_box:
            self.rect.move_ip(16, 16)
        elif adj_to_move_to == '5' and self.rect.left > 0 and self.rect.bottom < self.bound_box:
            self.rect.move_ip(-16, 16)


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


'''
Movement system:
    Npc has current facing and preferred tile type
    
    4 facing are cardinal directions N,E,S,W
    
    example north facing:
    
            [Seen]  [Seen]  [Seen]
            
            [....]   [XX]   [....]
            
            [....]  [....]  [....]
    
    the NPC is represented by XX, the tiles it can see are labelled SEEN, and the ones it cant ....
    
    if NPC is not currently standing on preferred tile type:
        if A seen tile is that type:
            Move to that tile
        else:
            Move to a random Tile
    else (currently standing on preferred tile):
        Make random choice between: Move to new tile, Wait on current tile, change facing direction(likely)
    
    once movement done make random choice to change facing (unlikely)
    
    expected behaviour from the above:
        1. NPC's will move in slightly random consistent paths until there prefered tile is found,
        2. they will then remain on that tile type moving in random directions
        3. if they leave they will begin to 1.
        
    
    to change behaviour change values of choices in second if statement
'''