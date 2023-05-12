import sys
from tile2 import *
from network import Network

network = Network()

# pygame.init()
clock = pygame.time.Clock()
width = 400
height = 640
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Player2")

data_to_send = network.getPlayerData()
player_id = data_to_send[1]
rect_player = pygame.Rect(0, 0, 51, 51)
rect_player.centerx = 250
rect_player.centery = 100

# movement units
player_vel = 6
direction = pygame.math.Vector2(0, 0)
fall_vel = 0
jump_speed = -15
gravity = 0.8

# position detection
on_ground = False
on_ceiling = False
on_left = False
on_right = False
following_ground = False
distance = 0
position = [on_ground, on_ceiling, on_left, on_right, following_ground, distance]

point = 0

# background
background = pygame.transform.scale(pygame.image.load("background\\bg02.png"), (1100, height))


def apply_gravity():
    direction.y += gravity
    rect_player.y += direction.y


def jump():
    direction.y = jump_speed


def horizontal_collision():
    for tile in tiles:
        if rect_player.colliderect(tile[0]):
            if direction.x < 0:
                rect_player.left = tile[0].right
                position[2] = True
            elif direction.x > 0:
                rect_player.right = tile[0].left
                position[3] = True
            break
    if position[2] and direction.x >= 0:
        position[2] = False
    if position[3] and direction.x <= 0:
        position[3] = False


def vertical_collision():
    apply_gravity()
    for tile in tiles:
        if rect_player.colliderect(tile[0]):
            if direction.y > 0:
                rect_player.bottom = tile[0].top
                direction.y = 0
                position[0] = True
            elif direction.y < 0:
                rect_player.top = tile[0].bottom
                direction.y = 0
                position[1] = True

            # player following position of the moving tile
            if position[0] and not position[4]:
                # measure the distance between current x position
                # of player and x position of moving tile.
                # position[5] contains the distance
                position[5] = rect_player.x - tile[0].x
                position[4] = True
            if position[0] and position[4] and direction.x == 0:
                rect_player.x = tile[0].x + position[5]
            break
    if position[0] and direction.y < 0 or direction.y > 1:
        position[0] = False
    if position[1] and direction.y > 0.05:
        position[1] = False
    if not position[0] or direction.x != 0:
        position[4] = False
        position[5] = 0


def update_position(player_vel):
    rect_player.x += direction.x * player_vel
    horizontal_collision()
    vertical_collision()
    return rect_player

def player_control():
    # player control and border control
    userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT] and rect_player.x > 0:
        direction.x = -1
    elif userInput[pygame.K_RIGHT] and rect_player.x < width - 50:
        direction.x = 1
    else:
        direction.x = 0
    if userInput[pygame.K_UP] and rect_player.y > 0 and position[0]:
        jump()

# check if the player touches the diamond
def check_diamond(diamond_rect):
    if rect_player.colliderect(diamond_rect):
        return True
    return False


# 1. for diamond pointer, 2. to check if diamond collected
data_to_send.append([2, False])
while True:
    clock.tick(60)
    data_retrieved = network.send(data_to_send)
    data_to_send[3][1] = False
    # print("data retrieved:", data_retrieved)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    player_control()
    # extracting tile position from server
    tiles = data_retrieved[0]
    # this stores the pointer of which diamond to be drawn
    diamond_pos_pointer = data_retrieved[1][0]
    if diamond_pos_pointer > 11:
        player_winner = 1
        max_point = data_retrieved[2][2]
        for i in range(3, len(data_retrieved)):
            if max_point < data_retrieved[i][2]:
                max_point = data_retrieved[i][2]
                player_winner = i - 1
        print("Player", player_winner, "won the game")

    # diamond position as a rectangle
    diamond_rect = data_retrieved[1][diamond_pos_pointer]
    diamond_image = pygame.image.load("tiles\\diamond.png")
    # diamond_rect = diamond_image.get_rect()
    index = 0
    for i in range(2, len(data_retrieved)):
        if player_id == data_retrieved[i][1]:
            index = i
    point = data_retrieved[index][2]
    print("my point", point)
    if check_diamond(diamond_rect):
        print("diamond touched")
        data_to_send[3][1] = True
        point += 10
        data_to_send[2] = point

    # update player position to be sent to the server
    data_to_send[0] = update_position(player_vel)

    screen.blit(background, (0, 0))
    # draw tiles
    for tile in tiles:
        if tile[1]:
            tile_image = pygame.transform. \
                scale(pygame.image.load("tiles\\tile_mid.png"), (40, 40))
        else:
            if tile[0].width == 40:
                tile_image = pygame.transform. \
                    scale(pygame.image.load("tiles\\tile.png"), (40, 40))
            elif tile[0].width == 80:
                tile_image = pygame.transform. \
                    scale(pygame.image.load("tiles\\2_tiles.png"), (80, 40))
            elif tile[0].width == 120:
                tile_image = pygame.transform. \
                    scale(pygame.image.load("tiles\\3_tiles.png"), (120, 40))
            else:
                tile_image = pygame.transform. \
                    scale(pygame.image.load("tiles\\4_tiles.png"), (160, 40))

        screen.blit(tile_image, tile[0])

    rect_front = None
    image_front = None
    # draw all players
    for i in range(2, len(data_retrieved)):
        # print(data_retrieved)
        rect_other = data_retrieved[i][0]
        image = data_retrieved[i][1]
        # make the user player visible on front
        if data_to_send[1] == image:
            rect_front = rect_other
            image_front = image
        # print(image)
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

    screen.blit(diamond_image, diamond_rect)
    pygame.display.flip()
