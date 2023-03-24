import pygame
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# import images
image1 = pygame.transform.scale(pygame.image.load('images/WPawn.png'), (100, 100))
image2 = pygame.transform.scale(pygame.image.load('images/WQueen.png'), (100, 100))
image3 = pygame.transform.scale(pygame.image.load('images/WKnight.png'), (100, 100))
image4 = pygame.transform.scale(pygame.image.load('images/WKing.png'), (100, 100))
image5 = pygame.transform.scale(pygame.image.load('images/WTower.png'), (100, 100))
image6 = pygame.transform.scale(pygame.image.load('images/WBishop.png'), (100, 100))
image7 = pygame.transform.scale(pygame.image.load('images/BPawn.png'), (100, 100))
image8 = pygame.transform.scale(pygame.image.load('images/BQueen.png'), (100, 100))
image9 = pygame.transform.scale(pygame.image.load('images/BKnight.png'), (100, 100))
image10 = pygame.transform.scale(pygame.image.load('images/BKing.png'), (100, 100))
image11 = pygame.transform.scale(pygame.image.load('images/BRook.png'), (100, 100))
image12 = pygame.transform.scale(pygame.image.load('images/BBishop.png'), (100, 100))

pion_blanc = [image5, image3, image6, image2, image4, image1]
pion_noir = [image11, image9, image12, image8, image10, image7]

# initialisation of pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))  # def of the screen
font = pygame.font.SysFont("calibri", 72)  # font
pygame.display.set_caption("chess")  # name of the window


# display of the screen
def chess_board(tour, chess, movement, r, passant):
    pionn = ["R", "N", "B", "Q", "K", "P"]
    pionb = ["r", "n", "b", "q", "k", "p"]
    for i in range(0, 5):
        for j in range(0, 5):
            pygame.draw.rect(screen, (225, 195, 154), pygame.Rect(200*i, 200*j, 100, 100))
            pygame.draw.rect(screen, (225, 195, 154), pygame.Rect(200*i+100, 200*j+100, 100, 100))
            pygame.draw.rect(screen, (133, 100, 77), pygame.Rect(100+200*i, 200*j, 100, 100))
            pygame.draw.rect(screen, (133, 100, 77), pygame.Rect(200*i, 200*j+100, 100, 100))
    for i in range(0, 7):
        pygame.draw.rect(screen, (255, 215, 0), pygame.Rect(100 + 100 * i, 0, 1.5, 800))
        pygame.draw.rect(screen, (255, 215, 0), pygame.Rect(0, 100 + 100 * i, 800, 1.5))

    if tour == -1:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, 800, 800), 3)
    else:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 800, 800), 3)

    # pawn:
    for j in range(0, 8):
        for i in range(0, 8):
            if chess[j, i][0] != "0":
                if chess[j, i][0] in pionn:
                    screen.blit(pion_noir[pionn.index(chess[j, i][0])], (i * 100, j * 100))
                else:
                    screen.blit(pion_blanc[pionb.index(chess[j, i][0])], (i * 100, j * 100))

    # red square for possible movement
    for square in movement:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(square[1] * 100 + 2, square[0]*100+2, 96, 96), 3)

    # green square for roque
    for square in r:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(square[1] * 100 + 2, square[0]*100+2, 96, 96), 3)

    # green square for en passant
    if passant[0] > -1:
        print(passant)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(passant[1] * 100 + 2, passant[0] * 100 + 2, 96, 96), 3)

    # display
    pygame.display.flip()


