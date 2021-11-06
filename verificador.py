import string
def testaChute(texto):
    palavra = "abacaxi"
    texto = texto.lower()
     
    #testa se o texto é igual a palavra
    if texto == palavra:
        res = 'Acertou!'
        return res
    else:
        return texto
    

