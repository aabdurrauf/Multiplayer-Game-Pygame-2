import pygame, sys
from network import Network

network = Network()

# pygame.init()
clock = pygame.time.Clock()
weight = 500
height = 500
screen = pygame.display.set_mode((weight, height))
pygame.display.set_caption("Player3")

player1 = pygame.image.load("superheroes\\captainamerica.png")
rect_player = player1.get_rect()
rect_player.x = 250
rect_player.y = 100

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
                rect_player.top =tile.rect.bottom
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

while True:
    clock.tick(60)

    all_players_rect = network.send([rect_player, "captainamerica.png"])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # player control and border control
    player_vel = 6
    userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT] and rect_player.x > 0:
        direction.x = -1
    elif userInput[pygame.K_RIGHT] and rect_player.x < weight - 50:
        direction.x = 1
    else:
        direction.x = 0
    if userInput[pygame.K_UP] and rect_player.y > 0 and position[0]:
        jump()

    update_position(player_vel)
    screen.fill((30, 30, 30))
    # screen.blit(player1, rect_player)
    for tile in tiles:
        screen.blit(tile.image, tile.rect)

    print(len(all_players_rect))
    for i in range(len(all_players_rect)):
        print(all_players_rect)
        rect_other = all_players_rect[i][0]
        image = all_players_rect[i][1]
        print(image)
        player_image = pygame.image.load("superheroes\\" + image)
        rect = player_image.get_rect()
        rect.x = rect_other.x
        rect.y = rect_other.y

        screen.blit(player_image, rect)

    pygame.display.flip()
