import pygame
from network import Network
import pickle
pygame.font.init()

width = 950
height = 700
win = pygame.display.set_mode((width, height))
foto = pygame.image.load('rpsls.png')
fotoSpock = pygame.image.load('spock.jpg')
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128,128,128))
    imagem(275,10)

    if not(game.connected()):
        font = pygame.font.SysFont("freesans", 80)
        text = font.render("Esperando oponente...", 1, (255,255,255), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("freesans", 60)
        text = font.render("Você", 1, (0, 255,255))
        win.blit(text, (120, 200))

        text = font.render("Oponente", 1, (0, 255, 255))
        win.blit(text, (590, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Pronto", 1, (0, 0, 0))
            else:
                text1 = font.render("Esperando...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Pronto", 1, (0, 0, 0))
            else:
                text2 = font.render("Esperando...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (50, 350))
            win.blit(text1, (575, 350))
        else:
            win.blit(text1, (50, 350))
            win.blit(text2, (575, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("1 Rock", 10, 500, (0,0,0)), Button("2 Scissors", 190, 500, (255,0,0)), Button("3 Paper", 390, 500,(0,255,0)), Button("4 Lizard", 590, 500, (0,255,255)), Button("5 Spock", 790, 500,(255,0,255))]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("Você é o jogador", player)

    while run:


        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Vitória!!", 1, (255,255,255))
            elif game.winner() == -1:
                text = font.render("Empate!", 1, (255,255,255))
            else:
                text = font.render("Derrota...", 1, (255, 255, 255))

            win.blit(text, (width/2 - (text.get_width()/2) - 40 , height/2 - (text.get_height()/2) - 35))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def imagem(x,y):
    win.blit(foto,(x,y))

def imageSpock(x,y):
    win.blit(fotoSpock,(x,y))

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("freesans", 60)
        imageSpock(0,0)
        text = font.render("Clique", 1, (92,51,23))
        textDois = font.render("para", 1, (92,51,23))
        textTres = font.render("jogar!", 1, (92,51,23))
        win.blit(text, (400,300))
        win.blit(textDois, (410,400))
        win.blit(textTres, (410,500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()