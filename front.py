from tkinter import *
from threading import Thread
import socket
from conf import PORT
import string
from verificador import testaChute


def receptor(tela):
 

    while True:
        tela['state'] = 'normal'
        message = s.recv(1024).decode('utf-8') #recebe a mensagem do servidor
        chute = testaChute(message.split(":",1)[1]); #verifica se o chute é valido (split para pegar apenas o chute)
        tela.insert(END, f'{message.split(":",1)[0]}: {chute}\n') #insere o chute na tela
        tela['state'] = 'disabled'


def confere(message):
    mensagem = message.get() 
    resChute = testaChute(mensagem); 
    s.send(bytes(resChute, 'utf-8'))
    message.set('')


def textConcat(sv):
    
    texto = sv.get() # pega o texto digitado


def main(player):
      # iniciar tkinter
    root = Tk()
    
      # janela tkinter
    root.geometry("400x400")
    root.minsize(height=300, width=400)
    root.title(f"Jogo trivia | Jogador {player}")

 
     # historico (lista)
    text_rcv = Text(root, font="Roboto 14 bold")
    text_rcv['state'] = 'disabled'
    text_rcv.place(width=390, height=330, x=5, y=5)



    # chama a função textConcat a cada modificação no texto
    sv = StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: textConcat(
        sv))  # chama a função textConcat a cada modificação no texto


    # config input de texto
    text_entry = Entry(root, font="Roboto 14 bold", textvariable=sv)
    text_entry.place(width=300, height=30, x=5, y=365)
    text_entry.focus_set()

    # botao enviar
    btn_send = Button(root, text="Enviar", font="Roboto 14 bold",
                      command=lambda: confere(sv))
    btn_send.place(width=85, height=30, x=310, y=365)

    t = Thread(target=receptor, args=(text_rcv,))
    t.start()

    Upper_right = Label(root,text ='Dica: Fruta') #painel onde ficara a dica ***organizar em txt***
    Upper_right.place(relx = 1.0,
                    rely = 0.0,
                    anchor ='ne')

    # loop tkinter  (mainloop)
    root.mainloop()


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), PORT))
    player = input('nickname: ')
    s.send(bytes(player, 'utf-8'))
    main(player)
