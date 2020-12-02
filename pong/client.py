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

