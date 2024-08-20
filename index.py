# BLACK JACK - PROJETO DE MARTIM GOMES E EDUARDO HENRIQUES
# 9ºA - Externato Champagnat
# ©	| O acesso a este código é interdito a pessoal não autorizado ou sem involvemento no desenvolvimento do mesmo

### Importações

from random import randint, choice
from math import floor
from time import sleep
from os import system, path
import threading

sons = False

try:
    from pygame import mixer
    mixer.init()
    sons = True
except:
    # Som falhou ao carregar
    input("Erro: Efeitos sonoros não serão carregados. Instala o pygame ('pip install pygame' no Terminal) para corrigir! (Enter) ")

###

### Classes

class jogadorClasse():
    def __init__(self):
        self.cartas = []
        self.soma_dos_valores_das_cartas = 0
        self.jogador_local = False
        self.mesa = False
        self.razao_perder = ""
        self.razao_ganhar = ""
        self.double_down = False

### Lista de Cartas

cartas = ['Ás de Paus', '2 de Paus', '3 de Paus', '4 de Paus', '5 de Paus', '6 de Paus', '7 de Paus', '8 de Paus', '9 de Paus', '10 de Paus', 'Valete de Paus', 'Dama de Paus', 'Rei de Paus',
          'Ás de Copas', '2 de Copas', '3 de Copas', '4 de Copas', '5 de Copas', '6 de Copas', '7 de Copas', '8 de Copas', '9 de Copas', '10 de Copas', 'Valete de Copas', 'Dama de Copas', 'Rei de Copas',
          'Ás de Ouros', '2 de Ouros', '3 de Ouros', '4 de Ouros', '5 de Ouros', '6 de Ouros', '7 de Ouros', '8 de Ouros', '9 de Ouros', '10 de Ouros', 'Valete de Ouros', 'Dama de Ouros', 'Rei de Ouros',
          'Ás de Espadas', '2 de Espadas', '3 de Espadas', '4 de Espadas', '5 de Espadas', '6 de Espadas', '7 de Espadas', '8 de Espadas', '9 de Espadas', '10 de Espadas', 'Valete de Espadas', 'Dama de Espadas', 'Rei de Espadas']

cartas_originais = cartas.copy()

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
                    e = int(input("Escolhe o valor do teu 'Ás' (1 ou 11): "))
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
        cartas.remove(carta)

# Funções para cada Ação
        
def hit(jogador): # Ao dar hit, o jogador recebe uma carta aleatória. Como o professor especificou que as cartas não devem repetir, podemos retirar a carta que calhar das opções
    nova_carta = choice(cartas)

    jogador.cartas.append(nova_carta)
    jogador.soma_dos_valores_das_cartas += obterValorDeCarta(nova_carta, jogador)

    cartas.remove(nova_carta) # Para que não seja escolhida de novo mais tarde

    if jogador.jogador_local == True: # Se não fosse isto, parecia que todos os jogadores eram o utilizador
        limparEcra()
        input("Escolheste a opção 'Pedir Carta (Hit)'!\n\nRecebeste a seguinte carta... (Enter) ")
        print(f"\n- {nova_carta}")
        print(f"\n\nA soma do valor das tuas cartas agora é {jogador.soma_dos_valores_das_cartas}!\n")
        if sons and jogador.soma_dos_valores_das_cartas == 21:
            mixer.Sound.play(mixer.Sound("win.wav"))
            sleep(1.6)
            mixer.Sound.play(mixer.Sound("blackjack.wav"))
            
        input("Continuar... ")
    else:
        input("Escolheu a opção 'Pedir Carta (Hit)'!\n\nRecebeu a seguinte carta... (Enter) ")
        print(f"\n- {nova_carta}\n")
        input("Continuar... ")

def stand(jogador):
    if jogador.jogador_local == True:
        limparEcra()
        print("Escolheste manter. Nenhumas alterações foram feitas às tuas cartas.\n\n")
        input("Continuar... ")
    else:
        print("Escolheu manter. Nenhumas alterações foram feitas às suas cartas.\n\n")
        input("Continuar... ")

aposta = 0

