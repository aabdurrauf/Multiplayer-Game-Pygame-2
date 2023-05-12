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


def update_data_to_be_sent(data_to_be_sent, player_data):
    data_to_be_sent.append(player_data)
    # print("update_data_to_be_sent: ", data_to_be_sent)
    return data_to_be_sent


# make moving tiles
width = 400
height = 650
cp = 1
tile_maker = TileMaker()
tiles_rect = tile_maker.getTiles(width, height)

data_to_be_sent = []
data_to_be_sent = update_data_to_be_sent(data_to_be_sent, tiles_rect)

character_list = ["ironman.png", "captainamerica.png", "hulk.png", "thor.png"]

# rectangle list for players
rect_list = []
for i in range(4):
    rect = pygame.Rect(50 + 60 * i, 300, 51, 51)
    rect_list.append(rect)
speed = [1, -2, 3, -1]

def update_moving_tiles(tiles_rect2):
    for i in range(4):
        tiles_rect2[10 + i][0].x = (tiles_rect2[10 + i][0].x + speed[i])
        if tiles_rect2[10 + i][0].left <= 0 or tiles_rect2[10 + i][0].right >= 400:
            speed[i] *= -1

    return tiles_rect2


def threaded_client(conn, data_to_be_sent, player_no):
    conn.send(pickle.dumps(data_to_be_sent[player_no]))
    print("data_to_be_sent:", data_to_be_sent)

    reply = ''
    while True:
        try:
            if player_no == 1:
                data_to_be_sent[0] = update_moving_tiles(data_to_be_sent[0])
            data = pickle.loads(conn.recv(2048))
            data_to_be_sent[player_no] = data
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
    data_to_be_sent = update_data_to_be_sent(data_to_be_sent, [rect_list[cp], character_list[cp]])

    start_new_thread(threaded_client, (conn, data_to_be_sent, cp))
    cp += 1
