# BLACK JACK - PROJETO DE MARTIM GOMES E EDUARDO HENRIQUES
# 9ºA - Externato Champagnat
# ©	| O acesso a este código é interdito a pessoal não autorizado ou sem involvemento no desenvolvimento do mesmo

### Importações

from random import randint, choice
from math import floor
from requests import request

###

### Classes

class jogadorClasse():
    def __init__(self):
        self.cartas = []
        self.soma_dos_valores_das_cartas = 0
        self.jogador_local = False
        self.mesa = False

###

# Lista de Cartas

cartas = ['Ás de Paus', '2 de Paus', '3 de Paus', '4 de Paus', '5 de Paus', '6 de Paus', '7 de Paus', '8 de Paus', '9 de Paus', '10 de Paus', 'Valete de Paus', 'Dama de Paus', 'Rei de Paus',
          'Ás de Copas', '2 de Copas', '3 de Copas', '4 de Copas', '5 de Copas', '6 de Copas', '7 de Copas', '8 de Copas', '9 de Copas', '10 de Copas', 'Valete de Copas', 'Dama de Copas', 'Rei de Copas',
          'Ás de Ouros', '2 de Ouros', '3 de Ouros', '4 de Ouros', '5 de Ouros', '6 de Ouros', '7 de Ouros', '8 de Ouros', '9 de Ouros', '10 de Ouros', 'Valete de Ouros', 'Dama de Ouros', 'Rei de Ouros',
          'Ás de Espadas', '2 de Espadas', '3 de Espadas', '4 de Espadas', '5 de Espadas', '6 de Espadas', '7 de Espadas', '8 de Espadas', '9 de Espadas', '10 de Espadas', 'Valete de Espadas', 'Dama de Espadas', 'Rei de Espadas']

def obterValorDeCarta(carta, jogador):
    primeiro_caracter = carta[0]
    valor = 0 # Para retornar mais tarde

    if primeiro_caracter.isnumeric():
        valor = int(primeiro_caracter)
        if carta[1].isnumeric(): # se o segundo também for número
            num = primeiro_caracter + carta[1]
            valor = int(num)
    else:
        if carta.startswith("Ás"):
            if jogador.jogador_local == True:
                while True:
                    e = int(input("Obteste um Ás. Escolhe o seu valor (1 ou 11): "))
                    if e == 1 or e == 1:
                        valor = e
                        break
                    else:
                        print("Valor inválido.")
            else:
                valor = choice([1,11])
        elif carta.startswith("Valete") or carta.startswith("Dama") or carta.startswith("Rei"):
            valor = 10
    
    return valor

def darCartasAJogador(jogador):
    for i in range(0,2):
        carta = choice(cartas)
        valor = obterValorDeCarta(carta, jogador)

        jogador.cartas.append(carta)
        jogador.soma_dos_valores_das_cartas += valor


# Criar Jogadores

jogadores = []

mesa = jogadorClasse()
mesa.mesa = True
darCartasAJogador(mesa)
jogadores.append(mesa)

for i in range(1,3): # mais três jogadores
    j = jogadorClasse()
    darCartasAJogador(j)
    jogadores.append(j)

print(jogadores[2].cartas)
print(jogadores[2].soma_dos_valores_das_cartas)