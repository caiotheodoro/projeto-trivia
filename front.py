from threading import Thread
import threading
import socket
from conf import PORT
from tkinter.ttk import *
from tkinter import *
import tkinter.font as font  
from tkinter import messagebox
import time
import sys

class NewWindow(Toplevel):
     
    def __init__(self, master = None):
        super().__init__(master = master)
        self.title("Trivia Game")
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self['bg']='#6000FE'

        global palavra

        with open("palavra.txt","r") as f:
            palavra =  f.readlines()
        #print("palavraaaa",palavra[0])

     
       
        if palavra[0] != '1':
            self.janelaEspera()
        else:
            self.janelaMestre()

    def janelaEspera(self):
   
        Font_tuple = ("Comic Sans MS", 16, "bold")
    
        global labelEspera
        labelEspera = Label(self, text ="Mestre ainda não escolheu a palavra!\n Espere até o botão de Entrar no jogo ficar disponível. ",font=Font_tuple, fg="white", bg="#6000FE")
        labelEspera.place(x = 150, y = 100)

        
        global btn_entrar
        btn_entrar = Button(self, text="Entrar no jogo",
                        command=lambda: [self.janela2('1'), labelEspera.destroy(),btn_entrar.destroy() ], font=("Comic Sans MS", 20, "bold"), fg="white", bg="#7d6fb1")
        btn_entrar.place(width=200, height=60, x = 350, y = 200)
        btn_entrar["state"] = DISABLED

        thread3 = threading.Thread(target=self.esperaPalavra, args=[btn_entrar])
        thread3.start()

 
    

        # font=("Comic Sans MS", 14, "bold"), fg="white", bg="#6000FE"
    
    def esperaPalavra(self, btn_entrar):
      while True:
            time.sleep(2)
            with open("palavra.txt","r") as f:
                palavra =  f.readlines()
            if palavra[0] != '0':
                btn_entrar["state"] = NORMAL
                break
      
    def janelaMestre(self):
        file_palavra1 = open('palavra.txt', 'w')
        file_palavra1.write('0')
        file_palavra2 = open('tema.txt', 'w')
        file_palavra2.write('0')
        file_palavra3 = open('dica.txt', 'w')
        file_palavra3.write('0')
        file_palavra1.close()
        file_palavra2.close()
        file_palavra3.close()
        Font_tuple = ("Comic Sans MS", 16, "bold")
        Font_tuple2 = ("Arial", 12, "bold")
        label = Label(self, text ="Você é o mestre!", font=Font_tuple, fg="white", bg="#6000FE")
        label.place(x = 10, y = 560)

        label2 = Label(self, text ="Escolha uma palavra para advinharem: ",font=Font_tuple, fg="white", bg="#6000FE")
        label2.place(x = 100, y = 100)

        label3 = Label(self, text ="Escolha uma dica: ",font=Font_tuple, fg="white", bg="#6000FE")
        label3.place(x = 100, y = 200)
        

        label4 = Label(self, text ="Escolha um tema: ",font=Font_tuple, fg="white", bg="#6000FE")
        label4.place(x = 100, y = 300)
        

        svPalavra = StringVar() #input da palavra
        svPalavra.trace("w", lambda name, index, mode, sv=svPalavra: palavraConcat(sv))  # chama a função textConcat a cada modificação no texto

        text_palavra = Entry(self, textvariable=svPalavra, font=Font_tuple2)
        text_palavra.place(width=150,x = 100, y = 140)
        text_palavra.focus_set()


        svDica = StringVar() #input da dica
        svDica.trace("w", lambda name, index, mode, sv=svDica: dicaConcat(svDica))  # chama a função textConcat a cada modificação no texto

        text_dica = Entry(self, textvariable=svDica,font=Font_tuple2)
        text_dica.place(width=150,x = 100, y = 240)
        text_dica.focus_set()
            #7d6fb1
        svTema = StringVar() #input da dica
        svTema.trace("w", lambda name, index, mode, sv=svTema: temaConcat(svTema))  # chama a função textConcat a cada modificação no texto
        text_tema = Entry(self, textvariable=svTema,font=Font_tuple2)
        text_tema.place(width=150,x = 100, y = 340)
        text_tema.focus_set()

        # botao enviar
        
        global btn_start
        btn_start = Button(self, text="Inciar tempo",
                        command=lambda: [self.clock(clock_count, 90,0), messageSend('7'), self.disableButton(btn_start)], font=("Comic Sans MS", 14, "bold"), fg="white", bg="#7d6fb1") #59
        btn_start.place(width=140, height=30, x = 10, y = 520)

        btn_send = Button(self, text="Enviar!",
                        command=lambda: [time.sleep(0.5),self.conferePalavra(svPalavra),self.confereDica(svDica),self.confereTema(svTema), self.janela2('0'), btn_send.destroy(), label.destroy(), label2.destroy(), label3.destroy(), label4.destroy(),text_palavra.destroy(), text_dica.destroy(), text_tema.destroy() ], font=("Comic Sans MS", 14, "bold"), fg="white", bg="#6000FE")
        btn_send.place(width=70, height=30, x = 100, y = 400)
        # font=("Comic Sans MS", 14, "bold"), fg="white", bg="#6000FE"
        if palavra[0] != "1":
            self.janelaEspera()

    def janela2(self, palavraMestre):
        with open("dica.txt","r") as f:
            dica = f.readlines()

    
        svDica = dica[0]
        Font_tuple = ("Comic Sans MS", 16, "bold")
        label = Label(self, text=svDica, font=Font_tuple, fg="white", bg="#6000FE")
        label.place(x = 650, y = 50)

        with open("tema.txt","r") as f:
            tema = f.readlines()
        svTema = tema[0]
        label2 = Label(self, text=svTema, font=Font_tuple, fg="white", bg="#6000FE")
        label2.place(x = 650, y = 20)

        label3 = Label(self, text ="Jogadores: Pontuação", fg="white" ,bg="#6000FE", font=Font_tuple)
        label3.place(x = 50, y = 50)

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
                        command=lambda: self.confere(sv),  font=("Comic Sans MS", 14, "bold"), fg="#ffffff", bg="#7d6fb1")
        btn_send.place(width=70, height=30, x = 590, y = 550)


        btn_send["state"] = DISABLED
        if palavraMestre == '0':
            # hide btn_send
            btn_send.place_forget()

        pontos = StringVar()
        pont_rcv = Entry(self, textvariable=pontos)
        pont_rcv['state'] = 'disabled'
        pont_rcv.place(width=340, height=400,x = 5,  y = 100)


        global clock_count
        fontClock = ("ds-digital", 20, "bold")
        clock_count = Label(self, text='01:30',font=fontClock, fg="green", bg="black")	
        clock_count.place(x = 150, y = 5)
        #self.clock(clock_count, 30)


        with open("palavra.txt","r") as f: #_ _ _ _
            texto = f.readlines() #[a, b, a, c, a, x, i]
        global textoPreenche
        textoPreenche=[]
        textoPreenche[:0]=texto[0]
        global tamPalavra
        tamPalavra = len(textoPreenche)
        global tempoAparecer
        tempoAparecer = 90 / int(tamPalavra/2)
        aux = ""
        global underlines
        underlines = StringVar()
        for item in textoPreenche:
            aux += "_ "
        underlines.set(aux)
        global dicaPalavra
        dicaPalavra = Label(self, textvariable=underlines, font=Font_tuple, fg="white", bg="#6000FE")
        dicaPalavra.place(x = 350, y = 30)

        thread2 = threading.Thread(target=self.receptor, args=[text_rcv, pont_rcv, pontos, btn_send, svDica,label,text_entry,clock_count,label2, label3])
        thread2.start()


    def conferePalavra(self,palavra):
        mensagem = palavra.get() 
        mensagem = "4"+ mensagem
        messageSend(mensagem)
        palavra.set('')

    def confereDica(self,dica):
        mensagem = dica.get()

        file_dica = open('dica.txt', 'w')
        file_dica.write("Dica: " + mensagem)
        file_dica.close()


        mensagem = "5"+ mensagem
        messageSend(mensagem)
        dica.set('')
        
    def confereTema(self,palavra):
        mensagem = palavra.get() 

        file_dica = open('tema.txt', 'w')
        file_dica.write("Tema: " + mensagem)
        file_dica.close()

        mensagem = "8"+ mensagem
        messageSend(mensagem)
        palavra.set('')

    def disableButton(self, tela):
        tela["state"] = DISABLED	

    def clock(self, tela, minutes, counter):
        minut = int(minutes/60)
        minute = str(minut)
        second = str(minutes%60)
        
        tela.config(text=minute+':'+second)
        if(minutes > 0):
            if(minutes % 20 == 0 and counter < (tamPalavra/2) -1): #tempoAparecer
                aux=[]
                aux[:0]=underlines.get()
                if counter % 3 == 0:
                    soma = 0
                else:
                    soma = counter

                aux[counter*3 + soma] = textoPreenche[counter*2]
                textoFinal  = ''
                for item in aux:
                    textoFinal += item
                underlines.set(textoFinal)
                counter += 1

            tela.after(1000, lambda: self.clock(tela, minutes-1,counter))
        else:
            tela.config(text=minute+':'+second + ' Tempo esgotado!')
            messageSend("6")
            

    def confere(self,message):
        mensagem = message.get() 
        mensagem = "3"+ mensagem
        messageSend(mensagem)
        message.set('')
        
    def on_closing(self):
        var = "2" + jogador.get()
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
        
    def receptor(self,text_rcv, pont_rcv, pontos, btn_send, svDica, label,text_entry,clock_count, label2, label3):
        while True:
        
            try:
                message = s.recv(1024).decode('utf-8') #recebe a mensagem do servidor
                
                if message[0] == 'C':
                    text_rcv['state'] = 'normal'
                    texto = message[1:]
                    text_rcv.insert(END, f'{texto}\n') #insere o chute na tela
                    self.atualizaPontos(pont_rcv, pontos)
                    text_rcv['state'] = 'disabled'
                
                if message[0] == 'V':
                    text_rcv['state'] = 'normal'
                    texto = message[1:]
                    text_rcv.tag_config('verde', foreground='green')
                    text_rcv.insert(END, f'{texto}\n', 'verde') #insere o chute na tela verde
                    self.atualizaPontos(pont_rcv, pontos)
                    text_rcv['state'] = 'disabled'

                if message[0] == 'M':
                    text_rcv['state'] = 'normal'
                    texto = message[1:]
                    text_rcv.tag_config('amarelo', foreground='#CCCC00')
                    text_rcv.insert(END, f'{texto}\n', 'amarelo') #insere o chute na tela amarelo
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
                    svDica.set(texto)
                    label['state'] = 'disabled'

                if message[0] == 'F':
                    btn_send["state"] = DISABLED
                    time.sleep(3)
                    self.janelaEspera()
                    text_rcv.destroy()
                    pont_rcv.destroy()
                    btn_send.destroy()
                    label.destroy()
                    text_entry.destroy()
                    clock_count.destroy()
                    label2.destroy()
                    label3.destroy()
                    btn_start.destroy()

                if message[0] == 'N':
                    file_palavra1 = open('palavra.txt', 'w')
                    file_palavra1.write('0')
                    file_palavra1.close()
                    time.sleep(2)
                    self.janelaMestre()
                    text_rcv.destroy()
                    pont_rcv.destroy()
                    btn_send.destroy()
                    label.destroy()
                    text_entry.destroy()
                    clock_count.destroy()
                    label2.destroy()
                    label3.destroy()
                    labelEspera.destroy()
                    btn_entrar.destroy()
                    dicaPalavra.destroy()

                if message[0] == 'T':
                    self.clock(clock_count, 90,0) #59
                    btn_send["state"] = NORMAL

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

