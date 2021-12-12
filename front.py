from threading import Thread
import threading
import socket
from conf import PORT
from verificador import testaChute
from tkinter import *
from tkinter.ttk import *
import tkinter.font as font  
from tkinter import messagebox

class NewWindow(Toplevel):
     
    def __init__(self, master = None):
        super().__init__(master = master)
        self.title("Trivia Game")
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.janela2()
        print('\nConectado')

    def janela2(self):

        label = Label(self, text ="Dica: ____________")
        label.place(x = 550, y = 50)

        label2 = Label(self, text ="Jogadores: Pontuação")
        label2.place(x = 150, y = 50)

        text_rcv = Text(self)
        text_rcv['state'] = 'disabled'
        text_rcv.place(height=400,width=545, x = 350, y = 100)

        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: textConcat(sv))  # chama a função textConcat a cada modificação no texto

        text_entry = Entry(self, textvariable=sv)
        text_entry.place(width=100, height=25, x = 575, y = 515)
        text_entry.focus_set()

        # botao enviar
        btn_send = Button(self, text="Enviar",
                        command=lambda: self.confere(sv))
        btn_send.place(width=50, height=30, x = 600, y = 550)
        
        pont_rcv = Text(self)
        pont_rcv['state'] = 'disabled'
        pont_rcv.place(width=340, height=400,x = 5,  y = 100)

     
        thread2 = threading.Thread(target=self.receptor, args=[text_rcv, pont_rcv])
        thread2.start()

    def confere(self,message):
        mensagem = message.get() 
        resChute = testaChute(mensagem); 
        resChute = "3"+ resChute
        print("confere resChute:", resChute)
        messageSend(resChute)
        message.set('')
        
    def on_closing(self):
        var = "2" + jogador.get()
        print("on_closing var:", var)
        messageSend(var)
        self.destroy()

    def receptor(self,text_rcv, pont_rcv):
        while True:
            try:
                message = s.recv(1024).decode('utf-8') #recebe a mensagem do servidor
                print("receptor:",message)
                print("message[0]:",message[0])
                if message[0] == 'C':
                    texto = message[1:]
                    text_rcv['state'] = 'normal'
                    text_rcv.insert(END, f'{texto}\n') #insere o chute na tela
                    text_rcv['state'] = 'disabled'
                
            except:
                print('\nNão foi possível permanecer conectado no servidor!\n')
                print('Pressione <Enter> Para continuar...')
                s.close()
                break

  #if message == '/listaPlayers':
   #         listaPlayers = []
   #         listaPontos = []
   #         string = '/'
   #         with open("players.txt","r") as f1:
    #            for word in f1.readlines():
   #                 listaPlayers.append(word)
   #         with open("pontos.txt","r") as f2:
   #             for word in f2.readlines():
   #                 listaPontos.append(word)
   #         for i in range(len(listaPontos)):
   #             string+= str(listaPlayers[i].split('\n')[0]) + ': ' + str(listaPontos[i].split('\n')[0]) + " pontos" + '\n'
   #         print(string)
   #         for user in players:
   #             user.send(bytes(string, 'utf-8'))
    

def textConcat(sv):
    global texto
    texto = sv.get()
   
def playerSend(player):
    player = player.get()#NOME JOGADOR
    msg = "1"+str(player)
    print("playersend", msg)
    messageSend(msg)

def messageSend(mensagem):
    print("mensagemSend:",mensagem)
    s.send(bytes(f'{mensagem}', 'utf-8')) 
     
def main():
    
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((socket.gethostname(), PORT))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')
    global jogador
    global listaPlayers 
    global listaPontos 
    global linhas

    linhas = 0
    listaPlayers = []
    listaPontos = []

    root = Tk()
    root.title("Trivia Game")
    root.geometry("900x600")

    label_login = Message(root, text="\n\n\n\n\nDIGITE O NOME DO JOGADOR", font="Roboto 18 bold", width=500)
    label_login.place(x=40, y=300)
    label_login.pack(pady = 30)

    jogador = StringVar() 
    jogador.trace("w", lambda name, index, mode, sv=jogador: textConcat(jogador))
    inputText = Entry(root, textvariable=jogador, width=50)
    inputText.pack(pady = 20)

    btn = Button(root, text ="Jogar!", width=25)
    btn.bind("<Button>", lambda e: [NewWindow(root), root.withdraw(), playerSend(jogador)])
    btn.place(x=500, y=300)
    btn.pack(pady = 20)

    root.mainloop()

if __name__ == '__main__':
    
    main()