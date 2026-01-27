import pygame
import Game 
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()     
running = True

# Play music
pygame.mixer.init()
pygame.mixer.music.load("Assets/Test music.mp3")
pygame.mixer.music.play(-1)  # -1 means loop forever, or use 0 for play once
pygame.mixer.music.set_volume(1) # Volume: 0.0 to 1.0

# Load and scale background image
background = pygame.image.load("Assets/Background.jpg")
background = pygame.transform.scale(background, (1920, 1080))

# Define Play button properties
button_rect_play = pygame.Rect(885, 480, 150, 50)
button_color = (100, 100, 255)
button_text_play = "Play"
font_play = pygame.font.Font(None, 36)
scale_play = 1.0

# Quit button properties
button_rect_quit = pygame.Rect(885, 600, 150, 50)
font_quit = pygame.font.Font(None, 36)
button_text_quit = "Quit"


# Variables for button animation
button_original_rect_play = button_rect_play.copy()
button_pressed_play = False 

while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #detect mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            #does the click happen on the button?
            if button_rect_play.collidepoint(event.pos):  
                button_pressed_play = True
            if button_rect_quit.collidepoint(event.pos):
                running = False
        #detect mouse release
        if event.type == pygame.MOUSEBUTTONUP:
            button_pressed_play = False
            Game.start_game()  # Start the game when Play button is released
            
    
    #Update animation for Play button
    dt = clock.tick(60) / 1000  #Delta time in seconds
    
    #Scale button based on animation for Play button
    if button_pressed_play:
        #Scale down the button
        scale_play = 0.9
        new_width = int(button_original_rect_play.width * scale_play)
        new_height = int(button_original_rect_play.height * scale_play)
        button_rect_play.width = new_width
        button_rect_play.height = new_height
        button_rect_play.center = button_original_rect_play.center
        font_play = pygame.font.Font(None, int(36 * scale_play))
    else:
        #Reset to original size
        button_rect_play = button_original_rect_play.copy()
        font_play = pygame.font.Font(None, int(36))
        scale_play = 1.0
    
    #Show the background
    screen.blit(background, (0, 0))

    #Draw the Play button
    pygame.draw.rect(screen, button_color, button_rect_play)
    text_surface = font_play.render(button_text_play, True, (255, 255, 255))
    screen.blit(text_surface, (button_rect_play.x + 50 * scale_play, button_rect_play.y + 10 * scale_play))

    #Draw the Quit button
    pygame.draw.rect(screen, (255, 100, 100), button_rect_quit)
    text_surface_quit = font_quit.render(button_text_quit, True, (255, 255, 255))
    screen.blit(text_surface_quit, (button_rect_quit.x + 50, button_rect_quit.y + 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