def doubledown(jogador):
    global aposta
    nova_carta = choice(cartas)

    jogador.cartas.append(nova_carta)
    jogador.soma_dos_valores_das_cartas += obterValorDeCarta(nova_carta, jogador)

    cartas.remove(nova_carta) # Para que não seja escolhida de novo mais tarde

    if jogador.jogador_local == True: aposta = aposta * 2 # Para que, no caso dos bots, a aposta do jogador não seja afetada

    jogador.double_down = True

    if jogador.jogador_local == True:
        limparEcra()
        print("Escolheste duplicar (Double Down). A tua aposta inicial foi duplicada, recebeste uma carta e terás de manter até ao final do jogo.")
        input("Continuar... ")
    else:
        print("Escolheu duplicar (Double Down). A sua aposta inicial foi duplicada, recebeu uma carta e terá de manter até ao final do jogo.")
        input("Continuar... ")

    
opcoes_funcoes = {
    "Pedir Carta (Hit)": hit,
    "Manter (Stand)": stand,
    "Duplicar (Double Down)": doubledown
}

#

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
rondas_totais = 3
upcard_card = ""
aposta_em_jogador = 0
dinheiro = 0

if not path.exists('database.txt'): # Se a base de dados não existir, o Python cria automaticamente
    with open('database.txt', 'w') as file:
        file.write("money=50") # Valor inicial do dinheiro

with open('database.txt', 'r') as file:
    # Ler a base de dados para obter o dinheiro guardado da sessão passada
    conteudo = file.read()

    variables = conteudo.split('=')

    if 'money' in variables[0]:
        dinheiro_guardado = int(variables[1])
    else:
        dinheiro_guardado = 0

    dinheiro = dinheiro_guardado

limparEcra()

print("Bem-vindo(a) ao Blackjack Python!")
print(f"O teu dinheiro: {dinheiro}$")
print("\n")
input("Começar (Enter) ")
print("\n")

limparEcra()

