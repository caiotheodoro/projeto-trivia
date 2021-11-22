from threading import Thread
import socket
from conf import PORT
import string
from verificador import testaChute
import tkinter as tk  
              # python 3

from tkinter import font as tkfont  # python 3


class SampleApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        self.frames["page_one"] = page_one(parent=container, controller=self)
        self.frames["page_two"] = page_two(parent=container, controller=self)

        self.frames["page_one"].grid(row=0, column=0, sticky="nsew")
        self.frames["page_two"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("page_one")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class page_one(tk.Frame):
    def __init__(self, parent, controller):
        # iniciar tkinter
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        # janela tkinter
        #geometry
        
   


        label_login = tk.Message(self, text="\n\n\n\n\nDigite o nome de usuario", font="Roboto 14 bold", width=300)
        label_login.place(x=40, y=200)
        label_login.pack()


        # chama a função textConcat a cada modificação no texto
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.textConcat(
            sv))  # chama a função textConcat a cada modificação no texto


        # config input de texto
        text_entry = tk.Entry(self, font="Roboto 14 bold", textvariable=sv)
        text_entry.place(width=300, height=30, x=50, y=200)
        text_entry.focus_set()
        text_entry.pack()
        # botao enviar
        btn_send = tk.Button(self, text="Conectar", font="Roboto 14 bold",
                        command=lambda: controller.show_frame("page_two"))
        btn_send.place(width=100, height=30, x=150, y=250)
        btn_send.pack()
                # loop tkinter  (mainloop)

    def textConcat(self,sv):
        texto = sv.get() # pega o texto digitado

    def player_send(self,player):
        player = player.get()
        s.send(bytes(player, 'utf-8'))



class page_two(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # janela tkinter
        
    

    
        # historico (lista)
        text_rcv = tk.Text(self, font="Roboto 14 bold")
        text_rcv['state'] = 'disabled'
        text_rcv.place(width=390, height=330, x=5, y=5)
        text_rcv.pack()


        # chama a função textConcat a cada modificação no texto
        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.textConcat(
            sv))  # chama a função textConcat a cada modificação no texto


        # config input de texto
        text_entry = tk.Entry(self, font="Roboto 14 bold", textvariable=sv)
        text_entry.place(width=300, height=30, x=5, y=365)
        text_entry.focus_set()
        text_entry.pack()
        # botao enviar
        btn_send = tk.Button(self, text="Enviar", font="Roboto 14 bold",
                        command=lambda: self.confere(sv))
        btn_send.place(width=85, height=30, x=310, y=365)
        btn_send.pack()
        t = Thread(target=self.receptor, args=(text_rcv,))
        t.start()

        Upper_right = tk.Label(self,text ='Dica: Fruta') #painel onde ficara a dica ***organizar em txt***
        Upper_right.place(relx = 1.0,
                        rely = 0.0,
                        anchor ='ne')
        Upper_right.pack()
        # loop tkinter  (mainloop)

    def receptor(self,tela):
        while True:
            tela['state'] = 'normal'
            message = s.recv(1024).decode('utf-8') #recebe a mensagem do servidor
            chute = testaChute(message.split(":",1)[1]); #verifica se o chute é valido (split para pegar apenas o chute)
            tela.insert(tk.END, f'{message.split(":",1)[0]}: {chute}\n') #insere o chute na tela
            tela['state'] = 'disabled'


    def confere(self,message):
        mensagem = message.get() 
        resChute = testaChute(mensagem); 
        s.send(bytes(resChute, 'utf-8'))
        message.set('')


    def textConcat(self,sv):
        
        texto = sv.get() # pega o texto digitado


if __name__ == '__main__':
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), PORT))
    app = SampleApp()
    app.mainloop()
