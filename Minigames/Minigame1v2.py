import pygame
import sys
import os
import random


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from Main import update_score

#initialisation of the screen and pygame variables

pygame.init()

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = None
clock = None
font = pygame.font.SysFont(None, 24)

#global variables for the game

variables = {
    "Gravity" : 1,
    "Ground _height" : 450,
    "sky color" : (40, 60, 120),

}

#ennemy : trash can that moves horizontally and does damage to the player on contact

class Enemy:

    def __init__(self,x=None,y=None,vx=None,vy=0,facing="horizontal"):
        y_min = variables["Ground _height"] - 120
        y_max = variables["Ground _height"] - 30
        self.y = random.randint(y_min, y_max) if y is None else y
        self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
        if x is None:
            if random.choice([True, False]):
                self.x = -30
                self.vx = 8
            else:
                self.x = WIDTH
                self.vx = -8
        else:
            self.x = x
            self.vx = vx if vx is not None else 8
        self.vy = vy
        self.facing = facing
    
    def update(self):
        self.x += self.vx
        if self.x < -30 or self.x > WIDTH:
            return True
        return False
    
    def draw(self):
        can_x = self.x
        can_y = self.y - 50
        pygame.draw.rect(screen, (120, 120, 120), (can_x, can_y + 10, 30, 40))
        pygame.draw.rect(screen, (160, 160, 160), (can_x - 4, can_y, 38, 10))
        pygame.draw.line(screen, (80, 80, 80), (can_x + 8, can_y + 15), (can_x + 8, can_y + 45), 2)
        pygame.draw.line(screen, (80, 80, 80), (can_x + 16, can_y + 15), (can_x + 16, can_y + 45), 2)
        pygame.draw.line(screen, (80, 80, 80), (can_x + 24, can_y + 15), (can_x + 24, can_y + 45), 2)

#goop : green slime that falls and does damage

class Goop:

    def __init__(self, player_x=None):
        if player_x is None:
            self.x = random.randint(0, WIDTH - 30)
        else:
            offset = random.randint(-200, 200)
            self.x = max(0, min(WIDTH - 30, player_x + offset))
        self.y = random.randint(-200, -60)
        self.vy = random.randint(5, 8)
        self.color = (30, 180, 30)

    def update(self):
        self.y += self.vy
        if self.y > variables["Ground _height"]:
            return True
        return False

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + 15, self.y - 25), 15)

#player : white rectangle
#movement possibles : zqsd, crouch, jump

class Player: 

    def __init__(self,x,y,vx,vy,facing): #variables of the class input
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.facing = facing
        self.health = 100
    
    #update the position of the player, applies gravity, ground collision and wall collision

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
        self.vx *= 0.8
        if self.vx < 1 and self.vx > -1:
            self.vx = 0


        if self.x == 0:
            self.vx = -self.vx
        
        if self.x < 0:
            self.x = 0
        if pygame.key.get_pressed()[keys["crouch"]]: #crouching reduces the size of the player, it's hitbox and the speed of the player is reduced
            self.crouching = 25
            if self.jumping == True and self.vy < 0:
                self.vy = 40
            else:
                self.jumpingpower = -40
                self.jumping = False
        else:
            self.crouching = 0


        

    def draw(self): #the rect draw of the player, it's hitbox is reduced whene crouching
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y - 50 + self.crouching, 30, 50 - self.crouching))

    def move(self):
        speed = 10
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
            if self.crouching == 25 and self.vy == 0:
                self.vy = self.jumpingpower + 70
            elif self.vy == 0:
                self.vy = self.jumpingpower
    
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
        self.vx *= 0.6
        if self.vx < 1 and self.vx > -1:
            self.vx = 0


        if self.x == 0:
            self.vx = -self.vx
        
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - 30:
            self.x = WIDTH - 30
        if pygame.key.get_pressed()[keys["crouch"]]:
            self.crouching = 25
            if self.jumping == True and self.vy < 0:
                self.vy = 40
            else:
                self.jumpingpower = -40
                self.jumping = False
        else:
            self.crouching = 0


        

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y - 50 + self.crouching, 30, 50 - self.crouching))

    def move(self):
        speed = 10
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
            if self.crouching == 25 and self.vy == 0:
                self.vy = self.jumpingpower + 70
            elif self.vy == 0:
                self.vy = self.jumpingpower
keys = {
    "left" : pygame.K_q,
    "right" : pygame.K_d,
    "jump" : pygame.K_z,
    "crouch" : pygame.K_s,
}

def reset_game(): #the reset game function that allows the game to restart when the player looses
    global player1, enemies, spawn_timer, goop_timer, timer_ms, game_over, won
    player1 = Player(100, variables["Ground _height"], 0, 0, "right")
    enemies = []

    #the timers thingies that controls the spawn of ennemies and goop the timer of the game also

    spawn_timer = 0
    goop_timer = 0
    timer_ms = 20000
    game_over = False
    won = False

