import pygame
import random
import numpy as np


class neighbors:
    def __init__(self):
        self.water_tot_num = 0
        self.plant_tot_num = 0
        self.grass_tot_num = 0
        self.water = 0


class terrianType:
    def __init__(self, name, color):
        self.name = name
        self.color = color


class coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)


water = terrianType('water', (0, 0, 255, 255))
plant = terrianType('plant', (36, 102, 38))
grass = terrianType('grass', (54, 209, 58))
water_plant = terrianType('water_plant', (0, 0, 255, 255))
grass_1 = terrianType('grass_1', (0, 0, 255, 255))
grass_2 = terrianType('grass_2', (0, 0, 255, 255))
grass_3 = terrianType('grass_3', (0, 0, 255, 255))
deep = terrianType('deep', (0, 0, 255, 255))

terrain_types = [water, plant, grass, water_plant, grass_1, grass_2, grass_3, deep]

map = {}


def test_to_see_how():
    print('test')


def generate_new_map(dimension):

    shape = (dimension, dimension)

    #Con[0] = chance of water to spawn
    #Con[1] = Num of generations 1 - 5
    #Con[2] = Num of neighbors for water to GROW
    #Con[3] = Num of neighbors for ground to become water

    Con = [random.uniform(0, 1), random.randint(1,5), random.randint(0,9), random.randint(0,9)]

    WATER = 0
    PLANT = 1
    GRASS = 2
    # create a random map
    new_map = np.ones(shape)
    rand_dict = {}

    for i in range(dimension):
        for j in range(dimension):
            choice = random.uniform(0, 1)
            rand_dict[coord(i, j)] = terrain_types[2] if choice < Con[0] else terrain_types[0]

    return iterate_new_map(dimension, Con[1], rand_dict, Con)

    #choice >> 1 - fewer spawn
    #generaitons = more applications of rules


def iterate_new_map(dimension, generations, rand_dict, Con):

    dict_to_use_parent = rand_dict
    '''
    Could change the generation loop so that it doesnt always start with water and grass, could instead be two random
    tile types
    '''

    for generation in range(generations):
        dict_to_use = {}
        for x in range(dimension):
            for y in range(dimension):
                surroundings = get_neighbors_water(x, y, dict_to_use_parent)

                if dict_to_use_parent[coord(x, y)] == terrain_types[0]:

                    #IF CURRENT TILE IS WATER THEN:

                    if surroundings.water_tot_num <= Con[2]:
                        dict_to_use.update({coord(x, y): terrain_types[2]})
                    else:
                        dict_to_use.update({coord(x, y): terrain_types[0]})
                else:
                    if dict_to_use_parent[coord(x, y)] == terrain_types[2]:

                        #ELSE IF CURRENT TILE IS GRASS THEN:

                        if surroundings.water_tot_num >= Con[3]:
                            dict_to_use.update({coord(x, y): terrain_types[0]})
                        else:
                            dict_to_use.update({coord(x, y): terrain_types[2]})
                    else:
                        pass

        dict_to_use_parent = dict_to_use

    for x in range(dimension):
        for y in range(dimension):
            surroundings = get_neighbors_water(x, y, dict_to_use_parent)

            choice = random.uniform(0, 1)

            if choice >= 0.99:
                dict_to_use.update({coord(x, y): get_random_plant(False)})

            if dict_to_use_parent[coord(x, y)] == terrain_types[0] and choice <= 0.2:
                if surroundings.water_tot_num <= 5:
                    dict_to_use.update({coord(x, y): get_random_plant(True)})
                else:
                    dict_to_use.update({coord(x, y): terrain_types[0]})

            if dict_to_use_parent[coord(x, y)] == terrain_types[2] and choice <= 0.2:
                if surroundings.water_tot_num >= 1:
                    dict_to_use.update({coord(x, y): get_random_plant(False)})
                else:
                    dict_to_use.update({coord(x, y): terrain_types[2]})

            if dict_to_use_parent[coord(x, y)] == terrain_types[2]:
                dict_to_use.update({coord(x, y): get_random_grass_type()})

            if dict_to_use_parent[coord(x, y)] == terrain_types[0]:
                if surroundings.water_tot_num == 8:
                    dict_to_use.update({coord(x, y): terrain_types[7]})
                else:
                    dict_to_use.update({coord(x, y): terrain_types[0]})

    #island correction loop and lone plant deletion loop, should probably change this, seems very inefficent
    #has to be in seperate loop because if in first it will not work

    dict_to_use_parent = dict_to_use

    for x in range(dimension):
        for y in range(dimension):
            surroundings = get_neighbors_water(x, y, dict_to_use_parent)
            if dict_to_use_parent[coord(x, y)] == terrain_types[7]:
                if surroundings.plant_tot_num >= 1:
                    dict_to_use.update({coord(x, y): terrain_types[0]})
                else:
                    dict_to_use.update({coord(x, y): terrain_types[7]})
            if dict_to_use_parent[coord(x, y)] == terrain_types[1]:
                if surroundings.grass_tot_num == 8:
                    dict_to_use.update({coord(x, y): terrain_types[2]})
                else:
                    dict_to_use.update({coord(x, y): terrain_types[1]})

    return dict_to_use


def get_random_plant(water_pref):
    choice = random.uniform(0, 1)
    if water_pref:
        if choice <= 0.8:
            return terrain_types[3]
        else:
            return terrain_types[1]
    else:
        if choice <= 0.9:
            return terrain_types[1]
        else:
            return terrain_types[3]


def get_random_grass_type():
    choice = random.uniform(0, 1)

    if choice <= 0.5:
        return terrain_types[2]
    elif choice <= 0.7:
        return terrain_types[4]
    elif choice <= 0.97:
        return terrain_types[5]
    else:
        return terrain_types[6]


def get_neighbors_water(x, y, test_dict):
    #offsets

    #      7 0 1
    #      6 x 2
    #      5 4 3

    offset = [coord(x, y-1), coord(x+1, y-1), coord(x+1, y), coord(x+1, y+1), coord(x, y+1), coord(x-1, y+1), coord(x-1, y), coord(x-1, y-1)]
    tiles = neighbors()

    for neighbor in offset:
        if neighbor in test_dict:
            if test_dict[neighbor] == terrain_types[0]:
                tiles.water += 1
                tiles.water_tot_num += 1
            elif test_dict[neighbor] == terrain_types[1]:
                tiles.plant_tot_num += 1
            elif test_dict[neighbor] == terrain_types[2]:
                tiles.grass_tot_num += 1
            elif test_dict[neighbor] == terrain_types[3]:
                tiles.plant_tot_num += 1
            elif test_dict[neighbor] == terrain_types[4]:
                tiles.grass_tot_num += 1
            elif test_dict[neighbor] == terrain_types[5]:
                tiles.grass_tot_num += 1
            elif test_dict[neighbor] == terrain_types[6]:
                tiles.grass_tot_num += 1
            elif test_dict[neighbor] == terrain_types[7]:
                tiles.water += 1
                tiles.water_tot_num += 1
        else:
            pass

    return tiles
