import socket
from _thread import *
import pickle

import pygame

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_STREAM

server = '172.16.0.54'
port = 5555

# server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(4)
print("Waiting for a connection")


def update_data_to_be_sent(data_to_be_sent, player_data):
    data_to_be_sent.append(player_data)
    print("update_data_to_be_sent: ", data_to_be_sent)
    return data_to_be_sent


def threaded_client(conn, data_to_be_sent, player_no):
    conn.send(pickle.dumps(data_to_be_sent[player_no]))  # actually we don't need this,
    # we can just draw all the
    # players on each side

    reply = ''
    while True:

        try:
            data = pickle.loads(conn.recv(2048))
            print("data in try:", data)
            data_to_be_sent[player_no] = data
            if not data:
                conn.send(str.encode("Disconnected"))
                break

            conn.sendall(pickle.dumps(data_to_be_sent))
        except:
            print("data in except:", data)
            print("Failed to send")
            break

    print("Connection Closed")
    conn.close()


cp = 0
data_to_be_sent = []
character_list = ["ironman.png", "captainamerica.png", "hulk.png", "thor.png"]

rect_list = []
for i in range(4):
    rect = pygame.Rect( 50+60*i, 300, 51, 51)
    rect_list.append(rect)

player_start_y = 150
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    data_to_be_sent = update_data_to_be_sent(data_to_be_sent, [rect_list[cp], character_list[cp]])
    # print(data_to_be_sent)

    start_new_thread(threaded_client, (conn, data_to_be_sent, cp))
    cp += 1
