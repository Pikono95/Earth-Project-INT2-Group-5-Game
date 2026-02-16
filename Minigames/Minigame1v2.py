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
        
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 3)

class Player: 

    def __init__(self,person,x,y,vx,vy,facing):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.facing = facing
        self.person = person
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.jumpingpower = -20
        if self.y < variables["Ground _height"]:
            self.jumping = True
            self.vy += variables["Gravity"]
        elif self.y > variables["Ground _height"]:
            self.y = variables["Ground _height"]
            self.vy = 0
            self.jumping = False
        else:
            self.vy = 0
            self.jumping = False
        self.vx *= 0.84
        if self.vx < 1 and self.vx > -1:
            self.vx = 0
        print(self.jumping)
        
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - 30:
            self.x = WIDTH - 30
        if pygame.key.get_pressed()[keys["crouch"]]:
            self.crouching = 25
            if self.jumping == True:
                self.vy = 40
            else:
                self.jumpingpower = -40
                self.jumping = False
        else:
            self.crouching = 0


        

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y - 50 + self.crouching, 30, 50 - self.crouching))

    def move(self):
        speed = 8
        if pygame.key.get_pressed()[keys["crouch"]]:
            speed = 4
        if pygame.key.get_pressed()[keys["jump"]] and pygame.key.get_pressed()[keys["crouch"]]:
            self.jumping = False
        if pygame.key.get_pressed()[keys["left"]]:
            self.vx = -speed
            self.facing = "left"
        if pygame.key.get_pressed()[keys["right"]]:
            self.vx = speed
            self.facing = "right"
        if pygame.key.get_pressed()[keys["left"]] and pygame.key.get_pressed()[keys["right"]]:
            self.vx = 0
        if pygame.key.get_pressed()[keys["jump"]] and self.jumping == False:
            if self.vy == 0:
                self.vy = self.jumpingpower
        

#keys

keys = {
    "left" : pygame.K_q,
    "right" : pygame.K_d,
    "jump" : pygame.K_z,
    "crouch" : pygame.K_s,
    "shoot" : pygame.K_f,
    "punch" : pygame.K_r,
    "kick" : pygame.K_e,
}

player1 = Player("player1",100, variables["Ground _height"], 0, 0, "right")

#game loop

run = True
while run:
    clock.tick(60)
    screen.fill(variables["sky color"])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        run = False
    
    player1.update()
    player1.draw()
    player1.move()

    pygame.display.flip()

pygame.quit()
sys.exit()