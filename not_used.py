import random
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type_of_tile, size=40):
        super().__init__()
        if type_of_tile == "mid":
            self.image = pygame.transform. \
                scale(pygame.image.load("tiles\\tile_mid.png"), (size, size))
        elif type_of_tile == "1":
            self.image = pygame.transform. \
                scale(pygame.image.load("tiles\\tile.png"), (size, size))
        elif type_of_tile == "2":
            self.image = pygame.transform. \
                scale(pygame.image.load("tiles\\2_tiles.png"), (size * 2, size))
        elif type_of_tile == "3":
            self.image = pygame.transform. \
                scale(pygame.image.load("tiles\\3_tiles.png"), (size * 3, size))
        elif type_of_tile == "4":
            self.image = pygame.transform. \
                scale(pygame.image.load("tiles\\4_tiles.png"), (size * 4, size))
        else:
            self.image = pygame.transform. \
                scale(pygame.image.load("tiles\\tile.png"), (size, size))
        self.rect = self.image.get_rect(topleft=pos)

class TileMaker:
    def __init__(self):
        self.tiles = None

    def getTiles(self, width, height, ):
        self.tiles = pygame.sprite.Group()
        # make the ground
        for bx in range(0, width, 40):
            self.tiles.add(Tile((bx, height-50), type_of_tile="mid"))

        # make moving tiles
        for level in range(4):
            tiles_num = random.randint(1, 3)
            starting_point = random.randrange(0, width-tiles_num*40, 7)
            if tiles_num == 1:
                self.tiles.add(Tile((starting_point, 470 - 100 * level), type_of_tile="1"))
            elif tiles_num == 2:
                self.tiles.add(Tile((starting_point, 470 - 100 * level), type_of_tile="2"))
            else:
                self.tiles.add(Tile((starting_point, 470 - 100 * level), type_of_tile="3"))

        return self.tiles