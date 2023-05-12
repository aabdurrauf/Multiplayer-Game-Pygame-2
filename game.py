import pygame, sys

from tile import *
from network import Network

network = Network()

# pygame.init()
clock = pygame.time.Clock()
width = 400
height = 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Player2")

# player1 = pygame.image.load("superheroes\\captainamerica.png")
# rect_player = player1.get_rect()
my_player_data = network.getPlayerData()
rect_player = pygame.Rect(0, 0, 51, 51)
rect_player.centerx = 250
rect_player.centery = 100

# movement units
player_vel = 10
direction = pygame.math.Vector2(0, 0)
fall_vel = 0
jump_speed = -16
gravity = 0.8

# position detection
on_ground = False
on_ceiling = False
on_left = False
on_right = False
position = [on_ground, on_ceiling, on_left, on_right]

# tiles
tile_maker = TileMaker()
tiles = tile_maker.getTiles(width, height)

# background
# background = pygame.image.load("background\\bg01.png")
background = pygame.transform.scale(pygame.image.load("background\\bg02.png"), (1100, height))


def apply_gravity():
    direction.y += gravity
    rect_player.y += direction.y


def jump():
    direction.y = jump_speed


def horizontal_collision():
    for tile in tiles:
        if rect_player.colliderect(tile.rect):
            if direction.x < 0:
                rect_player.left = tile.rect.right
                position[2] = True
                # self.current_x = player.rect.left
            elif direction.x > 0:
                rect_player.right = tile.rect.left
                position[3] = True
                # self.current_x = player.rect.right
    if position[2] and direction.x >= 0:
        position[2] = False
    if position[3] and direction.x <= 0:
        position[3] = False


def vertical_collision():
    apply_gravity()
    for tile in tiles:
        if rect_player.colliderect(tile.rect):
            if direction.y > 0:
                rect_player.bottom = tile.rect.top
                direction.y = 0
                position[0] = True
            elif direction.y < 0:
                rect_player.top = tile.rect.bottom
                direction.y = 0
                position[1] = True

    if position[0] and direction.y < 0 or direction.y > 1:
        position[0] = False
    if position[1] and direction.y > 0.1:
        position[1] = False


def update_position(player_vel):
    rect_player.x += direction.x * player_vel
    horizontal_collision()
    vertical_collision()
    return rect_player

while True:
    clock.tick(60)

    data_retrieved = network.send(my_player_data)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # player control and border control
    player_vel = 6
    userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT] and rect_player.x > 0:
        direction.x = -1
    elif userInput[pygame.K_RIGHT] and rect_player.x < width - 50:
        direction.x = 1
    else:
        direction.x = 0
    if userInput[pygame.K_UP] and rect_player.y > 0 and position[0]:
        jump()

    my_player_data[0] = update_position(player_vel)
    # screen.fill((30, 30, 30))
    screen.blit(background, (0, 0))
    for tile in tiles:
        screen.blit(tile.image, tile.rect)

    # print(len(data_retrieved))
    rect_front = None
    image_front = None
    # draw all players
    for i in range(len(data_retrieved)):
        print(data_retrieved)
        rect_other = data_retrieved[i][0]
        image = data_retrieved[i][1]
        # make the user player visible on front
        if my_player_data[1] == image:
            rect_front = rect_other
            image_front = image
        print(image)
        player_image = pygame.image.load("superheroes\\" + image)
        rect = player_image.get_rect()
        rect.x = rect_other.x
        rect.y = rect_other.y

        screen.blit(player_image, rect)
    # redraw the player in front of the others
    player_image = pygame.image.load("superheroes\\" + image_front)
    rect = player_image.get_rect()
    rect.x = rect_front.x
    rect.y = rect_front.y
    screen.blit(player_image, rect)

    pygame.display.flip()
