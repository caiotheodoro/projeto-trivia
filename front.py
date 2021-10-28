from conf import PORT
from threading import Thread
from tkinter import *
import string
import socket


def receptor(tela):

    while True:
        tela['state'] = 'normal'
        msg = s.recv(1024).decode()
        tela.insert(END, f'{msg.split(":",1)[0]}')
        tela['state'] = 'disabled'



def main(player):
    # iniciar tkinter
    root = Tk()
    
    # janela tkinter
    root.geometry("400x400")
    root.minsize(height=400, width=400)
    root.title(f"Jogo trivia | Jogador {player}")

    # input de texto
    text_rcv = Text(root, font="Roboto 14 bold")
    text_rcv['state'] = 'disabled'
    text_rcv.place(width=390, height=330, x=5, y=5)

    # config input de texto
    sv = StringVar()
    input_text = Entry(root, font="Roboto 14 bold", textvariable=sv)
    input_text.place(width=300, height=30, x=5, y=365)
    input_text.focus_set()

    # botao enviar
    btn_try = Button(root, text="Tentar", font="Roboto 14 bold")
    btn_try.place(width=85, height=30, x=310, y=360)



    Upper_right = Label(root,text ='Dica: Fruta') #painel onde ficara a dica ***organizar em txt***
    Upper_right.place(relx = 1.0,
                    rely = 0.0,
                    anchor ='ne')

                  
    t = Thread(target=receptor, args=(text_rcv))
    t.start()

    # loop tkinter  (mainloop)
    root.mainloop()


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), PORT))
    player = input('Qual o seu nick? ')
    s.send(player.encode())
    main(player)
