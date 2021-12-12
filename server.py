import socket
import threading
import os
import time
from verificador import testaChute
import string

"""def listagem(client,player):
    client.recv(1024).decode('utf-8')
    while True:
        time.sleep(5)
        temp = ''
        for user in players:
            temp = ')' + str(user)
            user.send(bytes(temp,'utf-8'))
"""

def messagesTreatment(client,player):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print("|msg:", msg, "|")
            print("|player:", player, "|")
            indice = msg[0]
            texto = msg[1:]

            if indice == "1":  #cria jogador e ponto respectivo
                print("1:", texto)
                file_players = open('players.txt', 'a')
                file_pontos = open('pontos.txt', 'a')
                file_players.write(texto + "\n")
                file_pontos.write("0" + "\n")
                file_players.close()
                file_pontos.close()
                players.append(texto)
                texto = "C"+ players[player]+" entrou."
                if player == 0:
                    file_palavra = open('palavra.txt', 'w')
                    file_palavra.write('1')
                    file_palavra.close()
              
                broadcast(texto, client)

            if indice == "2": #apaga jogador e ponto respectivo
                print("2:", texto)
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
                saiu = "C"+ players[player]+" saiu."
                broadcast(saiu, client)

            if indice == "3":
                print("3:", texto)
                resposta = testaChute(texto,players[player])
                if resposta == 1:
                    texto = "C"+ players[player]+": "+ texto
                elif resposta == 0:
                    texto = "A"+ players[player]+ "Acertou!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                broadcast(texto, client)
            if indice == "4": #insere palavra
                print("4:", texto)
                texto = texto.lower()
                file_palavra = open('palavra.txt', 'w')
                file_palavra.write(texto)
                file_palavra.close()
            if indice == "5": #insere dica
                print("5:", texto)
                texto = texto.lower()
                file_dica = open('dica.txt', 'w')
                file_dica.write(texto)
                file_dica.close()
        except:
            deleteClient(client)
            break



def broadcast(msg, client):
    for clientItem in clients:
        try:
            print("broadcast")
            clientItem.send(bytes(f'{msg}', 'utf-8')) 
        except:
            deleteClient(clientItem)



def deleteClient(client):
    clients.remove(client)

if os.path.exists("players.txt"):
    os.remove("players.txt")
    os.remove("pontos.txt")

clients = list()
players = list()
def main():
    player = 0
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((socket.gethostname(), 3000))
        server.listen()
        
    except: 
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)
       
        print(f'{addr} conectou.')
        thread = threading.Thread(target=messagesTreatment, args=[client,player])
        thread.start()
        player += 1
if __name__ == '__main__':
    main()