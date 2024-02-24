# BLACK JACK - PROJETO DE MARTIM GOMES E EDUARDO HENRIQUES
# 9ºA - Externato Champagnat
# ©	| O acesso a este código é interdito a pessoal não autorizado ou sem involvemento no desenvolvimento do mesmo

### Importações

from random import randint, choice
from math import floor
from time import sleep
from os import system
import threading

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
                    e = int(input("Obtiveste um Ás. Escolhe o seu valor (1 ou 11): "))
                    if e == 11 or e == 1:
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

def limparEcra():
    system('cls||clear')

# Criar Jogadores

jogadores = []

mesa = jogadorClasse()
mesa.mesa = True
jogadores.append(mesa)

for i in range(1,6): # mais três jogadores
    j = jogadorClasse()
    jogadores.append(j)

localPlayer = jogadores[1]
localPlayer.jogador_local = True # O jogador local é quem está a dar run neste programa, e é sempre o jogador 1 (sendo o 0 a mesa)

# Início

ronda = 0

print("Bem-vindo(a) ao Blackjack Python!")

while True:
    ronda += 1

    limparEcra()
    print(f"\n--- RONDA {ronda} -----------------------")

    # Loop de Rondas

    if ronda == 1:
        input("\nIrás agora receber as tuas cartas. Analisa-as com atenção! (Enter) ") # Isto só é um input para permitir que o jogador skipe
    else:
        input("\nIrás agora receber duas novas cartas. Estas são as tuas cartas atuais... (Enter) ") # Isto só é um input para permitir que o jogador skipe

    # Dar cartas a todos os jogadores

    for j in jogadores:
        darCartasAJogador(j)

    mesa.cartas.pop() # Utilizamos pop() para que a segunda carta da mesa seja apagada da sua posse, recebendo assim a mesa apenas uma carta como suposto

    # Mostar cartas ao jogador

    print("\n---- AS TUAS CARTAS ----")
    for carta in localPlayer.cartas:
        print(carta)
    print("------------------------")
    print(f"Soma do valor das cartas: {localPlayer.soma_dos_valores_das_cartas}")

    input("\nContinuar... ")

    # Ações

    for jogador in jogadores:
        limparEcra()
        if jogador.jogador_local == False:
            # Não é o utilizador, portanto vai ser ação do bot
    
            nome_jogador = ""

            print("------------------------")
            if jogador.mesa == False:
                print(f"É A VEZ DO JOGADOR {jogadores.index(jogador)}!\n")
            else:
                print(f"É A VEZ DA MESA!\n")

            print("A pensar...")

            print("------------------------")
            sleep(4)
        else:
            # É o utilizador

            atual_opcao_index = -1
            stop = False
            opcao_escolhida = ""
            opcoes = ["Perder Carta (Hit)", "Manter (Stand)"]

            def mostrarInput(input_event):
                global opcao_escolhida
                input("")
                opcao_escolhida = opcoes[atual_opcao_index]
                input_event.set()  # Set the event to notify the main thread

            input_event = threading.Event()
            inputThread = threading.Thread(target=mostrarInput, args=(input_event,))
            inputThread.start()

            while True:
                atual_opcao_index += 1
                if atual_opcao_index >= len(opcoes): atual_opcao_index = 0

                print("------------------------")
                opcoesString = ""
                setaString = ""

                for o in opcoes:
                    if opcoes.index(o) != 0:
                        opcoesString += "         " + o
                    else:
                        opcoesString += o
                
                seta = "↑↑"

                limparEcra()

                print("É A TUA VEZ DE JOGAR! SELECIONA UMA OPÇÃO\n")
                print(opcoesString)
                for e in range(0, atual_opcao_index):
                    l = len(opcoes[atual_opcao_index])
                    setaString += "            "
                    for k in range(0,l+1):
                        setaString += " "
                setaString += seta
                print(setaString)
                print("\n")
                
                if input_event.is_set():  # Check if input event is set
                    break

                sleep(0.7)
            limparEcra()
            sleep(5)
            