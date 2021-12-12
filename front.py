from threading import Thread
import threading
import socket
from conf import PORT
from tkinter import *
from tkinter.ttk import *
import tkinter.font as font  
from tkinter import messagebox
import time

class NewWindow(Toplevel):
     
    def __init__(self, master = None):
        super().__init__(master = master)
        self.title("Trivia Game")
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        global palavra

        with open("palavra.txt","r") as f:
            palavra =  f.readlines()
        print("palavraaaa",palavra[0])

        if palavra[0] != '1':
            self.janela2('1')
        else:
            self.janelaMestre()

    def janelaMestre(self):
        file_palavra = open('palavra.txt', 'w')
        file_palavra.write('0')
        file_palavra.close()

 

        label = Label(self, text ="Você é o mestre!!!!")
        label.place(x = 450, y = 50)

        label2 = Label(self, text ="Escolha uma palavra para todos advinharem")
        label2.place(x = 100, y = 100)

        label3 = Label(self, text ="Escolha um dica para todos os jogadores")
        label3.place(x = 100, y = 200)
        

        svPalavra = StringVar() #input da palavra
        svPalavra.trace("w", lambda name, index, mode, sv=svPalavra: palavraConcat(sv))  # chama a função textConcat a cada modificação no texto

        text_palavra = Entry(self, textvariable=svPalavra)
        text_palavra.place(width=100, height=25, x = 450, y = 100)
        text_palavra.focus_set()


        svDica = StringVar() #input da dica
        svDica.trace("w", lambda name, index, mode, sv=svDica: dicaConcat(svDica))  # chama a função textConcat a cada modificação no texto

        text_dica = Entry(self, textvariable=svDica)
        text_dica.place(width=100, height=25, x = 450, y = 200)
        text_dica.focus_set()

        # botao enviar
        btn_send = Button(self, text="Enviar!",
                        command=lambda: [self.conferePalavra(svPalavra),self.confereDica(svDica), self.janela2('0'), btn_send.destroy()])
        btn_send.place(width=50, height=30, x = 100, y = 500)
        if palavra[0] != "1":
            self.janelaEspera()

    def janela2(self, palavraMestre):
        with open("dica.txt","r") as f:
            dica = f.readlines()
        svDica = dica[0]
        label = Label(self, text=svDica)
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

        if palavraMestre == '0':
            btn_send["state"] = DISABLED

        pontos = StringVar()
        pont_rcv = Entry(self, textvariable=pontos)
        pont_rcv['state'] = 'disabled'
        pont_rcv.place(width=340, height=400,x = 5,  y = 100)

        thread2 = threading.Thread(target=self.receptor, args=[text_rcv, pont_rcv, pontos, btn_send, svDica,label])
        thread2.start()

    def conferePalavra(self,palavra):
        mensagem = palavra.get() 
        mensagem = "4"+ mensagem
        print("confere palavra:", mensagem)
        messageSend(mensagem)
        palavra.set('')

    def confereDica(self,dica):
        mensagem = dica.get()

        file_dica = open('dica.txt', 'w')
        file_dica.write("Dica: " + mensagem)
        file_dica.close()


        mensagem = "5"+ mensagem
        print("confere dica:", mensagem)
        messageSend(mensagem)
        dica.set('')
        


    def confere(self,message):
        mensagem = message.get() 
        mensagem = "3"+ mensagem
        print("confere resChute:", mensagem)
        messageSend(mensagem)
        message.set('')
        
    def on_closing(self):
        var = "2" + jogador.get()
        print("on_closing var:", var)
        messageSend(var)
        self.destroy()

    def atualizaPontos(self,tela,pontos):
        pontos.set('')
        tela['state'] = 'normal'
        listaPontos = []
        listaPlayers = []
        with open("players.txt","r") as f:
            newline = []
            for word in f.readlines():
                listaPlayers.append(word)
        with open("pontos.txt","r") as f2:
            for word in f2.readlines():
                listaPontos.append(word)
        texto = '\n'
        for i in range(len(listaPontos)):
            if listaPlayers[i] != '\n':
                texto +=  str(listaPlayers[i]) + ": " + str(listaPontos[i]) + ' pontos '
        pontos.set(texto)
        tela.insert(END, '\n')
        tela['state'] = 'disabled'
        
    def receptor(self,text_rcv, pont_rcv, pontos, btn_send, svDica, label):
        while True:
            try:
                message = s.recv(1024).decode('utf-8') #recebe a mensagem do servidor
                print("receptor:",message)
                print("message[0]:",message[0])
                
                if message[0] == 'C':
                    text_rcv['state'] = 'normal'
                    texto = message[1:]
                    text_rcv.insert(END, f'{texto}\n') #insere o chute na tela
                    self.atualizaPontos(pont_rcv, pontos)
                    text_rcv['state'] = 'disabled'

                if message[0] == 'A':
                    text_rcv['state'] = 'normal'
                    self.atualizaPontos(pont_rcv, pontos)
                    btn_send["state"] = DISABLED
                    text_rcv['state'] = 'disabled'

                if message[0] == 'D':
                    svDica.set('')
                    texto = message[1:]
                    label['state'] = 'normal'
                    print("svdica:", texto)
                    svDica.set(texto)
                    label['state'] = 'disabled'
                
                if message[0] == 'J':
                    self.janela2()
            except:
                print('\nNão foi possível permanecer conectado no servidor!\n')
                print('Pressione <Enter> Para continuar...')
                s.close()
                break



def dicaConcat(sv):
    global dica
    dica = sv.get()

def palavraConcat(sv):
    global palavra
    palavra = sv.get()

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
    btn.bind("<Button>", lambda e: [playerSend(jogador), root.withdraw(), NewWindow(root)])
    btn.place(x=500, y=300)
    btn.pack(pady = 20)
    
    root.mainloop()

if __name__ == '__main__':
    
    main()