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
