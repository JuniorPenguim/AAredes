class Game:
    def __init__(self, id):
        self.p1Went = False   #verificar se jogador já fez a jogada
        self.p2Went = False
        self.ready = False
        self.id = id          #id pra saber qual o id da partida lançada
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):  #função pra pegar o movimento do player x

        return self.moves[p]

    def play(self, player, move):  #função pra fazer o movimento e atualizar a variável do player x
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):    #função pra determinar se os dois players estão conectados
        return self.ready

    def bothWent(self):     #função pra verificar se os dois players fizeram um movimento
        return self.p1Went and self.p2Went

    def winner(self):     #função pra verificar as possibilidades de vitória

        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "1" and p2 == "2":
            winner = 0
        elif p1 == "1" and p2 == "3":
            winner = 1
        elif p1 == "1" and p2 == "4":
            winner = 0
        elif p1 == "1" and p2 == "5":
            winner = 1
        elif p1 == "2" and p2 == "1":
            winner = 1
        elif p1 == "2" and p2 == "3":
            winner = 0
        elif p1 == "2" and p2 == "4":
            winner = 0
        elif p1 == "2" and p2 == "5":
            winner = 1
        elif p1 == "3" and p2 == "1":
            winner = 0
        elif p1 == "3" and p2 == "2":
            winner = 1
        elif p1 == "3" and p2 == "4":
            winner = 1
        elif p1 == "3" and p2 == "5":
            winner = 0
        elif p1 == "4" and p2 == "1":
            winner = 1
        elif p1 == "4" and p2 == "2":
            winner = 1
        elif p1 == "4" and p2 == "3":
            winner = 0
        elif p1 == "4" and p2 == "5":
            winner = 0
        elif p1 == "5" and p2 == "1":
            winner = 0
        elif p1 == "5" and p2 == "2":
            winner = 0
        elif p1 == "5" and p2 == "3":
            winner = 1
        elif p1 == "5" and p2 == "4":
            winner = 1

        return winner

    def resetWent(self):   #função pra resetar os movimentos dos players
        self.p1Went = False
        self.p2Went = False