import socket
from threading import Thread
from conf import PORT
import os
import time

def dispatch(client, player):
    while True:
        message = client.recv(1024).decode('utf-8')
        indice = message[0]


        if indice == "1":
            texto = message[1:]
            linha = 0
            linhas = 0
            with open("players.txt","r") as f:
                newline = []
                for word in f.readlines():
                    linhas+=1   
                    if word == texto + '\n':
                        linha = linhas   
                    newline.append(word.replace(texto, ""))
            with open("players.txt","w") as f:
                for line in newline:
                    f.writelines(line)

            with open("pontos.txt","r") as f:
                total = f.readlines()
            with open("pontos.txt","w") as f:
                for i, line in enumerate(total):
                    if i == linha -1:
                        f.writelines("\n")
                    else:
                        f.writelines(line)
        for user in players:
            user.send(bytes(f'{player}: {message}', 'utf-8'))


def listagem(client,player):
    client.recv(1024).decode('utf-8')
    while True:
        time.sleep(5)
        temp = ''
        for user in players:
            temp = ')' + str(user)
            user.send(bytes(temp,'utf-8'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 3000))
s.listen(2)



players = list()

if os.path.exists("players.txt"):
    os.remove("players.txt")
    os.remove("pontos.txt")

while True:
    try:
        client, address = s.accept()
        players.append(client)
        player = client.recv(1024).decode('utf-8')
        print(f'{player} conectou.  {address}')
        t1 = Thread(target=dispatch, args=(client, player))
        t2 = Thread(target=listagem, args=(client,player))
        t1.start()
        t2.start()
    except ConnectionAbortedError:
        break
    except:
        print("Error")
        client.shutdown(socket.SHUT_RDWR)
client.close()