import socket
from threading import Thread
from conf import PORT


def dispatch(client, player):
    while True:
        message = client.recv(1024).decode('utf-8')
        for user in players:
            user.send(bytes(f'{player}: {message}', 'utf-8'))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 3000))
s.listen(2)

players = list()
while True:
    client, address = s.accept()
    players.append(client)
    player = client.recv(1024).decode('utf-8')
    print(f'{player} conectou.  {address}')
    Thread(target=dispatch, args=(client, player)).start()
client.close()
