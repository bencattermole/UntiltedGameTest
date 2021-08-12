

"""
Old code that I scrapped
"""


def draw_grid():
    for x in range(0, Screen_Size, block_size):
        for y in range(0, Screen_Size, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, color_map[int(x/10)][int(y/10)], rect) #one here only draws outline

#color_map = WorldGen.make_colour_map(Screen_Size, block_size)

def make_colour_map(screen_size, block_size):
    dim = int(screen_size / block_size)
    colour_map = [[0 for x in range(dim)] for y in range(dim)]

    for x in range(dim):
        for y in range(dim):
            colour_map[x][y] = get_random_color()

    return colour_map

#def get_random_color():
#    Decider = random.randrange(1, 10, 1)
#
#    if Decider >= 9:
#        b = 255 - random.randint(0,100)
#        return (0, 0, b, 255)
#    elif Decider >= 8:
#        g = 102 - random.randint(-100,100)
#        return (36, g, 38)
#    else:
#        r = 54 - random.randint(-40,40)
#        g = 209 - random.randint(-30,60)
#        return (r, g, 58)

def generate_map_dict(screen_size, block_size):
    dimensions = int(screen_size / block_size)
    i = 0

    for x in range(dimensions):
        for y in range(dimensions):
            new_map = generate_new_map(60)
            i +=1
            print(i)
            if (new_map[coord(x, y)] == 0):
                map[coord(x, y)] = terrain_types[0]
            else:
                map[coord(x, y)] = terrain_types[2]

    return map

def get_random_terrain():
    Decider = random.randrange(1, 10, 1)

    if Decider >= 9:
        return terrain_types[0]
    elif Decider >= 8:
        return terrain_types[1]
    else:
        return terrain_types[2]