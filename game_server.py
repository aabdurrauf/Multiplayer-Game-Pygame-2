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
    return players_data

# def setup(layout, character_name):
#     tiles = pygame.sprite.Group()
#     player = pygame.sprite.GroupSingle()
#
#     for row_index, row in enumerate(layout):
#         for col_index, cell in enumerate(row):
#             x = col_index * 40
#             y = row_index * 40
#
#             if cell == 'X':
#                 tile = Tile((x, y), 40)
#                 tiles.add(tile)
#             if cell == 'P':
#                 player_sprite = PlayerData((x, y), character_name)
#                 player.add(player_sprite)

def threaded_client(conn, players_data, player_no):
    conn.send(pickle.dumps(players_data[player_no]))

    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players_data[player_no] = data
            if not data:
                conn.send(str.encode("Disconnected"))
                break

            conn.sendall(pickle.dumps(players_data))
        except:
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
    players_data = update_players_data(players_data,
                                       PlayerData(50 + 60 * cp, player_start_y, "superheroes\\" + character_list[cp]))

    start_new_thread(threaded_client, (conn, players_data, cp))
    cp += 1
