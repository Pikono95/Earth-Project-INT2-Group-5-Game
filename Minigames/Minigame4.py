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



# the bubble disappearence is not working, but the click to open and close the popups is working, 




def start_mini_game4():
    pygame.init()

    BASE_DIR = Path(__file__).resolve().parent.parent  # project root
    ASSETS_DIR = BASE_DIR / "Assets"

    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Kitchen Quiz")
    
    # Scaling function for fullscreen
    def compute_scale_and_offset():
        """Computes scale factor and offset for letterboxing."""
        ww, wh = screen.get_size()
        scale = min(ww / WIDTH, wh / HEIGHT)
        off_x = (ww - WIDTH * scale) / 2
        off_y = (wh - HEIGHT * scale) / 2
        return scale, off_x, off_y
    
    def screen_to_canvas_coords(screen_pos):
        """Converts screen coordinates to canvas coordinates."""
        scale, off_x, off_y = compute_scale_and_offset()
        canvas_x = (screen_pos[0] - off_x) / scale
        canvas_y = (screen_pos[1] - off_y) / scale
        return (canvas_x, canvas_y)
    
    # Create canvas for rendering at logical resolution
    canvas = pygame.Surface((WIDTH, HEIGHT))
    
    kitchen_image = pygame.image.load(ASSETS_DIR / "kitchen.png").convert_alpha()
    kitchen_image = pygame.transform.smoothscale(kitchen_image, (WIDTH, HEIGHT))

    button_img = pygame.image.load(ASSETS_DIR / "info_bubble.png").convert_alpha()
    button_img = pygame.transform.scale(button_img, (75, 60))  

    # Track open popups globally
    max_open_popups = 2
    
    class Bubble:
        def __init__(self, image, pos, popup_im = None, hover_tint=(30, 30, 30)):
            self.image = image
            self.hover_tint = hover_tint
            self.rect = image.get_rect(center=pos)
            self._hovered = False
            self.pi = popup_im  # for popup images
            self.show_popup = False
            self.pressed = False # so that the popups don't reappear once pressed

        def click(self, event, all_buttons): # for when the button is clicked and escape button pressed
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                canvas_pos = screen_to_canvas_coords(event.pos)
                if self.rect.collidepoint(canvas_pos) and self.pi:
                    # Toggle popup if already open
                    if self.show_popup:
                        self.show_popup = False
                    else:
                        # Count currently open popups
                        open_count = sum(1 for b in all_buttons if b.show_popup)
                        # Only open if less than max
                        if open_count < max_open_popups:
                            self.show_popup = True
                            self.pressed = True  # Mark as viewed

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_popup = False



        def draw(self, surface):
            mouse_pos = screen_to_canvas_coords(pygame.mouse.get_pos())
            self._hovered = self.rect.collidepoint(mouse_pos)

            if self._hovered:
                hover_surf = self.image.copy()
                hover_surf.fill((*self.hover_tint, 0), special_flags=pygame.BLEND_RGB_ADD)
                surface.blit(hover_surf, self.rect)
            else:
                surface.blit(self.image, self.rect)

        # popup function (images implemented in Assets)
        # => makes the different info pictures appear depending on the button pressed
        
        def draw_popup_to_screen(self, screen, scale, off_x, off_y):
            """Draw popup directly to screen at fullscreen scale to avoid pixelation."""
            if self.show_popup and self.pi:
                # Scale the popup image smoothly to match fullscreen scaling
                scaled_popup = pygame.transform.smoothscale(
                    self.pi, 
                    (int(self.pi.get_width() * scale), int(self.pi.get_height() * scale))
                )
                # Center on screen (not canvas)
                screen_center = screen.get_rect().center
                popup_rect = scaled_popup.get_rect(center=screen_center)
                screen.blit(scaled_popup, popup_rect)


    # buttons included: fridge, plastic bottles, trash bags, sink, light (switch)

    buttons = [
        Bubble(button_img, pos=(970, 165), popup_im=pygame.image.load(ASSETS_DIR / "bottles_info.png").convert_alpha()), # plastic bottles info button
        Bubble(button_img, pos=(1000, 300), popup_im=pygame.image.load(ASSETS_DIR / "fridge_info.png").convert_alpha()), # fridge info button
        Bubble(button_img, pos=(700, 320), popup_im=pygame.image.load(ASSETS_DIR / "sink_info.png").convert_alpha()), # sink info button
        Bubble(button_img, pos=(480, 450), popup_im=pygame.image.load(ASSETS_DIR / "trash_info.png").convert_alpha()), # trash info button
        Bubble(button_img, pos=(690, 160), popup_im=pygame.image.load(ASSETS_DIR / "light_info.png").convert_alpha()), # overhead light info button
    ]

    # Store original popup images before scaling
    popup_images = [b.pi for b in buttons if b.pi]

    # quiz


    questions = [
        (pygame.image.load(ASSETS_DIR / "q1.png").convert_alpha(), False),
        (pygame.image.load(ASSETS_DIR / "q2.png").convert_alpha(), True),
        (pygame.image.load(ASSETS_DIR / "q3.png").convert_alpha(), False),
        (pygame.image.load(ASSETS_DIR / "q4.png").convert_alpha(), False),
        (pygame.image.load(ASSETS_DIR / "q5.png").convert_alpha(), True)
    ]

    true_btn = pygame.image.load(ASSETS_DIR / "true_button.png").convert_alpha()
    false_btn = pygame.image.load(ASSETS_DIR / "false_button.png").convert_alpha()

    #scale the buttons to match hitboxes
    true_btn  = pygame.transform.scale(true_btn,  (300, 100))
    false_btn = pygame.transform.scale(false_btn, (300, 100))

    score_img = pygame.image.load(ASSETS_DIR / "score.png").convert_alpha()

    class Quiz:
        #make true/false buttons
        true_rect = pygame.Rect(180, 580, 300, 100)
        false_rect = pygame.Rect(800, 580, 300, 100)

        def __init__(self, questions, true_btn, false_btn):
            self.questions = questions
            self.true_btn = true_btn
            self.false_btn = false_btn
            self.score_img = score_img
            self.current = 0
            self.score = 0
            self.active = False
            self.finished = False

        def start(self): #initialize quiz
            self.current = 0
            self.score = 0
            self.active = True
            self.finished = False

        def click(self, event): #works similarly to the bubbles click, counts score
            if not self.active or self.finished:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                canvas_pos = screen_to_canvas_coords(event.pos)
                if self.true_rect.collidepoint(canvas_pos):
                    if self.questions[self.current][1]: #check if answer is true
                        self.score += 60 # we add 60 points since the final score is out of 300
                    self.advance()

                elif self.false_rect.collidepoint(canvas_pos):
                    if not self.questions[self.current][1]: #check if it's false
                        self.score += 60
                    self.advance()

        def advance(self):  #advances to the next question and stops when end is reached
            self.current += 1
            if self.current >= len(self.questions):
                self.finished = True

        def draw(self, surface): #draws questions and true/false
            if not self.active:
                return

            if self.finished:
                self.draw_score(surface)
                return

            img, _ = self.questions[self.current]
            surface.blit(img, img.get_rect(center=surface.get_rect().center))
            self.blit_btn(surface, self.true_btn,  self.true_rect)
            self.blit_btn(surface, self.false_btn, self.false_rect)

        def blit_btn(self, surface, img, rect):
            canvas_pos = screen_to_canvas_coords(pygame.mouse.get_pos())
            if rect.collidepoint(canvas_pos):
                hover = img.copy()
                hover.fill((30, 30, 30, 0), special_flags=pygame.BLEND_RGB_ADD)
                surface.blit(hover, rect)
            else:
                surface.blit(img, rect)

        def draw_score(self, surface): #draws score on score image

            img_rect = self.score_img.get_rect(center=surface.get_rect().center)
            surface.blit(self.score_img, img_rect)

            font = pygame.font.SysFont("Arial", 48, bold=True)
            score_text = font.render(
                f"{self.score} / {len(self.questions) * 60}", True, (60, 60, 60)
            )
            surface.blit(score_text, score_text.get_rect(center=surface.get_rect().center))

    quiz = Quiz(questions, true_btn, false_btn) #sets quiz as a usable function


    #main loop

    running = True
    end_time = None
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if quiz.active:
                quiz.click(event)
            else:
                for button in buttons:
                    button.click(event, buttons)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if all(button.pressed for button in buttons) and not quiz.active:
                    quiz.start()  # ← launch quiz if all bubbles done
                else:
                    for button in buttons:
                        button.show_popup = False

        canvas.fill((0, 0, 0))
        canvas.blit(kitchen_image, (0, 0))

        if not quiz.active:  # only draw bubbles when quiz is not running
            for button in buttons:
                button.draw(canvas)

        quiz.draw(canvas)

        # Scale canvas to fullscreen
        scale, off_x, off_y = compute_scale_and_offset()
        canvas_scaled = pygame.transform.smoothscale(canvas, (int(WIDTH * scale), int(HEIGHT * scale)))
        screen.fill((0, 0, 0))
        screen.blit(canvas_scaled, (int(off_x), int(off_y)))
        
        # Draw popups directly to screen to avoid pixelation
        if not quiz.active:
            for button in buttons:
                button.draw_popup_to_screen(screen, scale, off_x, off_y)

        pygame.display.flip()
        clock.tick(60)

        if quiz.finished and end_time is None:
            end_time = pygame.time.get_ticks()

        if end_time and pygame.time.get_ticks() - end_time > 3000:
            return quiz.score  # Return score to main game after showing it for 3 seconds


if __name__ == "__main__":
    start_mini_game4()


