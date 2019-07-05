import socket
from _thread import *
import pickle
from game import Game

server = "192.168.0.8"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #conexão socket

try:    #verificar se a porta e o ip conectam tranquilamente
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) #tempo esperado pra conexão
print("Esperando por uma conexão, Servidor Inicializado!")

connected = set()
games = {} #dicionário para guardar os jogos, passando ID como chave
idCount = 0 #contador de partidas


def threaded_client(conn, p, gameId):
    global idCount #variável global pra saber quantos jogos estão rodando
    conn.send(str.encode(str(p)))

    reply = ""
    while True: #função roda constatemente recebendo dados do cliente
        try:
            data = conn.recv(4096).decode()

            if gameId in games: #verifica se o ID da partida ainda existe no dicionário de partidas
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset": #verifica se o jogo precisa ser resetado
                        game.resetWent()
                    elif data != "get": #verifica se o dado é um movimento
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game)) #empacota a partida, envia pro cliente que desempacota e faz movimentos
            else:
                break
        except:
            break

    print("Conexão Perdida")
    try:
        del games[gameId]
        print("Fechando Jogo", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True: #função pra verificar os pares de jogos abertos
    conn, addr = s.accept()
    print("Conectado em:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2 #define qual o id da partida
    if idCount % 2 == 1:  #if para dizer que o número de players é ímpar e precisa conectar um player novo
        games[gameId] = Game(gameId)
        print("Criando um jogo novo...")
    else: #existe um número par de players e o jogo já pode iniciar
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))