class Game:
    def __init__(self):
        self.pionn = ["R", "N", "B", "Q", "K", "P"]  # black player
        self.pionb = ["r", "n", "b", "q", "k", "p"]  # white player
        self.enemy = [self.pionn, None, self.pionb]  # list of player
        self.chess = np.array([["r0", "n", "b", "q", "k0", "b", "n", "r1"],
                               ["p", "p", "p", "p", "p", "p", "p", "p"],
                               ["0", "0", "0", "0", "0", "0", "0", "0"],
                               ["0", "0", "0", "0", "0", "0", "0", "0"],
                               ["0", "0", "0", "0", "0", "0", "0", "0"],
                               ["0", "0", "0", "0", "0", "0", "0", "0"],
                               ["P", "P", "P", "P", "P", "P", "P", "P"],
                               ["R2", "N", "B", "K2", "Q", "B", "N", "R3"]])

    def pawn(self, x, y, tour, p):
        movement = []
        passant = -1, -1

        if self.chess[y-1*tour, x] == "0" and 0 <= y-1*tour < 8:
            movement.append([y-tour, x])
            if -1 < y - 2 * tour < 8 and self.chess[y - 2 * tour, x] == "0" and y == 1+2.5*(tour+1):
                movement.append([y - 2 * tour, x])

        for i in range(-1, 3, 2):
            if -1 < x+i < 8 and self.chess[y-tour, x+i][0] in self.enemy[tour + 1]:
                movement.append([y-tour, x+i])

        # en passant:
        if p > -1 and y == 3+0.5*(-1*tour+1):
            if p == x + 1 and self.chess[y-tour, p] == '0':
                passant = y-tour, p
            if p == x - 1 and self.chess[y-tour, p] == '0':
                passant = y-tour, p

        return movement, passant

    def rook(self, x, y, tour):
        movement = []
        for i in range(-1, 2, 2):
            a = i
            while 0 <= a + y < 8:
                if self.chess[y+a, x] == "0":
                    movement.append([y+a, x])
                elif self.chess[y+a, x][0] in self.enemy[tour + 1]:
                    movement.append([y+a, x])
                    break
                else:
                    break
                a += i

        for i in range(-1, 2, 2):
            a = i
            while 0 <= a + x < 8:
                if self.chess[y, x + a] == "0":
                    movement.append([y, x + a])
                elif self.chess[y, x + a][0] in self.enemy[tour + 1]:
                    movement.append([y, x + a])
                    break
                else:
                    break
                a += i

        return movement

    def bishop(self, x, y, tour):
        movement = []
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                a = i
                b = j
                while 0 <= a + x < 8 and 0 <= b + y < 8:
                    if self.chess[y + b, x + a] == "0":
                        movement.append([y + b, x + a])
                    elif self.chess[y + b, x + a][0] in self.enemy[tour + 1]:
                        movement.append([y + b, x + a])
                        break
                    else:
                        break
                    a += i
                    b += j
        return movement

    def knight(self, x, y, tour):
        movement = []
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                if 0 <= y + 2*i < 8 and 0 <= x + j < 8 and self.chess[y + 2*i, x + j] == "0":
                    movement.append([y + 2*i, x + j])
                elif 0 <= y + 2*i < 8 and 0 <= x + j < 8 and self.chess[y + 2*i, x + j][0] in self.enemy[tour + 1]:
                    movement.append([y + 2*i, x + j])

        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                if 0 <= y + i < 8 and 0 <= x + 2 * j < 8 and self.chess[y + i, x + 2 * j] == "0":
                    movement.append([y + i, x + 2*j])
                elif 0 <= y + i < 8 and 0 <= x + 2 * j < 8 and self.chess[y + i, x + 2*j][0] in self.enemy[tour + 1]:
                    movement.append([y + i, x + 2*j])

        return movement

    def king(self, x, y, tour, roque):
        movement = []
        R = []
        for i in range(3):
            for j in range(3):
                if y + i - 1 < 8 and  x + j - 1 < 8:
                    if self.chess[y + i - 1, x + j - 1] == "0":
                        movement.append([y + i - 1, x + j - 1])
                    elif self.chess[y + i - 1, x + j - 1][0] in self.enemy[tour + 1]:
                        movement.append([y + i - 1, x + j - 1])

            # roque
            if roque[int(self.chess[y, x][1])] == 2:
                b = True
                for a in self.chess[int(int(self.chess[y, x][1]) * 3.5), 1: int(4 - 0.5*int(self.chess[y, x][1]))]:
                    if a != '0':
                        b = False
                if b:
                    R.append([y, x - 2])

            if roque[int(self.chess[y, x][1])+1] == 2:
                b = True
                for a in self.chess[int(int(self.chess[y, x][1])*3.5), int(5 - 0.5*int(self.chess[y, x][1])): 7]:
                    if a != '0':
                        b = False
                if b:
                    R.append([y, x + 2])
            print(roque)

        return movement, R

    def queen(self, x, y, tour):
        movement = self.bishop(x, y, tour) + self.rook(x, y, tour)
        return movement


game = Game()


def main():
    roque = [2, 2, 2, 2]
    en_passant = -1
    passant = -1, 0

    # who play?
    tour = -1

    # possible movement
    movement = []
    r = []

    # mouse position
    x = y = 0
    select = None

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                x //= 100
                y //= 100
                print(game.pionb, game.pionn)
                if game.chess[y, x][0] in game.enemy[tour * -1 + 1]: # if you clicked on one of your pawn
                    select = y, x
                    choosed = str(game.chess[y, x][0]).lower()

                    if choosed == 'r':
                        movement = game.rook(x, y, tour)

                    elif choosed == 'n':
                        movement = game.knight(x, y, tour)

                    elif choosed == 'b':
                        movement = game.bishop(x, y, tour)

                    elif choosed == 'q':
                        movement = game.queen(x, y, tour)

                    elif choosed == 'k':
                        movement, r = game.king(x, y, tour, roque)

                    elif choosed == 'p':
                        movement, passant = game.pawn(x, y, tour, en_passant)

                elif [y, x] in movement+r or (y == passant[0] and x == passant[1]):
                    # roque
                    if game.chess[select][0].lower == 'r':
                        roque[game.chess[select][1]] = '0'

                    if game.chess[select][0].lower == 'k':
                        if roque[game.chess[select][1]] == '0':
                            roque[0], roque[1] = 0, 0
                        else:
                            roque[2], roque[3] = 0, 0

                    # en passant
                    if str(game.chess[select]).lower() == 'p' and abs(select[0] - y) == 2:
                        en_passant = x
                    else:
                        en_passant = -1

                    # final movement
                    if str(game.chess[select]).lower() == 'p' and (y == 0 or y == 7):
                        if game.chess[select] == 'P':
                            game.chess[select] = 'Q'
                        else:
                            game.chess[select] = 'q'

                    game.chess[y, x] = game.chess[select]
                    game.chess[select] = '0'
                    tour *= -1
                    movement = []
                    if passant[0] > -1:
                        game.chess[passant[0]-tour, passant[1]] = '0'
                        passant = -1, 0

                    # roque
                    if r:
                        if x > 4:
                            game.chess[y, 5-y//7] = game.chess[y, 7]
                            game.chess[y, 7] = '0'
                        else:
                            game.chess[y, 3 - y // 7] = game.chess[y, 0]
                            game.chess[y, 0] = '0'
                        r = []

        # draw board
        chess_board(tour, game.chess, movement, r, passant)

        x, y = pygame.mouse.get_pos()


if __name__ == '__main__':
    main()