def temaConcat(sv):
    global tema
    tema = sv.get()

def palavraConcat(sv):
    global palavra
    palavra = sv.get()

def textConcat(sv):
    global texto
    texto = sv.get()
   
def playerSend(player):
    player = player.get()#NOME JOGADOR
    msg = "1"+str(player)
    messageSend(msg)

def messageSend(mensagem):
    s.send(bytes(f'{mensagem}', 'utf-8')) 
     
def main():
    
    global s

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((socket.gethostname(), PORT))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')
        
    global jogador, listaPlayers, listaPontos, listaPontos, listaPontos, linhas

    linhas = 0
    listaPlayers = []
    listaPontos = []

    root = Tk()
    root.title("Trivia Game")
    root.geometry("900x600")
    root['bg']='#6000FE'
    imgDigite = PhotoImage(file="images/titulo1.png")
    label_login = Label(root, text="\n\n\n\n\n",image=imgDigite,  width=800, bg="#6000FE")
    label_login.place(x=40, y=500)
    label_login.pack(pady = 100)

    jogador = StringVar() 
    jogador.trace("w", lambda name, index, mode, sv=jogador: textConcat(jogador))
    inputText = Entry(root, textvariable=jogador, width=30, font=("Arial", 20))
    inputText.pack(pady = 30)
    imgJogar = PhotoImage(file="images/jogar.png")
   



    btn = Button(root, text ="Jogar!", image=imgJogar, bg="#6000FE", borderwidth=0)
    btn.bind("<Button>", lambda e: [playerSend(jogador), root.withdraw(), NewWindow(root)])
    btn.place(x=500, y=300)
    btn.pack(pady = 40)
    
    root.mainloop()

if __name__ == '__main__':
    
    main()