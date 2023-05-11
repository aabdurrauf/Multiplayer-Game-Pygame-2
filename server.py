import socket
from _thread import *
import pickle
import pygame

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket.SOCK_STREAM
server = '172.30.48.1'
port = 5555
s.bind((server, port))

s.listen(2)
print("Waiting for a connection")

def threaded_client(conn, server_data, id_num):
    # conn.send(pickle.dumps(server_data[id_num]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            server_data[id_num] = data
            if not data:
                conn.send(str.encode("Disconnected"))
                break
            conn.sendall(pickle.dumps(server_data))
        except:
            print("Failed to send")
            break

    print("Connection Closed")
    conn.close()


server_data = []
id_num = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn, server_data, id_num))
    id_num += 1
