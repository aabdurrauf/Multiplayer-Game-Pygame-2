import socket
from _thread import *
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_STREAM

server = '172.30.48.1'
port = 5555

# server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(4)
print("Waiting for a connection")


def update_players_data(players_data, player_data):
    players_data.append(player_data)
    print("update_players_data: ", players_data)
    return players_data


def threaded_client(conn, players_data, player_no):
    conn.send(pickle.dumps(players_data[player_no]))  # actually we don't need this,
    # we can just draw all the
    # players on each side

    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print("data in try:", data)
            players_data[player_no] = data
            if not data:
                conn.send(str.encode("Disconnected"))
                break

            conn.sendall(pickle.dumps(players_data))
        except:
            print("data in except:", data)
            print("Failed to send")
            break

    print("Connection Closed")
    conn.close()


cp = 0
players_data = []
character_list = ["antman.png", "captainamerica.png", "doctorstrange.png", "hawkeye.png"]

player_start_y = 150
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    players_data = update_players_data(players_data, [None, character_list[cp]])
    # print(players_data)

    start_new_thread(threaded_client, (conn, players_data, cp))
    cp += 1
