#!/usr/bin/python3

# Copyright (c) 2017, 2020 Samuel Thibault <samuel.thibault@ens-lyon.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY Samuel Thibault ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import sys
import pygame
import socket
import time
import os
import time
import threading
from pygame import mixer

##############
############################################
HOST = "localhost"
PORT = 9004
connexion = None
ball_envoie = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
print("Le serveur est mise en route")

while connexion == None:
    connexion, adresse = s.accept()
    print("Une personne est connecter avec pour ip {0} et pour port {1}".format(adresse[0],adresse[1]))
###########################################
###############################################################

# Screen setup

width = 800
height = 600


new_value = 0

ball_speed = [ -2, -2 ]
racket_speed_gauche = [0, 0]

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode( (width, height) )

# Load resources

background = pygame.image.load("ressources/image/background.png")

ball = pygame.image.load("ressources/image/ball.png")
ball_coords = ball.get_rect()

racket_gauche = pygame.image.load("ressources/image/racket.png")
racket_coords_gauche = racket_gauche.get_rect()

racket_droite = pygame.image.load("ressources/image/racket.png")
racket_coords_droite = racket_droite.get_rect()

#background sound
pygame.mixer.music.load('ressources/musique.wav')
pygame.mixer.music.play()

#GameOver
gameover = pygame.image.load("ressources/image/Gameover.jpg")
gameover = pygame.transform.scale(gameover,(800,600))

#Win
win = pygame.image.load("ressources/image/win.jpg")
win = pygame.transform.scale(win,(800,600))

#score
score_value_rackette_gauche = 0
score_value_rackette_droite = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 300
textY = 30

def show_score(x,y):
    score = font.render("Score : " + str(score_value_rackette_droite) + " / "  +str(score_value_rackette_gauche),True,(255,255,255))
    screen.blit(score,(x,y))


# Throw ball from center
def throw():
    ball_coords.left = 531
    ball_coords.top = 298

throw()

while True:
    for e in pygame.event.get():
        # Check for exit
        if e.type == pygame.QUIT:
            sys.exit()
    
        # Check for racket movements
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                racket_speed_gauche[1] = -4
                pass
            elif e.key == pygame.K_DOWN:
                racket_speed_gauche[1] = 4
                pass

        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_UP:
                racket_speed_gauche[1] = 0
                pass
            elif e.key == pygame.K_DOWN:
                racket_speed_gauche[1] = 0
                pass

    # Move ball
    ball_coords = ball_coords.move(ball_speed)

    # Bounce ball on walls
    if ball_coords.left < 0 or ball_coords.right >= width:
        ball_speed[0] = -ball_speed[0]
    if ball_coords.top < 0 or ball_coords.bottom >= height:
        ball_speed[1] = -ball_speed[1]

    # Move racket
    racket_coords_gauche = racket_coords_gauche.move(racket_speed_gauche)


    # Racket reached racket position?
    if ball_coords.left <= 0:
        if ball_coords.bottom <= racket_coords_gauche.top or ball_coords.top >= racket_coords_gauche.bottom:
            score_value_rackette_gauche = score_value_rackette_gauche + 1
            # print(score_value_rackette_gauche)
            print("lost Joueur gauche")
            throw()



    # Racket reached racket position?
    if ball_coords.left >= 780:
        if ball_coords.bottom <= racket_coords_droite.top or ball_coords.top >= racket_coords_droite.bottom:
            score_value_rackette_droite = score_value_rackette_droite + 1
            # print(score_value_rackette_droite)
            print("lost Joueur droite!")
            throw()

        # Clip racket on court
    if racket_coords_droite.left == width:
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

    pygame.display.flip()

    # Win
    if score_value_rackette_droite == 3:
        score_value_rackette_gauche = 0
        score_value_rackette_droite = 0
        screen.blit(win, (0, 0))
        pygame.display.flip()
        time.sleep(1)
        pygame.time.delay(5000)

    # Game over
    elif score_value_rackette_gauche == 3:
        score_value_rackette_gauche = 0
        score_value_rackette_droite = 0
        screen.blit(gameover, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5000)

    else:
        # affichage
        screen.fill([255, 255, 255])
        screen.blit(background, (0, 0))
        screen.blit(ball, ball_coords)
        screen.blit(racket_gauche, racket_coords_gauche)
        show_score(textX, textY)

    ##########################################
    ##############
    #Envoie de données

    ballx = ball_coords.x
    bally = ball_coords.y

    ball_envoie = "ball" + ":" + str(ballx) + ":" + str(bally) + ":"
    connexion.send(ball_envoie.encode('utf-8'))

    #############
    ##########################################

    # reception rackette droite
    recu = connexion.recv(1024).decode('utf-8')
    spliter = recu.split(":")
    # print(spliter)
    toutslesmot = spliter
    premierMot = toutslesmot[0]

    if premierMot == "coordonéeRocketdroite":
        raquettex = int(toutslesmot[1])
        raquettey = int(toutslesmot[2])

        # print(raquettex)
        # print(raquettey)

        racket_coords_droite.x = 760
        racket_coords_droite.y = raquettey
        # print(racket_coords_droite)
        screen.blit(racket_droite, racket_coords_droite)


    racketx = racket_coords_gauche.x
    rackety = racket_coords_gauche.y
    a = "coordonéeRocketgauche" + ":" + str(racketx) + ":" + str(rackety) + ":"
    connexion.send(a.encode('utf-8'))


    # sleep 10ms, since there is no need for more than 100Hz refresh :)
    pygame.time.delay(10)




