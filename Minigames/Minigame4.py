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

class Bubble:
    def __init__(self, image, pos, popup_im = None, popup_dur = 6000, hover_tint=(30, 30, 30)):
        self.image = image
        self.hover_tint = hover_tint
        self.rect = image.get_rect(center=pos)
        self._hovered = False
        self.pi = popup_im  # for popup images
        self.pd = popup_dur
        self.pu_timer = 0

    def click(self, event): # for when the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.pi:
                    self.pu_timer = self.pd

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        self._hovered = self.rect.collidepoint(mouse_pos)

        if self._hovered:
            hover_surf = self.image.copy()
            hover_surf.fill((*self.hover_tint, 0), special_flags=pygame.BLEND_RGB_ADD)
            surface.blit(hover_surf, self.rect)
        else:
            surface.blit(self.image, self.rect)

    # popup function (images implemented in Assets)
    # => makes the different info pictures appear depending on the button pressed
    # implement timer to make the popup disappear after a few seconds and unable to be pressed again

    def popup(self, surface, dt):
        if self.pu_timer > 0:
            self.pu_timer -= dt # dt being delta time (time difference)
            popup_rect = self.pi.get_rect(center=surface.get_rect().center)
            surface.blit(self.pi, popup_rect)


# buttons to include: fridge, plastic bottles, trash bags, sink, light (switch)
#to be done: implement popups in assets and redirect the button image loader to them (pygame.image.load(filename))

buttons = [
    Bubble(button_img, pos=(970, 165), popup_im=pygame.image.load(ASSETS_DIR / "trash_info.png").convert_alpha()), # plastic bottles info button
    Bubble(button_img, pos=(1000, 300), popup_im=pygame.image.load(ASSETS_DIR / "trash_info.png").convert_alpha()), # fridge info button
    Bubble(button_img, pos=(700, 320), popup_im=pygame.image.load(ASSETS_DIR / "trash_info.png").convert_alpha()), # sink info button
    Bubble(button_img, pos=(480, 450), popup_im=pygame.image.load(ASSETS_DIR / "trash_info.png").convert_alpha()), # trash info button
    Bubble(button_img, pos=(690, 160), popup_im=pygame.image.load(ASSETS_DIR / "light_info.png").convert_alpha()), # overhead light info button
]


# main loop
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.click(event)


    screen.fill((0, 0, 0))
    screen.blit(kitchen_image, (0, 0))
    
    for button in buttons:
        button.draw(screen)

    for btn in buttons:
        btn.popup(screen, dt)

    pygame.display.flip()


pygame.quit()
sys.exit()


