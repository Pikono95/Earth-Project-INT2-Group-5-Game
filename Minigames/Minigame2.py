def start_mini_game2():
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        dt = clock.tick(60) / 1000  
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game to be done", True, (255, 255, 255))
        screen.blit(text, (760, 500))
        pygame.display.flip()