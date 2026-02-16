import pygame
import sys
import random

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skibidi fighter prototype")
clock = pygame.time.Clock()

variables = {
    "Gravity" : 1,
    "Ground _height" : 400,
    "sky color" : (40, 60, 120),
    
}

projectiles = []
particles = []