import string
def testaChute(texto, player, mestreAtual):

    with open("palavra.txt","r") as f:
        palavra =  f.readlines()
    
    texto = texto.lower()
    #testa se o texto é igual a palavra
    if texto == palavra[0]:
        linhaPlayer = 0
        linhaMestre = 0
        linhas = 0
        with open("players.txt","r") as f:
            for word in f.readlines():
                linhas+=1   
                if word == player + '\n':
                    linhaPlayer = linhas  
                if word == mestreAtual + '\n':
                    linhaMestre = linhas

        with open("pontos.txt","r") as f:
            total = f.readlines()
        with open("pontos.txt","w") as f:
            for i, line in enumerate(total):
                if i == linhaPlayer -1:
                    line = int(line) + 5
                    f.writelines(str(line) + '\n')
                elif i == linhaMestre -1:
                    line = int(line) + 2
                    f.writelines(str(line) + '\n')
                else:
                    f.writelines(line)
        return 0
    else:
        word1 = list(texto)
        resposta = list(palavra[0])
        contador = 0
        percent= int(len(resposta)/2) +1
        for i in range(int(len(resposta))):
            try: 
                if word1[i] == resposta[i]:
                    contador+=1
            except: 
                pass
        if contador >= percent:
            return 2
        else:
            return 1
 
     
 
    

