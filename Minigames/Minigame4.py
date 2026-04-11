import pygame
import sys
import random
from pathlib import Path

# Quiz pour le "Kitchen" 
# Structure: 
# - Fonction pour popup des informations
# - Liste des informations par "problème" dans la cuisine (librairie?)
# - Système de hover et clic pour afficher les informations
# - Faire le quiz de fin de minigame pour valider les connaissances (score sur 25?)
#  => stocker questions/options/réponses dans librairie

pygame.init()

BASE_DIR = Path(__file__).resolve().parent.parent  # project root
ASSETS_DIR = BASE_DIR / "Assets"

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Kitchen Quiz")
kitchen_image = pygame.image.load(ASSETS_DIR / "kitchen.png").convert_alpha()
kitchen_image = pygame.transform.smoothscale(kitchen_image, (WIDTH, HEIGHT))

button_img = pygame.image.load(ASSETS_DIR / "info_bubble.png").convert_alpha()
button_img = pygame.transform.scale(button_img, (75, 60))  
button_rect = button_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
show_popup = False

class ImageButton:
    def __init__(self, image, pos, hover_tint=(30, 30, 30)):
        self.image = image
        self.hover_tint = hover_tint
        self.rect = image.get_rect(center=pos)
        self._hovered = False

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self._hovered = self.rect.collidepoint(mouse_pos)

        if self._hovered:
            hover_surf = self.image.copy()
            hover_surf.fill((*self.hover_tint, 0), special_flags=pygame.BLEND_RGB_ADD)
            surface.blit(hover_surf, self.rect)
        else:
            surface.blit(self.image, self.rect)


# buttons to include: fridge, plastic bottles, trash bags, sink, light (switch)

buttons = [
    ImageButton(button_img, pos=(200, 150)),
    ImageButton(button_img, pos=(400, 300)),
    ImageButton(button_img, pos=(700, 320)), #sink info button
]

# popup function (images to be implemented in data) 
# => makes the different info pictures appear depending on the button pressed
# implement timer to make the popup disappear after a few seconds and unable to be pressed again

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(kitchen_image, (0, 0))
    
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


