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

# Load and scale game name image
Game_name = pygame.image.load("Assets/Game name.png")
Game_name = pygame.transform.scale(Game_name, (500, 500))

# Load and scale background image
background = pygame.image.load("Assets/Background.jpg")
background = pygame.transform.scale(background, (1920, 1080))

# Load and scale play button image
play_button_img = pygame.image.load("Assets/Play buntton.png")
play_button_img = pygame.transform.scale(play_button_img, (300, 150))
play_button_original = play_button_img.copy()

# Define Play button properties
button_rect_play = pygame.Rect(810, 430, 300, 150)
button_rect_original = button_rect_play.copy()

# Load and scale quit button image
quit_button_img = pygame.image.load("Assets/Quit buntton.png")
quit_button_img = pygame.transform.scale(quit_button_img, (300, 150))
quit_button_original = quit_button_img.copy()

# Quit button properties
button_rect_quit = pygame.Rect(810, 600, 300, 150)
button_rect_quit_original = button_rect_quit.copy()


# Variables for button animation
button_pressed_play = False
button_pressed_quit = False

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
                button_pressed_quit = True
        #detect mouse release
        if event.type == pygame.MOUSEBUTTONUP:
            if button_pressed_play:
                button_pressed_play = False
                Game.start_game()  # Start the game when Play button is released
            if button_pressed_quit:
                button_pressed_quit = False
                running = False
            
    
    #Update animation
    clock.tick(60)
    
    #Scale button based on animation for Play button
    if button_pressed_play:
        #Scale down the button
        scale_play = 0.9
        new_width = int(button_rect_original.width * scale_play)
        new_height = int(button_rect_original.height * scale_play)
        play_button_img = pygame.transform.scale(play_button_original, (new_width, new_height))
        button_rect_play.width = new_width
        button_rect_play.height = new_height
        button_rect_play.center = button_rect_original.center
    else:
        #Reset to original size
        play_button_img = play_button_original.copy()
        button_rect_play = button_rect_original.copy()
    
    #Scale button based on animation for Quit button
    if button_pressed_quit:
        #Scale down the button
        new_width = int(button_rect_quit_original.width * 0.9)
        new_height = int(button_rect_quit_original.height * 0.9)
        quit_button_img = pygame.transform.scale(quit_button_original, (new_width, new_height))
        button_rect_quit.width = new_width
        button_rect_quit.height = new_height
        button_rect_quit.center = button_rect_quit_original.center
    else:
        #Reset to original size
        quit_button_img = quit_button_original.copy()
        button_rect_quit = button_rect_quit_original.copy()
    
    #Show the background
    screen.blit(background, (0, 0))

    #Show the game name
    screen.blit(Game_name, (700, 10))

    #Draw the Play button image
    screen.blit(play_button_img, button_rect_play)

    #Draw the Quit button image
    screen.blit(quit_button_img, button_rect_quit)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
