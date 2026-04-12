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

# Constants
g = 9.81 * 50
DEPTH_FACTOR = 0.5

BALL_IMG_PLASTIC = pygame.image.load("assets/ball_plastic.png").convert_alpha()
BALL_IMG_PAPER = pygame.image.load("assets/ball_paper.png").convert_alpha()
BALL_IMG_GLASS = pygame.image.load("assets/ball_glass.png").convert_alpha()

TRASH_IMG_PAPER = pygame.image.load("assets/Minigame1_PAPER.png").convert_alpha()
TRASH_IMG_PLASTIC = pygame.image.load("assets/Minigame1_PLASTIC.png").convert_alpha()
TRASH_IMG_GLASS = pygame.image.load("assets/Minigame1_GLASS.png").convert_alpha()

BALL_IMG_PLASTIC = pygame.transform.scale(BALL_IMG_PLASTIC, (35, 35))
BALL_IMG_PAPER = pygame.transform.scale(BALL_IMG_PAPER, (35, 35))
BALL_IMG_GLASS = pygame.transform.scale(BALL_IMG_GLASS, (35, 35))

TRASH_IMG_PAPER = pygame.transform.scale(TRASH_IMG_PAPER, (120, 140))
TRASH_IMG_PLASTIC = pygame.transform.scale(TRASH_IMG_PLASTIC, (120, 140))
TRASH_IMG_GLASS = pygame.transform.scale(TRASH_IMG_GLASS, (120, 140))

particles = []
score = 0
TARGET_SCORE = 200

game_over = False
victory = False

TRASH_TYPES = ["plastic", "paper", "glass"]

BALL_IMAGES = {
    "plastic": BALL_IMG_PLASTIC,
    "paper": BALL_IMG_PAPER,
    "glass": BALL_IMG_GLASS
}

class TrashBin:
    def __init__(self, x, y, image, accepted_type):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.radius = self.rect.width // 2 - 10
        self.accepted_type = accepted_type
        self.capacity = 3
        self.current_fill = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        font = pygame.font.SysFont(None, 40)
        text = font.render(f"{self.current_fill}/{self.capacity}", True, (255,255,255))
        screen.blit(text, (self.rect.x, self.rect.y - 40))

    def is_full(self):
        return self.current_fill >= self.capacity

    def add_trash(self, trash_type):
        if not self.is_full() and trash_type == self.accepted_type:
            self.current_fill += 1
            return True
        return False

class Ball:
    def __init__(self, x, y, z, bins):
        self.start_x = x
        self.start_y = y
        self.start_z = z
        self.bins = bins
        self.reset()

    def launch(self, force, angle_h, angle_v):
        self.vx = force * math.cos(angle_v) * math.cos(angle_h)
        self.vz = force * math.cos(angle_v) * math.sin(angle_h)
        self.vy = -force * math.sin(angle_v)
        self.is_moving = True

    def update(self, dt):
        if not self.is_moving:
            return

        self.vy += g * dt

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        sx = int(self.x + self.z * DEPTH_FACTOR)
        sy = int(self.y - self.z * DEPTH_FACTOR)
        self.rect.center = (sx, sy)

        if sx < -50 or sx > WIDTH + 50 or sy > HEIGHT + 50 or sy < -50:
            self.reset()

    def reset(self):
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        self.z = float(self.start_z)
        self.vx = self.vy = self.vz = 0.0
        self.is_moving = False

        available = [t for t in TRASH_TYPES if not any(b.accepted_type == t and b.is_full() for b in self.bins)]
        if available:
            self.trash_type = random.choice(available)
        else:
            self.trash_type = random.choice(TRASH_TYPES)

        self.image = BALL_IMAGES[self.trash_type]
        self.radius = self.image.get_width() // 2
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# collision
def circle_collision(x1, y1, r1, x2, y2, r2):
    return math.hypot(x1 - x2, y1 - y2) <= (r1 + r2)

bins = [
    TrashBin(WIDTH - 200, HEIGHT - 200, TRASH_IMG_PLASTIC, "plastic"),
    TrashBin(WIDTH - 350, HEIGHT - 200, TRASH_IMG_PAPER, "paper"),
    TrashBin(WIDTH - 500, HEIGHT - 200, TRASH_IMG_GLASS, "glass")
]

ball = Ball(100, HEIGHT - 80, 0, bins)

charging = False
force = 0.0
max_force = 1000.0
charge_rate = 500.0

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball.is_moving and not game_over:
                charging = True
                force = 0.0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and charging:
                charging = False

                mx, my = pygame.mouse.get_pos()
                dx = mx - ball.rect.centerx
                dy = ball.rect.centery - my

                angle_h = math.atan2(dy, dx)
                angle_v = math.atan2(dy, 500)

                ball.launch(force, angle_h, angle_v)

    if charging:
        force = min(force + charge_rate * dt, max_force)

    screen.fill((30, 30, 50))

    # trajectory
    if charging and not game_over:
        mx, my = pygame.mouse.get_pos()
        dx = mx - ball.rect.centerx
        dy = ball.rect.centery - my

        angle_h = math.atan2(dy, dx)
        angle_v = math.atan2(dy, 500)

        vx = force * math.cos(angle_v) * math.cos(angle_h)
        vz = force * math.cos(angle_v) * math.sin(angle_h)
        vy = -force * math.sin(angle_v)

        for i in range(25):
            t = i * 0.1
            xt = ball.x + vx * t
            yt = ball.y + vy * t + 0.5 * g * t * t
            zt = ball.z + vz * t

            sx = int(xt + zt * DEPTH_FACTOR)
            sy = int(yt - zt * DEPTH_FACTOR)

            pygame.draw.circle(screen, (255,255,255), (sx, sy), 3)

    for b in bins:
        b.draw(screen)

    if not game_over:
        ball.update(dt)
    ball.draw(screen)

    if ball.is_moving and not game_over:
        for b in bins:
            if circle_collision(ball.rect.centerx, ball.rect.centery, ball.radius,
                                b.rect.centerx, b.rect.centery, b.radius):

                if b.add_trash(ball.trash_type):
                    score += 35
                else:
                    if score > 0: 
                        score -= 10

                ball.reset()
                break

    # end condition
    if all(b.is_full() for b in bins):
        game_over = True
        victory = score >= TARGET_SCORE

    # charge bar
    if charging:
        ratio = max(0, min(1, force / max_force))
        r = int(255 * ratio)
        g_col = int(255 * (1 - ratio))
        color = (r, g_col, 0)

        pygame.draw.rect(screen, color, (50, HEIGHT - 120, int(500 * ratio), 30))
        pygame.draw.rect(screen, (255,255,255), (50, HEIGHT - 120, 500, 30), 3)

    font = pygame.font.SysFont(None, 40)
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (50,50))
    screen.blit(font.render(f"Trash: {ball.trash_type}", True, (255,255,255)), (50,100))

    if game_over:
        big_font = pygame.font.SysFont(None, 100)
        if victory:
            text = big_font.render("YOU WIN", True, (0,255,0))
        else:
            text = big_font.render("YOU LOSE", True, (255,0,0))
        screen.blit(text, (WIDTH//2 - 250, HEIGHT//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
