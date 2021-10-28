from conf import PORT
import socket
from threading import Thread


def dispatch(client, player):
    while True:
        message = client.recv(1024).decode()
        for c in clientes:
            c.send(bytes(f'{player}: {message}', 'utf-8'))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(2)

clientes = list()

while True:
    client, address = s.accept()
    clientes.append(client)
    player = client.recv(1024).decode()
    print(f'{player} conectou.  {address}')
    Thread(target=dispatch, args=(client, player)).start()
client.close()