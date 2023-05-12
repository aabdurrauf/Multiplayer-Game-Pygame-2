import random
import socket
from _thread import *
import pickle
from tile2 import *
import pygame

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_STREAM

server = '172.16.0.54'
port = 5555

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(4)
print("Waiting for a connection")


def update_data_to_be_sent(data_to_be_sent, data):
    data_to_be_sent.append(data)
    # print("update_data_to_be_sent: ", data_to_be_sent)
    return data_to_be_sent


# make moving tiles
width = 400
height = 650
cp = 2
tile_maker = TileMaker()
tiles_rect = tile_maker.getTiles(width, height)

data_to_be_sent = []
data_to_be_sent = update_data_to_be_sent(data_to_be_sent, tiles_rect)

character_list = ["captainamerica.png", "wandavision.png", "hulk.png", "thor.png"]

# rectangle list for players
rect_list = []
for i in range(4):
    rect = pygame.Rect(50 + 60 * i, 300, 51, 51)
    rect_list.append(rect)

speed = [1, -2, 3, -1]
# randomly set the velocity of tiles
for i in range(4):
    num = 0
    while num == 0:
        num = random.randint(-2, 3)
    speed[i] = num

def update_moving_tiles(tiles_rect2):
    for i in range(4):
        tiles_rect2[10 + i][0].x = (tiles_rect2[10 + i][0].x + speed[i])
        if tiles_rect2[10 + i][0].left <= 0 or tiles_rect2[10 + i][0].right >= 400:
            speed[i] *= -1

    return tiles_rect2


number_of_diamonds = 10
diamonds = [2, False]
for i in range(number_of_diamonds):
    d_x = random.randrange(10, width-50, 10)
    d_y = random.randrange(10, 470, 10)
    diamonds.append(pygame.Rect(d_x, d_y, 24, 24))
# add last diamond to be unreachable
diamonds.append(pygame.Rect(1000, 1000, 24, 24))

data_to_be_sent = update_data_to_be_sent(data_to_be_sent, diamonds)
def threaded_client(conn, data_to_be_sent, player_no):
    conn.send(pickle.dumps(data_to_be_sent[player_no]))
    print("data_to_be_sent:", data_to_be_sent)

    reply = ''
    while True:
        try:
            if player_no == 2:
                data_to_be_sent[0] = update_moving_tiles(data_to_be_sent[0])
            data = pickle.loads(conn.recv(2048*2))
            data_to_be_sent[player_no] = data

            # point = data_to_be_sent[player_no][2]
            if data[3][1]:
                data_to_be_sent[1][0] += 1
                # data_to_be_sent[player_no][2] += 10
                # point += 10
                # data_to_be_sent[player_no][2] = point

            # data_to_be_sent[1][0] = data[2]
            print(data[2])
            if not data:
                conn.send(str.encode("Disconnected"))
                break

            conn.sendall(pickle.dumps(data_to_be_sent))
        except:
            print("Failed to send")
            break

    print("Connection Closed")
    conn.close()


player_start_y = 150
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    data_to_be_sent = update_data_to_be_sent(data_to_be_sent,
                      [rect_list[cp-2], character_list[cp-2], 0])

    start_new_thread(threaded_client, (conn, data_to_be_sent, cp))
    cp += 1
