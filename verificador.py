import string
def testaChute(texto, player):

    with open("palavra.txt","r") as f:
        palavra =  f.readlines()
    
    texto = texto.lower()
   #testa se o texto é igual a palavra
    if texto == palavra[0]:
        linha = 0
        linhas = 0
        with open("players.txt","r") as f:
            for word in f.readlines():
                linhas+=1   
                if word == player + '\n':
                    linha = linhas   

        with open("pontos.txt","r") as f:
            total = f.readlines()
        with open("pontos.txt","w") as f:
            for i, line in enumerate(total):
                if i == linha -1:
                    line = int(line) + 5
                    f.writelines(str(line) + '\n')
                else:
                    f.writelines(line)
        return 0
    else:
        return 1
 
     
 
    

