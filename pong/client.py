import sys
import pygame
import socket
from pygame import mixer
import threading


###############################################
# Initialisation du serveur
# Mise en place du socket avec les protocoles IPv4 et TCP

HOST = "localhost"
PORT = 9004

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#################################################
# Taille ecran
width = 800
height = 600

# vitesse ball
ball_speed = [ -2, -2 ]

# vitesse racket
racket_speed_droite = [0, 0]
racket_speed_gauche = [0, 0]
x2 = 0
la_balle = 0


# Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode( (width, height) )


# chargement ressources

background = pygame.image.load("ressources/image/background.png")

ball_load = pygame.image.load("ressources/image/ball.png")
ball_coords = ball_load.get_rect()


racket_droite = pygame.image.load("ressources/image/racket.png")
racket_coords_droite = racket_droite.get_rect()

racket_gauche = pygame.image.load("ressources/image/racket.png")
racket_coords_gauche = racket_gauche.get_rect()

pygame.mixer.music.load('ressources/musique.wav')
pygame.mixer.music.play()

#GameOver
gameover = pygame.image.load("ressources/image/Gameover.jpg")
gameover = pygame.transform.scale(gameover,(800,600))

#Win
win = pygame.image.load("ressources/image/win.jpg")
win = pygame.transform.scale(win,(800,600))

# score
score_gauche=0
score_droite=0
font = pygame.font.Font('freesansbold.ttf',32)



#score - initialisation, position et police
score_droite = 0
score_gauche = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 300
textY = 30
def show_score(x,y):
    score = font.render("Score : " + str(score_droite) + " / "  + str(score_gauche),True,(255,255,255))
    screen.blit(score,(x,y))

# Lance la balle
def throw():
    ball_coords.left = 531
    ball_coords.top = 298

throw()

# Le joueur à perdu
def ball_lost():
    if ball_coords.left <= 0:
        if ball_coords.bottom <= racket_coords_gauche.top or ball_coords.top >= racket_coords_gauche.bottom:
            print("lost!")
            throw()

# Boucle Principale
while True:
    for e in pygame.event.get():
        # Check for exit
        if e.type == pygame.QUIT:
            sys.exit()
        # touches joueur
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                racket_speed_droite[1] = -4
                pass
            elif e.key == pygame.K_RIGHT:
                racket_speed_droite[1] = 4
                pass

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                racket_speed_droite[1] = 0
                pass
            elif e.key == pygame.K_RIGHT:
                racket_speed_droite[1] = 0
                pass


    # rebonds balles sur les murs
    if ball_coords.left < 0 or ball_coords.right >= width:
        ball_speed[0] = -ball_speed[0]
    if ball_coords.top < 0 or ball_coords.bottom >= height:
        ball_speed[1] = -ball_speed[1]

    # Mouvements raquettes racket
    racket_coords_droite = racket_coords_droite.move(racket_speed_droite)
    racket_coords_gauche = racket_coords_gauche.move(racket_speed_gauche)

    # Racket reached racket position?
    if ball_coords.left <= 0:
        if ball_coords.bottom <= racket_coords_gauche.top or ball_coords.top >= racket_coords_gauche.bottom:
            score_gauche = score_gauche + 1
            # print(score_value_rackette_gauche)
            print("lost Joueur gauche")

    # Racket reached racket position?
    if ball_coords.left >= 780:
        if ball_coords.bottom <= racket_coords_droite.top or ball_coords.top >= racket_coords_droite.bottom:
            score_droite = score_droite + 1
            # print(score_value_rackette_droite)
            print(score_droite)

        # accrochage raquettes sur l'ecran
    if racket_coords_droite.left < 0:
        racket_coords_droite.left = 0
    elif racket_coords_droite.right >= width:
        racket_coords_droite.right = width - 1
    if racket_coords_droite.top < 0:
        racket_coords_droite.top = 0
    elif racket_coords_droite.bottom >= height:
        racket_coords_droite.bottom = height - 1

    if racket_coords_gauche.left < 0:
        racket_coords_gauche.left = 0
    elif racket_coords_gauche.right >= width:
        racket_coords_gauche.right = width - 1
    if racket_coords_gauche.top < 0:
        racket_coords_gauche.top = 0
    elif racket_coords_gauche.bottom >= height:
        racket_coords_gauche.bottom = height - 1

        # Win
    if score_gauche == 3:
        score_gauche = 0
        score_droite = 0
        screen.blit(win, (0, 0))
        pygame.display.flip()


        # Game over
    elif score_droite == 3:
        score_droite = 0
        score_gauche = 0
        screen.blit(gameover, (0, 0))
        pygame.display.flip()


    else:

        # affichage
        screen.fill([255, 255, 255])
        screen.blit(background, (0, 0))
        screen.blit(ball_load, ball_coords)
        screen.blit(racket_droite, racket_coords_droite)
        show_score(textX, textY)

    #########################################################
    #########################################################
    for i in range(3):
        recu = s.recv(1024).decode('utf-8')
        spliter =recu.split(":")
        # print(spliter)
        toutslesmot = spliter
        premierMot = toutslesmot[0]

        #########################################################
        #########################################################
        # reception ball
        if premierMot == "ball":
            x = int(toutslesmot[1])
            y = int(toutslesmot[2])

            if ball_coords.x <= 400:
                ball_coords.x = x-4
            else:
                ball_coords.x = x+4
            ball_coords.y = y
            screen.blit(ball_load, ball_coords)