def start_mini_game1v2():
    global screen, clock, player1, enemies, spawn_timer, goop_timer, timer_ms, game_over, won, end_time

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    variables["Ground _height"] = int(HEIGHT * 0.9)
    clock = pygame.time.Clock()
    
    ################################################ game variables

    tile_width = 100
    num_tiles = (WIDTH // tile_width) + 1
    tile_states = [0] * num_tiles  # 0: safe, 1: warning, 2: polluted
    tile_timers = [0] * num_tiles
    lava_timer = 0
    player1 = Player(100, variables["Ground _height"], 0, 0, "right")
    enemies = []
    spawn_timer = 0
    goop_timer = 0
    timer_ms = 20000
    game_over = False
    won = False
    end_time = None
    run = True
    ##############################################################


    while run:
        dt = clock.tick(60)
        screen.fill(variables["sky color"])
        
        # Update pollution tiles
        lava_timer += dt
        if lava_timer > 4000:
            lava_count = random.randint(1, 2)
            safe_tiles = [i for i in range(num_tiles) if tile_states[i] == 0]
            if len(safe_tiles) >= lava_count:
                lava_indices = random.sample(safe_tiles, lava_count)
                for i in lava_indices:
                    tile_states[i] = 1  # warning
                    tile_timers[i] = 180  # 3 seconds => 60 frame a second * 3
            lava_timer = 0
        
        # Update tile timers
        for i in range(num_tiles):
            if tile_states[i] == 1:
                tile_timers[i] -= 1
                if tile_timers[i] <= 0:
                    tile_states[i] = 2  # polluted
        
        # Reset some lava tiles
        for i in range(num_tiles):
            if tile_states[i] == 2 and random.random() < 0.005:
                tile_states[i] = 0
        
        # Draw ground tiles
        for i in range(num_tiles):
            if tile_states[i] == 2:
                color = (255, 0, 0)  # polluted red
            elif tile_states[i] == 1:
                color = (128, 0, 128)  # violet warning
            else:
                color = (80, 180, 60)  # safe green
            pygame.draw.rect(screen, color, (i * tile_width, variables["Ground _height"], tile_width, HEIGHT - variables["Ground _height"]))
        
        health_ratio = player1.health / 100
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            run = False
        
        if game_over or won:
            if end_time is None:
                end_time = pygame.time.get_ticks()

            if won:
                status_text = font.render("YOU WIN! your score: " + str(int(250 * health_ratio)), True, (0, 255, 0))
            else:
                status_text = font.render("GAME OVER", True, (255, 0, 0))

            screen.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, HEIGHT // 2 - 30))

            if pygame.key.get_pressed()[pygame.K_r]:
                reset_game()
                end_time = None
                pygame.display.flip()
                continue

            elapsed = pygame.time.get_ticks() - end_time
            if elapsed >= 5000:
                run = False

            pygame.display.flip()
            continue
        
        timer_ms -= dt
        if timer_ms <= 0:
            timer_ms = 0
            won = True
        
        spawn_timer += 1
        goop_timer += 1
        if goop_timer > 20 and len(enemies) < 10:
            enemies.append(Goop(player1.x))
            goop_timer = 0
        elif spawn_timer > 26 and len(enemies) < 10:
            enemies.append(Enemy())
            spawn_timer = 0
        
        # the loop of the player update draw and all

        player1.update()
        player1.draw()
        player1.move()

        # Check for polluted tile damage
        tile_index = int(player1.x // tile_width)
        if tile_index < len(tile_states) and tile_states[tile_index] == 2:
            if random.random() < 0.05:
                player1.health -= 1

        for enemy in enemies[:]:
            if enemy.update():
                enemies.remove(enemy)
            else:
                enemy.draw()
                player_rect = pygame.Rect(player1.x, player1.y - 50 + player1.crouching, 30, 50 - player1.crouching)
                enemy_rect = pygame.Rect(enemy.x, enemy.y - 50, 30, 50)
                if player_rect.colliderect(enemy_rect):
                    player1.health -= 10
                    enemies.remove(enemy)

        #game over loop

        if player1.health <= 0:
            player1.health = 0
            game_over = True

        timer_text = font.render(f"Time: {timer_ms // 1000}", True, (255, 255, 255))
        screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

        bar_x, bar_y = 10, 10
        bar_width = 200
        bar_height = 20
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width + 2, bar_height + 2), 2)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x + 1, bar_y + 1, bar_width * health_ratio, bar_height))
        health_text = font.render(f"{player1.health}/100", True, (255, 255, 255))
        text_x = bar_x + bar_width // 2 - health_text.get_width() // 2
        text_y = bar_y + bar_height // 2 - health_text.get_height() // 2
        screen.blit(health_text, (text_x, text_y))

        pygame.display.flip()

    #the game score is based on the ratio of health the player has at the end of the game
    return int(300 * health_ratio)

#launches the game

if __name__ == "__main__":
    start_mini_game1v2()
