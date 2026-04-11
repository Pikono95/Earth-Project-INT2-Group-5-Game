import time
import pygame
import math
import sys
import random

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Constantes
g = 9.81 * 50
DEPTH_FACTOR = 0.5

BALL_IMG = pygame.image.load("assets/Minigame1.png").convert_alpha()
TRASH_IMG = pygame.image.load("assets/Minigame1.png").convert_alpha()

BALL_IMG = pygame.transform.scale(BALL_IMG, (35, 35))
TRASH_IMG = pygame.transform.scale(TRASH_IMG, (180, 210))

particles = []

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

        self.trail = []

    def launch(self, force, angle_h, angle_v):
        self.vx = force * math.cos(angle_v) * math.sin(angle_h)
        self.vz = force * math.cos(angle_v) * math.cos(angle_h)
        self.vy = -force * math.sin(angle_v)
        self.is_moving = True

    def update(self, dt):
        if not self.is_moving:
            return

        self.vy += g * dt

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        screen_x = int(self.x + self.z * DEPTH_FACTOR)
        screen_y = int(self.y - self.z * DEPTH_FACTOR)
        self.rect.center = (screen_x, screen_y)

        self.trail.append((self.rect.center, 255))
        if len(self.trail) > 10:
            self.trail.pop(0)

        if self.rect.bottom >= HEIGHT or self.rect.top <= 0 or self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.reset()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.z = self.start_z
        self.vx = self.vy = self.vz = 0
        self.is_moving = False
        self.trail.clear()

    def draw(self, surface):
        for i, (pos, alpha) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            surf = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 0, alpha), (5, 5), 5)
            surface.blit(surf, pos)

        surface.blit(self.image, self.rect)

class Trash:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(bottomleft=(x, y))

    def draw(self, screen):
        # bounce réduit (divisé par ~3)
        offset = math.sin(time.time() * 2) * 2

        draw_x = self.x
        draw_y = self.y + offset

        # synchronisation collision
        self.rect.topleft = (draw_x, draw_y - self.image.get_height())

        screen.blit(self.image, (draw_x, draw_y))

ball = Ball(100, HEIGHT - 80, 0, BALL_IMG)

trash_list = [
    Trash(WIDTH - 200, HEIGHT - 50, TRASH_IMG),
    Trash(WIDTH - 350, HEIGHT - 200, TRASH_IMG),
    Trash(WIDTH - 500, HEIGHT - 350, TRASH_IMG)
]

charging = False
force = 0.0
max_force = 1000.0
charge_rate = 500.0


def predict_trajectory(ball, force, angle_h, angle_v):
    points = []

    vx = force * math.cos(angle_v) * math.sin(angle_h)
    vz = force * math.cos(angle_v) * math.cos(angle_h)
    vy = -force * math.sin(angle_v)

    x, y, z = ball.x, ball.y, ball.z

    for i in range(30):
        t = i * 0.1

        x_temp = x + vx * t
        y_temp = y + vy * t + 0.5 * g * t * t
        z_temp = z + vz * t

        screen_x = int(x_temp + z_temp * DEPTH_FACTOR)
        screen_y = int(y_temp - z_temp * DEPTH_FACTOR)

        points.append((screen_x, screen_y))

    return points

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

                mx, my = pygame.mouse.get_pos()

                dx = mx - ball.x
                dy = ball.y - my

                angle_h = math.atan2(dx, 500)
                angle_v = math.atan2(dy, 500)

                ball.launch(force, angle_h, angle_v)

    if charging:
        force += charge_rate * dt
        if force > max_force:
            force = max_force

    # fond dégradé corrigé
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(135 * (1 - ratio) + 50 * ratio)
        g_col = int(206 * (1 - ratio) + 50 * ratio)
        b = int(235 * (1 - ratio) + 100 * ratio)
        pygame.draw.line(screen, (r, g_col, b), (0, y), (WIDTH, y))

    if charging:
        mx, my = pygame.mouse.get_pos()
        dx = mx - ball.x
        dy = ball.y - my

        angle_h = math.atan2(dx, 500)
        angle_v = math.atan2(dy, 500)

        points = predict_trajectory(ball, force, angle_h, angle_v)

        for i, point in enumerate(points):
            alpha = int(255 * (1 - i / len(points)))
            surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 255, alpha), (4, 4), 4)
            screen.blit(surf, point)

    for trash in trash_list:
        trash.draw(screen)

    ball.update(dt)
    ball.draw(screen)

    for p in particles[:]:
        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt
        p["vy"] += 300 * dt
        p["life"] -= dt

        surf = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 255, 0, int(255 * p["life"])), (3, 3), 3)
        screen.blit(surf, (p["x"], p["y"]))

        if p["life"] <= 0:
            particles.remove(p)

    if charging:
        ratio = force / max_force
        color = (int(255 * ratio), 255 - int(255 * ratio), 0)
        pygame.draw.rect(screen, color, (50, 550, int(500 * ratio), 20))
        pygame.draw.rect(screen, (255, 255, 255), (50, 550, 500, 20), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()