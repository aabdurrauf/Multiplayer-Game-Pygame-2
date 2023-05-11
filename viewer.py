import pygame, sys
from network import Network

network = Network()

pygame.init()
clock = pygame.time.Clock()
weight = 500
height = 500
screen = pygame.display.set_mode((weight, height))
pygame.display.set_caption("Viewer")


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size=35):
        super().__init__()
        # self.image = pygame.Surface((size,size))
        self.image = pygame.transform. \
            scale(pygame.image.load("tile.png"), (size, size))
        # self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)


tiles = pygame.sprite.Group()
for bx in range(0, 500, 35):
    tiles.add(Tile((bx, 400)))
tiles.add(Tile((260, 260)))
tiles.add(Tile((170, 170)))
tiles.add(Tile((70, 100)))
tiles.add(Tile((100, 300)))

player_image = pygame.image.load("superheroes\\captainamerica.png")

while True:
    rect_host = network.send(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))
    screen.blit(player_image, rect_host)
    for tile in tiles:
        screen.blit(tile.image, tile.rect)
    pygame.display.flip()
    clock.tick(60)
