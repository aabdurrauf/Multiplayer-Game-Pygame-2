import random
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, number_of_tile, size=40, ground_tile=False):
        super().__init__()
        self.rect = pygame.Rect(pos_x, pos_y, size * number_of_tile, size)
        self.ground_tile = ground_tile
        # print("rect.size:", self.rect.width)

class TileMaker:
    def __init__(self):
        self.tiles = []

    def getTiles(self, width, height, ):
        # make the ground
        for bx in range(0, width, 40):
            new_tile = Tile(bx, height - 50, number_of_tile=1, ground_tile=True)
            self.tiles.append([new_tile.rect, new_tile.ground_tile])

        # make moving tiles
        for level in range(4):
            tiles_num = random.randint(1, 3)
            starting_point = random.randrange(0, width - tiles_num * 40, 7)
            new_tile = Tile(starting_point, 475 - 115 * level, tiles_num)
            self.tiles.append([new_tile.rect, new_tile.ground_tile])

        return self.tiles
