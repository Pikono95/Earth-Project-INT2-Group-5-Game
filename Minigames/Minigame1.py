import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skibidi fighter prototype")
clock = pygame.time.Clock()

GROUND_Y = HEIGHT - 80
GRAVITY = 0.9

font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 36)

projectiles = []
particles = []

sky_color = (40, 60, 120)
sun_pos = (800, 100)
buildings = []
for i in range(0, WIDTH, 80):
    h = random.randint(80, 180)
    buildings.append((i, h))


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


class Projectile:
    def __init__(self, x, y, direction, color, damage, speed):
        self.rect = pygame.Rect(x, y, 20, 10)
        self.direction = direction
        self.color = color
        self.damage = damage
        self.speed = speed
        self.active = True

    def update(self, opponent):
        self.rect.x += self.direction * self.speed
        if self.rect.colliderect(opponent.rect):
            opponent.health -= self.damage
            opponent.health = max(0, opponent.health)
            opponent.hit_timer = 10
            opponent.rect.x += self.direction * 20
            for _ in range(6):
                particles.append(Particle(opponent.rect.centerx, opponent.rect.centery))
            self.active = False
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.active = False

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


class Fighter:
    def __init__(self, x, color, controls, name):
        self.rect = pygame.Rect(x, GROUND_Y - 140, 70, 140)
        self.color = color
        self.controls = controls
        self.vel_y = 0
        self.speed = 6
        self.jump_force = -18
        self.health = 200
        self.facing = 1
        self.attack_timer = 0
        self.hit_timer = 0
        self.special_timer = 0
        self.name = name

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
        if self.hit_timer > 0:
            self.hit_timer -= 1
        if self.special_timer > 0:
            self.special_timer -= 1

    def melee(self, opponent, damage, reach, height):
        if self.attack_timer == 0:
            self.attack_timer = 20
            if self.facing == 1:
                hitbox = pygame.Rect(self.rect.right, self.rect.y + height, reach, 30)
            else:
                hitbox = pygame.Rect(self.rect.left - reach, self.rect.y + height, reach, 30)

            if hitbox.colliderect(opponent.rect):
                opponent.health -= damage
                opponent.health = max(0, opponent.health)
                opponent.hit_timer = 10
                opponent.rect.x += self.facing * 25
                for _ in range(6):
                    particles.append(Particle(opponent.rect.centerx, opponent.rect.centery))

    def shoot(self):
        if self.attack_timer == 0:
            self.attack_timer = 30
            x = self.rect.right if self.facing == 1 else self.rect.left - 20
            y = self.rect.centery
            projectiles.append(Projectile(x, y, self.facing, (0, 255, 255), 8, 10))

    def special(self, opponent):
        if self.special_timer == 0:
            self.special_timer = 120
            if self.name == "red":
                self.rect.x += self.facing * 120
                if self.rect.colliderect(opponent.rect):
                    opponent.health -= 25
                    opponent.health = max(0, opponent.health)
                    opponent.hit_timer = 15
            else:
                x = self.rect.right if self.facing == 1 else self.rect.left - 60
                y = self.rect.centery - 20
                projectiles.append(Projectile(x, y, self.facing, (0, 255, 0), 20, 15))

    def draw(self):
        c = (255, 255, 255) if self.hit_timer > 0 else self.color
        pygame.draw.circle(screen, c, (self.rect.centerx, self.rect.y + 20), 20)
        pygame.draw.rect(screen, c, (self.rect.x + 15, self.rect.y + 40, 40, 60))
        pygame.draw.rect(screen, c, (self.rect.x + 10, self.rect.y + 100, 20, 40))
        pygame.draw.rect(screen, c, (self.rect.x + 40, self.rect.y + 100, 20, 40))


def draw_health(x, y, health):
    pygame.draw.rect(screen, (200, 50, 50), (x, y, 300, 25))
    pygame.draw.rect(screen, (50, 200, 50), (x, y, 3 * health, 25))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 300, 25), 3)


def draw_background():
    screen.fill(sky_color)
    pygame.draw.circle(screen, (255, 200, 0), sun_pos, 50)
    for b in buildings:
        pygame.draw.rect(screen, (25, 25, 45), (b[0], GROUND_Y - b[1], 60, b[1]))


p1_controls = {
    "left": pygame.K_q,
    "right": pygame.K_d,
    "jump": pygame.K_z,
    "punch": pygame.K_f,
    "kick": pygame.K_g,
    "shoot": pygame.K_h,
    "special": pygame.K_j
}

p2_controls = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "jump": pygame.K_UP,
    "punch": pygame.K_KP1,
    "kick": pygame.K_KP2,
    "shoot": pygame.K_KP4,
    "special": pygame.K_KP5
}

player1 = Fighter(200, (220, 60, 60), p1_controls, "red")
player2 = Fighter(700, (60, 60, 220), p2_controls, "blue")

game_over = False
winner = ""

running = True
while running:
    clock.tick(60)
    draw_background()
    pygame.draw.rect(screen, (60, 160, 60), (0, GROUND_Y, WIDTH, 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        player1.move(keys, player2)
        player2.move(keys, player1)

        if keys[p1_controls["punch"]]:
            player1.melee(player2, 10, 50, 40)
        if keys[p1_controls["kick"]]:
            player1.melee(player2, 15, 60, 80)
        if keys[p1_controls["shoot"]]:
            player1.shoot()
        if keys[p1_controls["special"]]:
            player1.special(player2)

        if keys[p2_controls["punch"]]:
            player2.melee(player1, 10, 50, 40)
        if keys[p2_controls["kick"]]:
            player2.melee(player1, 15, 60, 80)
        if keys[p2_controls["shoot"]]:
            player2.shoot()
        if keys[p2_controls["special"]]:
            player2.special(player1)

        player1.update()
        player2.update()

        for p in projectiles[:]:
            target = player2 if p.direction == 1 else player1
            p.update(target)
            if not p.active:
                projectiles.remove(p)

        for particle in particles[:]:
            particle.update()
            if particle.life <= 0:
                particles.remove(particle)

        if player1.health <= 0:
            winner = "BLUE WINS"
            game_over = True
        elif player2.health <= 0:
            winner = "RED WINS"
            game_over = True

    else:
        text = font.render(winner, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 40))
        restart = small_font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 20))
        if keys[pygame.K_r]:
            player1 = Fighter(200, (220, 60, 60), p1_controls, "red")
            player2 = Fighter(700, (60, 60, 220), p2_controls, "blue")
            projectiles.clear()
            particles.clear()
            game_over = False

    player1.draw()
    player2.draw()

    for p in projectiles:
        p.draw()

    for particle in particles:
        particle.draw()

    draw_health(50, 30, player1.health)
    draw_health(WIDTH - 350, 30, player2.health)

    pygame.display.flip()

pygame.quit()
sys.exit()
