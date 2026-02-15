import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighter")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
YELLOW = (255, 255, 0)

GROUND_Y = HEIGHT - 80
GRAVITY = 0.9

font = pygame.font.SysFont(None, 48)


class Fighter:
    def __init__(self, x, color, controls):
        self.rect = pygame.Rect(x, GROUND_Y - 120, 60, 120)
        self.color = color
        self.controls = controls
        self.vel_y = 0
        self.speed = 6
        self.jump_force = -18
        self.health = 100
        self.facing = 1
        self.attack_type = None
        self.attack_timer = 0
        self.hit_timer = 0

    def move(self, keys, opponent):
        dx = 0

        if self.hit_timer == 0:
            if keys[self.controls["left"]]:
                dx = -self.speed
                self.facing = -1
            if keys[self.controls["right"]]:
                dx = self.speed
                self.facing = 1
            if keys[self.controls["jump"]] and self.rect.bottom >= GROUND_Y:
                self.vel_y = self.jump_force

        self.rect.x += dx

        if self.rect.colliderect(opponent.rect):
            if dx > 0:
                self.rect.right = opponent.rect.left
            if dx < 0:
                self.rect.left = opponent.rect.right

        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0

        if self.attack_timer > 0:
            self.attack_timer -= 1
        else:
            self.attack_type = None

        if self.hit_timer > 0:
            self.hit_timer -= 1

    def attack(self, opponent, attack_type):
        if self.attack_timer == 0 and self.hit_timer == 0:
            self.attack_type = attack_type
            self.attack_timer = 20

            if attack_type == "punch":
                damage = 10
                width = 50
                height = 30
                y_offset = 30
            else:
                damage = 15
                width = 60
                height = 40
                y_offset = 60

            attack_rect = pygame.Rect(
                self.rect.centerx + (self.facing * 40),
                self.rect.y + y_offset,
                width,
                height
            )

            if attack_rect.colliderect(opponent.rect):
                opponent.health -= damage
                opponent.hit_timer = 15
                opponent.rect.x += self.facing * 20

    def draw(self):
        color = (255, 255, 255) if self.hit_timer > 0 else self.color
        pygame.draw.rect(screen, color, self.rect)

        if self.attack_type:
            if self.attack_type == "punch":
                width, height, y_offset = 50, 30, 30
            else:
                width, height, y_offset = 60, 40, 60

            attack_rect = pygame.Rect(
                self.rect.centerx + (self.facing * 40),
                self.rect.y + y_offset,
                width,
                height
            )
            pygame.draw.rect(screen, YELLOW, attack_rect)


def draw_health(x, y, health):
    pygame.draw.rect(screen, RED, (x, y, 300, 25))
    pygame.draw.rect(screen, GREEN, (x, y, 3 * health, 25))
    pygame.draw.rect(screen, BLACK, (x, y, 300, 25), 3)


p1_controls = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "jump": pygame.K_w,
    "punch": pygame.K_f,
    "kick": pygame.K_g
}

p2_controls = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "jump": pygame.K_UP,
    "punch": pygame.K_RCTRL,
    "kick": pygame.K_RSHIFT
}

player1 = Fighter(200, RED, p1_controls)
player2 = Fighter(700, BLUE, p2_controls)

game_over = False
winner_text = ""

running = True
while running:
    clock.tick(60)
    screen.fill(GRAY)
    pygame.draw.rect(screen, (60, 160, 60), (0, GROUND_Y, WIDTH, 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        player1.move(keys, player2)
        player2.move(keys, player1)

        if keys[p1_controls["punch"]]:
            player1.attack(player2, "punch")
        if keys[p1_controls["kick"]]:
            player1.attack(player2, "kick")

        if keys[p2_controls["punch"]]:
            player2.attack(player1, "punch")
        if keys[p2_controls["kick"]]:
            player2.attack(player1, "kick")

        player1.update()
        player2.update()

        if player1.health <= 0:
            winner_text = "BLUE WINS"
            game_over = True
        if player2.health <= 0:
            winner_text = "RED WINS"
            game_over = True
    else:
        text = font.render(winner_text, True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        restart = font.render("Press R", True, WHITE)
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 50))

        if keys[pygame.K_r]:
            player1 = Fighter(200, RED, p1_controls)
            player2 = Fighter(700, BLUE, p2_controls)
            game_over = False

    player1.draw()
    player2.draw()

    draw_health(50, 30, player1.health)
    draw_health(WIDTH - 350, 30, player2.health)

    pygame.display.flip()

pygame.quit()
sys.exit()
