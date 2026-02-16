import pygame
import math
import sys

# def start_mini_game2():
#     import pygame
#     pygame.init()
#     screen = pygame.display.set_mode((1920, 1080))
#     clock = pygame.time.Clock()
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         dt = clock.tick(60) / 1000  
#         screen.fill((0, 0, 0))
#         font = pygame.font.Font(None, 74)
#         text = font.render("Game to be done", True, (255, 255, 255))
#         screen.blit(text, (760, 500))
#         pygame.display

# Initialisation Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Constantes physiques
g = 9.81 * 50

# Facteur de projection pour simuler profondeur
DEPTH_FACTOR = 0.5

# Chargement images et redimensionnement
BALL_IMG = pygame.image.load("assets/Minigame1.png").convert_alpha()
TRASH_IMG = pygame.image.load("assets/Minigame1.png").convert_alpha()

BALL_IMG = pygame.transform.scale(BALL_IMG, (24, 24))
TRASH_IMG = pygame.transform.scale(TRASH_IMG, (150, 180))

def normalize_angle(angle):
    while angle < -math.pi:
        angle += 2 * math.pi
    while angle >= math.pi:
        angle -= 2 * math.pi
    return angle


class Ball:
    def __init__(self, x, y, z, image):
        self.image = image
        self.start_x = x
        self.start_y = y
        self.start_z = z

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0

        self.is_moving = False

        self.rect = self.image.get_rect(center=(x, y))

    def launch(self, force, angle_h, angle_v):
        self.vx = force * math.cos(angle_v) * math.sin(angle_h)
        self.vz = force * math.cos(angle_v) * math.cos(angle_h)
        self.vy = -force * math.sin(angle_v) 

        self.is_moving = True

    def update(self, dt):
        if self.is_moving:
            self.vy += g * dt

            self.x += self.vx * dt
            self.y += self.vy * dt
            self.z += self.vz * dt

            if self.y > HEIGHT - 50:
                self.is_moving = False
                self.x, self.y, self.z = self.start_x, self.start_y, self.start_z
                self.vx = self.vy = self.vz = 0.0
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.z = self.start_z
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.is_moving = False
        self.rect.center = (int(self.x), int(self.y))


    def draw(self, surface):
        screen_x = int(self.x + self.z * DEPTH_FACTOR)
        screen_y = int(self.y - self.z * DEPTH_FACTOR)

        self.rect = self.image.get_rect(center=(screen_x, screen_y))
        surface.blit(self.image, self.rect)

class Trash:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.top_rect = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.rect.width,
            10
        )
        self.top_rect_right = pygame.Rect(
            self.rect.left,
            self.rect.top,
            self.rect.width,
            10
        )
        self.top_rect_right = pygame.Rect(
            self.rect.right,
            self.rect.top,
            self.rect.width - 10,
            10
        )
        self.bot_rect = pygame.Rect(
            self.rect.left,
            self.rect.bottom ,
            self.rect.width,
            10
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0,100), self.top_rect, 2)  # Dessiner la zone haute en rouge

ball = Ball(100, HEIGHT - 80, 0, BALL_IMG)

# Position des poubelles 
trash_list = [
    Trash(150, HEIGHT - 300, TRASH_IMG),
    Trash(350, HEIGHT - 300, TRASH_IMG),
    Trash(550, HEIGHT - 300, TRASH_IMG),
]

charging = False
force = 0.0
max_force = 1000.0
charge_rate = 500.0  # unité de force par seconde

running = True
while running:
    dt = clock.tick(60) / 1000 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball.is_moving:
                charging = True
                force = 0.0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and charging:
                charging = False

                # Récupération position souris
                mx, my = pygame.mouse.get_pos()

                # Calcul des angles pour lancer
                dx = mx - ball.x
                dy = ball.y - my  

                distance_camera_ball = 500  

                angle_h = math.atan2(dx, distance_camera_ball)
                angle_h = normalize_angle(angle_h)
                angle_v = math.atan2(dy, distance_camera_ball)
                angle_v = normalize_angle(angle_v)

                ball.launch(force, angle_h, angle_v)

    if charging:
        force += charge_rate * dt
        if force > max_force:
            force = max_force


    # Affichage
    screen.fill((100, 100, 100))

    for trash in trash_list:
        trash.draw(screen)
        if ball.rect.colliderect(trash.top_rect):
            print("La balle touche une poubelle !")
            ball.reset()
    ball.update(dt)
    ball.draw(screen)

    # Affichage barre de charge
    if charging:
        bar_width = int(500 * (force / max_force))
        pygame.draw.rect(screen, (0, 255, 0), (50, 550, bar_width, 20))
        pygame.draw.rect(screen, (255, 255, 255), (50, 550, 500, 20), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()