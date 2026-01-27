def start_game():
    #initialize the game module
    import pygame
    from Minigames import Minigame1
    from Minigames import Minigame2
    from Minigames import Minigame3

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    running = True

    #music 
    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Game music.mp3")  # Load your game music
    pygame.mixer.music.play(-1)  # Loop forever
    pygame.mixer.music.set_volume(1)  # Volume: 0.0 to 1.0

    #create 3 clicable objects as images for the game (placeholder) 
    minigame_1 = pygame.image.load("Assets/Minigame1.png")
    minigame_2 = pygame.image.load("Assets/Minigame2.png")
    minigame_3 = pygame.image.load("Assets/Minigame3.png")
    minigame_1_rect = minigame_1.get_rect(topleft=(200, 400))
    minigame_2_rect = minigame_2.get_rect(topleft=(800, 400))
    minigame_3_rect = minigame_3.get_rect(topleft=(1300, 400))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if minigame_1_rect.collidepoint(event.pos):
                    Minigame1.start_mini_game1()  # Launch Minigame 1
                if minigame_2_rect.collidepoint(event.pos):
                    Minigame2.start_mini_game2()  # Launch Minigame 2
                if minigame_3_rect.collidepoint(event.pos):
                    Minigame3.start_mini_game3()  # Launch Minigame 3
        
        #background text
        dt = clock.tick(60) / 1000  
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Game to be done", True, (255, 255, 255))
        screen.blit(text, (760, 500))

        #draw the minigame images
        screen.blit(minigame_1, minigame_1_rect)
        screen.blit(minigame_2, minigame_2_rect)
        screen.blit(minigame_3, minigame_3_rect)

        pygame.display.flip()
    pygame.quit()
