def start_mini_game3():
    import pygame
    import random
    pygame.init()

    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption("Bathroom Chaos - Save the Water")
    clock = pygame.time.Clock()

    bg_img = pygame.image.load("assets/bathroom_bg.png").convert()
    bg_img = pygame.transform.scale(bg_img, (1920, 1080))

    tap_img = pygame.image.load("assets/tap.png").convert_alpha()
    shower_img = pygame.image.load("assets/shower.png").convert_alpha()
    big_img = pygame.image.load("assets/leak_big.png").convert_alpha()

    tap_img = pygame.transform.scale(tap_img, (135, 135))
    shower_img = pygame.transform.scale(shower_img, (135, 135))
    big_img = pygame.transform.scale(big_img, (165, 165))

    font = pygame.font.Font(None, 60)
    big_font = pygame.font.Font(None, 105)

    water = 100
    score = 0
    game_duration = 90
    total_time = 0
    spawn_timer = 0

    class Leak:
        def __init__(self):
            self.x = random.randint(150, 1650)
            self.y = random.randint(180, 930)
            self.active = True
            self.type = random.choice(["tap", "shower", "big"])

            if self.type == "tap":
                self.image = tap_img
            elif self.type == "shower":
                self.image = shower_img
            else:
                self.image = big_img

            self.rect = self.image.get_rect(center=(self.x, self.y))

        def draw(self):
            if self.active:
                screen.blit(self.image, self.rect)

        def check_click(self, pos):
            if self.active and self.rect.collidepoint(pos):
                self.active = False
                return True
            return False

    leaks = []
    running = True

    start = True
    while start:
        screen.fill((20, 20, 40))

        title = big_font.render("Bathroom Chaos", True, (255, 255, 255))
        info = font.render("Stop water leaks before it's too late!", True, (255, 255, 255))
        play = font.render("Press SPACE to start", True, (255, 200, 50))

        screen.blit(title, (630, 300))
        screen.blit(info, (540, 450))
        screen.blit(play, (645, 600))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = False

    while running:
        dt = clock.tick(60) / 1000
        total_time += dt
        spawn_timer += dt

        if total_time >= game_duration or water <= 0:
            running = False

        spawn_rate = max(0.35, 1 - total_time / 70)
        difficulty = 1 + total_time / 90

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for leak in leaks:
                    if leak.check_click(pos):
                        if leak.type == "tap":
                            score += 10
                        elif leak.type == "shower":
                            score += 20
                        else:
                            score += 30

        if spawn_timer > spawn_rate:
            leaks.append(Leak())
            spawn_timer = 0

        active_leaks = 0

        for leak in leaks:
            if leak.active:
                active_leaks += 1

                if leak.type == "tap":
                    water -= 2 * difficulty * dt
                elif leak.type == "shower":
                    water -= 4 * difficulty * dt
                else:
                    water -= 7 * difficulty * dt

        if active_leaks > 6:
            water -= 6 * dt

        if active_leaks == 0:
            water += 4 * dt

        water = max(0, min(100, water))

        screen.blit(bg_img, (0, 0))

        for leak in leaks:
            leak.draw()

        pygame.draw.rect(screen, (200, 50, 50), (60, 60, 450, 38))
        pygame.draw.rect(screen, (50, 150, 255), (60, 60, int(4.5 * water), 38))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        time_text = font.render(f"Time: {int(game_duration - total_time)}", True, (255, 255, 255))

        screen.blit(score_text, (60, 120))
        screen.blit(time_text, (60, 180))

        pygame.display.flip()


    screen.fill((0, 0, 0))

    win_score = 300
    almost_score = 250
    if score > win_score:
        score = win_score

    if score >= win_score:
        message = "YOU WON!"
        color = (50, 255, 100)
    elif score >= almost_score:
        message = "YOU WERE ALMOST THERE..."
        color = (255, 200, 50)
    else:
        message = "YOU LOST..."
        color = (255, 80, 80)

    
    end_title = big_font.render(message, True, color)
    final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))

    screen.blit(end_title, (540, 375))
    screen.blit(final_score, (780, 540))

    pygame.display.flip()
    pygame.time.wait(4000)
    return score


if __name__ == "__main__":
    start_mini_game3()