while True:
    ronda += 1

    limparEcra()
    print(f"\n--- RONDA {ronda} / {rondas_totais} -----------------------")

    aposta = float(input("Quanto dinheiro gostarias de apostar? "))
    aposta = floor(aposta)

    # Loop de Rondas

    input("\nIrás agora receber as tuas cartas. Analisa-as com atenção! (Enter) ") # Isto só é um input para permitir que o jogador skipe

    if sons: mixer.Sound.play(mixer.Sound("select.wav"))

    # Dar cartas a todos os jogadores

    cartas = cartas_originais.copy()

    for j in jogadores:
        if len(j.cartas) > 0: j.cartas.clear()
        j.soma_dos_valores_das_cartas = 0
        darCartasAJogador(j)
    upcard_card = mesa.cartas[0]

    acao_loops = 1

    while acao_loops <= 3: # Loop para as 3 ações por jogador
        acao_loops += 1

        opcao_escolhida = ""
        opcoes = ["Pedir Carta (Hit)", "Manter (Stand)", "Duplicar (Double Down)"]

        limparEcra()
        # Mostar cartas ao jogador

        print("\n---- AS TUAS CARTAS ----")
        for carta in localPlayer.cartas:
            print(carta)
        print("------------------------")
        print(f"Soma do valor das cartas: {localPlayer.soma_dos_valores_das_cartas}")
        
        input("\nContinuar... ")

        # Aposta em um Jogador

        if acao_loops != 2:
            limparEcra()

            print("\n---- APOSTA NUM JOGADOR ----")
            print("\n\nPodes agora apostar num jogador! Se o jogador em que apostares ganhar o jogo, recebes 1/3\n da tua aposta de volta, mesmo que percas!")
            while True:
                aposta_em_jogador_por_validar = input("\n\nInsere o número do jogador (1-5), ou 0 (nenhum) para continuares: ")
                if aposta_em_jogador_por_validar.isnumeric() and int(aposta_em_jogador_por_validar) >= 0 and int(aposta_em_jogador_por_validar) <= 5:
                    aposta_em_jogador = int(aposta_em_jogador_por_validar)
                    break
                else:
                    print("Erro! Tenta novamente.")

        #

        if sons: mixer.Sound.play(mixer.Sound("select.wav"))

        # Ações

        for jogador in jogadores:
            limparEcra()
            if jogador.jogador_local == False:
                # Não é o utilizador, portanto vai ser ação do bot
        
                nome_jogador = ""

                print("------------------------")
                if jogador.mesa == False:
                    print(f"É A VEZ DO JOGADOR {jogadores.index(jogador)}!\nA carta visível deste jogador (apenas para ti) é {jogador.cartas[0]} (valendo {obterValorDeCarta(jogador.cartas[0],jogador)})")
                else:
                    print(f"É A VEZ DA MESA!\nA carta visível da mesa é {upcard_card} (valendo {obterValorDeCarta(upcard_card, mesa)})")

                print("\nA pensar...")
                espera = randint(1,3)
                sleep(espera)

                # Escolher opção (Bot)

                #If hand total is 11 or lower: Always Hit, as there's little risk of busting with such a low hand total.
                #If hand total is 12 to 16 (inclusive): Consider the dealer's upcard. If the dealer's upcard is 7 or higher, Hit; otherwise, Stand. This is because the dealer has a good chance of having a strong hand when their upcard is 7 or higher, so the player should try to improve their hand.
                #If hand total is 17 or higher: Stand, as the risk of busting is higher with a hand total of 17 or above.

                if jogador.soma_dos_valores_das_cartas <= 11:
                    opcao_escolhida = "Pedir Carta (Hit)"
                elif jogador.soma_dos_valores_das_cartas >= 12 and jogador.soma_dos_valores_das_cartas <= 16:
                    if obterValorDeCarta(upcard_card, jogador) >= 7:
                        opcao_escolhida = "Pedir Carta (Hit)"
                    else:
                        opcao_escolhida = "Manter (Stand)"
                elif jogador.soma_dos_valores_das_cartas == 21:
                    opcao_escolhida = "Manter (Stand)"
                else:
                    opcao_escolhida = "Manter (Stand)"

                chance_de_jogada_random = randint(1,10)
                if jogador.mesa: chance_de_jogada_random = randint(1,23)
                if jogador.soma_dos_valores_das_cartas != 21 and chance_de_jogada_random == 1:
                    opcao_escolhida = choice(opcoes)

                if opcoes_funcoes[opcao_escolhida]:
                    opcoes_funcoes[opcao_escolhida](jogador)

                #

                print("------------------------")
            else:
                # É o utilizador

                atual_opcao_index = -1
                stop = False

                def mostrarInput(input_event):
                    global opcao_escolhida
                    input("")
                    if sons: mixer.Sound.play(mixer.Sound("select.wav"))
                    opcao_escolhida = opcoes[atual_opcao_index]
                    input_event.set()  # Set the event to notify the main thread

                input_event = threading.Event()
                inputThread = threading.Thread(target=mostrarInput, args=(input_event,))
                inputThread.start()

                while jogador.double_down == False:
                    atual_opcao_index += 1
                    if atual_opcao_index >= len(opcoes): atual_opcao_index = 0

                    opcoesString = ""
                    setaString = ""

                    for o in opcoes:
                        if opcoes.index(o) != 0:
                            opcoesString += "          " + o
                        else:
                            opcoesString += o
                    
                    seta = "↑↑"

                    limparEcra()

                    print("------------------------")
                    print("É A TUA VEZ DE JOGAR!\nSELECIONA UMA OPÇÃO\n")
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
                if jogador.double_down == True:
                    opcao_escolhida = "Manter (Stand)"

                if opcoes_funcoes[opcao_escolhida]:
                    opcoes_funcoes[opcao_escolhida](jogador)
                limparEcra()
                sleep(0.5)
    limparEcra()

    tocheck = jogadores.copy()  # Includes players that need to be determined if they won or lost (including the dealer)
    winners = []
    losers = []

    if mesa.soma_dos_valores_das_cartas == 21:  # Dealer has Blackjack! Any player who doesn't have Blackjack loses.
        mesa.razao_ganhar = "Conseguiu o Blackjack"
        tocheck.remove(mesa)
        for j in tocheck:
            if j.soma_dos_valores_das_cartas != 21:
                losers.append(j)
                j.razao_perder = "A mesa obteu o Blackjack, enquanto o jogador não o conseguiu fazer"
    else:
        # If the dealer doesn't have Blackjack...
        for j in tocheck:
            if j.soma_dos_valores_das_cartas == 21:
                winners.append(j)
                j.razao_ganhar = "Conseguiu o Blackjack"
                tocheck.remove(j)

        if mesa.soma_dos_valores_das_cartas > 21:
            losers.append(mesa)
            mesa.razao_perder = "Estourou (Bust)"
            tocheck.remove(mesa)

            # Remove players who busted themselves
            for j in tocheck:
                if j.soma_dos_valores_das_cartas > 21:
                    winners.append(j)
                    j.razao_ganhar = "A mesa estourou a sua mão"
                    tocheck.remove(j)

            # Identify players who win when the dealer busts
            for j in tocheck:
                winners.append(j)
                j.razao_ganhar = "A mesa estourou a sua mão"
                tocheck.remove(j)

    # Now, handle the remaining players
    for j in tocheck:
        if j.soma_dos_valores_das_cartas > 21:
            losers.append(j)
            j.razao_perder = "Estourou (Bust)"
        elif j != mesa and j.soma_dos_valores_das_cartas <= 21:
            if mesa.soma_dos_valores_das_cartas > 21:
                winners.append(j)
                j.razao_ganhar = "Mão maior que a mesa (Mesa estourou)"
            elif j.soma_dos_valores_das_cartas > mesa.soma_dos_valores_das_cartas:
                winners.append(j)
                j.razao_ganhar = "Maior mão que a mesa"
            else:
                losers.append(j)
                j.razao_perder = "Mão menor ou igual à mesa"

    # Mostrar resultados

    print("-----FIM DA RONDA------\n")
    input("Vamos atentar nos resultados da ronda... (Enter) ")
    print("\n")
    print(f"Mesa: {mesa.soma_dos_valores_das_cartas} Pontos\n")

    print("VENCEDORES-----\n")
    for j in winners:
        if j.mesa == False:
            if j.jogador_local:
                if sons: mixer.Sound.play(mixer.Sound("win.wav"))
                print(f"- Jogador {jogadores.index(j)} (Tu) - {j.soma_dos_valores_das_cartas} Pontos - [{j.razao_ganhar}]")
            else:
                if aposta_em_jogador != jogadores.index(j):
                    print(f"- Jogador {jogadores.index(j)} - {j.soma_dos_valores_das_cartas} Pontos - [{j.razao_ganhar}]")
                else:
                    print(f"- Jogador {jogadores.index(j)} (APOSTA) - {j.soma_dos_valores_das_cartas} Pontos - [{j.razao_ganhar}]")
        #else:
        #    print(f"- Mesa [{j.razao_ganhar}]")
        sleep(0.75)
    sleep(1.25)
    print("\nPERDEDORES-----\n")
    for j in losers:
        if j.mesa == False:
            if j.jogador_local:
                if sons: mixer.Sound.play(mixer.Sound("lose.wav"))
                print(f"- Jogador {jogadores.index(j)} (Tu) - {j.soma_dos_valores_das_cartas} Pontos - [{j.razao_perder}]")
            else:
                if aposta_em_jogador != jogadores.index(j):
                    print(f"- Jogador {jogadores.index(j)} - {j.soma_dos_valores_das_cartas} Pontos - [{j.razao_perder}]")
                else:
                    print(f"- Jogador {jogadores.index(j)} (APOSTA) - {j.soma_dos_valores_das_cartas} Pontos - [{j.razao_perder}]")
        #else:
        #    print(f"- Mesa [{j.razao_perder}]")
        sleep(0.75)
    print("\n")
    input("Continuar... ")
    limparEcra()

    print("------------------------")
    if localPlayer in winners:
        print(f"Parabéns, ganhaste a ronda!\n\nAposta: {aposta}$\nGanhos: +{floor(aposta * 1.5)}$")
        dinheiro += floor(aposta * 1.5)
    else:
        print(f"Uh oh, perdeste a ronda!\n\nAposta: {aposta}$\nPerdas: -{aposta}$")
        dinheiro -= aposta

    if jogadores[aposta_em_jogador] in winners:
        dinheiro += floor(aposta / 3)
        print(f"\nO jogador no qual apostaste venceu o jogo, pelo que tens direito a +{floor(aposta / 3)}$ adicionais!")

    aposta_em_jogador = 0

    with open('database.txt', 'w') as file: # Atualizar a base de dados com o valor atual de dinheiro
        file.write(f"money={dinheiro}")

    input("Continuar... ")