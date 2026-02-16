import pygame
import sys
import random

pygame.init()

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

class Projectile:
    def __init__(self,x,y,vx,vy,direction):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.direction = direction
    
    def update(self):
        self.x += self.vx * self.direction
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 5)

#particule system
particles = []
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 0)
        self.life = 20

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 3)

class Player: 

    def __init___(self,x,y,vx,vy,facing,person):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.facing = facing
        self.person = person
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += variables["Gravity"]

        if self.y > variables["Ground _height"]:
            self.y = variables["Ground _height"]
            self.vy = 0

#keys

keys = {
    "left" : pygame.K_a,
    "right" : pygame.K_d,
    "jump" : pygame.K_w,
    "shoot" : pygame.K_f
    "punch" : pygame.K_r
    "kick" : pygame.K_e
}

#game loop

run = True
while run:
    clock.tick(24)
    screen.fill(variables["sky color"])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        run = False

    pygame.display.flip()

pygame.quit()
sys.exit()