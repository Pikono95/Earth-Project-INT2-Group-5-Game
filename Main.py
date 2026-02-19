# =========================
# IMPORTS
# =========================

import pygame              # Moteur principal (fenêtre, events, images, sons)
import cv2                 # OpenCV pour lire la vidéo (images uniquement)
from Minigames import Minigame3  # Tes mini-jeux


# =========================
# INITIALISATION
# =========================

pygame.init()              # Initialise tous les modules pygame
pygame.mixer.init()        # Initialise le système audio


# =========================
# CONSTANTES
# =========================

BASE_W, BASE_H = 1920, 1080    # Résolution logique du jeu
HOVER_SCALE = 1.08             # Facteur d’agrandissement au survol des boutons


# =========================
# FENÊTRE PRINCIPALE
# =========================

# Fenêtre fullscreen native (taille écran réelle)
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()    # Pour limiter les FPS


# =========================
# OUTILS DE MISE À L’ÉCHELLE
# =========================

def compute_scale_and_offset():
    """
    Calcule :
    - scale : facteur d’échelle entre la résolution logique (1920x1080)
              et la fenêtre réelle
    - off_x / off_y : bandes noires (letterbox)
    """
    ww, wh = window.get_size()
    scale = min(ww / BASE_W, wh / BASE_H)
    off_x = (ww - BASE_W * scale) / 2
    off_y = (wh - BASE_H * scale) / 2
    return scale, off_x, off_y


def mouse_screen_to_base(mouse_pos):
    """
    Convertit la position de la souris (écran réel)
    en coordonnées logiques (1920x1080)
    """
    scale, off_x, off_y = compute_scale_and_offset()
    mx, my = mouse_pos
    return ((mx - off_x) / scale, (my - off_y) / scale)


def scale_image(img, s):
    """
    Redimensionne une image avec un facteur s
    (utilisé pour l’animation hover)
    """
    w = max(1, int(img.get_width() * s))
    h = max(1, int(img.get_height() * s))
    return pygame.transform.smoothscale(img, (w, h))


# =========================
# LECTURE DE LA VIDÉO
# =========================

def play_video(video_path, audio_path=None):
    """
    Joue une vidéo avec OpenCV.
    Si audio_path est fourni, joue l’audio avec pygame en parallèle.
    """

    # Lance l’audio si présent
    if audio_path is not None:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()        # Une seule fois
        pygame.mixer.music.set_volume(1.0)

    # Ouvre la vidéo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erreur: impossible d'ouvrir la vidéo:", video_path)
        if audio_path is not None:
            pygame.mixer.music.stop()
        return

    # Récupère les FPS de la vidéo
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30

    running_video = True
    while running_video:
        # Gestion des événements (skip possible)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_video = False
            if event.type == pygame.KEYDOWN:
                running_video = False  # Appuyer sur une touche = skip

        # Lecture d’une frame
        ret, frame = cap.read()
        if not ret:
            break  # Fin de la vidéo

        # Conversion OpenCV (BGR) -> Pygame (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Mise à l’échelle plein écran
        frame_surf = pygame.transform.scale(frame_surf, window.get_size())

        # Affichage
        window.blit(frame_surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)

    cap.release()

    # Stop l’audio à la fin de la vidéo
    if audio_path is not None:
        pygame.mixer.music.stop()


# =========================
# MENU PRINCIPAL (START / QUIT)
# =========================

def start_menu():
    canvas = pygame.Surface((BASE_W, BASE_H)).convert()

    # Musique d’intro
    pygame.mixer.music.load("Assets/Test music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)

    # Background
    background = pygame.image.load("Assets/Background.png").convert()
    background = pygame.transform.scale(background, (BASE_W, BASE_H))

    # Boutons
    play_img0 = pygame.image.load("Assets/Start_button.png").convert_alpha()
    quit_img0 = pygame.image.load("Assets/Quit_button.png").convert_alpha()

    # Position centrale des boutons
    play_center = (BASE_W // 2, BASE_H // 2)
    quit_center = (BASE_W // 2, BASE_H // 2 + 150)

    # Bounding box réelle (sans transparence)
    play_bbox0 = play_img0.get_bounding_rect()
    quit_bbox0 = quit_img0.get_bounding_rect()

    # Décalage entre centre image et centre bbox
    play_off = (
        play_bbox0.centerx - play_img0.get_rect().centerx,
        play_bbox0.centery - play_img0.get_rect().centery
    )
    quit_off = (
        quit_bbox0.centerx - quit_img0.get_rect().centerx,
        quit_bbox0.centery - quit_img0.get_rect().centery
    )

    # Hitbox initiale
    play_hit = pygame.Rect(0, 0, play_bbox0.w, play_bbox0.h)
    quit_hit = pygame.Rect(0, 0, quit_bbox0.w, quit_bbox0.h)

    play_hit.center = (play_center[0] + play_off[0], play_center[1] + play_off[1])
    quit_hit.center = (quit_center[0] + quit_off[0], quit_center[1] + quit_off[1])

    while True:
        # Détection du hover
        mouse_base = mouse_screen_to_base(pygame.mouse.get_pos())
        hover_play = play_hit.collidepoint(mouse_base)
        hover_quit = quit_hit.collidepoint(mouse_base)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = mouse_screen_to_base(event.pos)
                if play_hit.collidepoint(pos):
                    return True
                if quit_hit.collidepoint(pos):
                    return False

        # Animation hover
        play_scale = HOVER_SCALE if hover_play else 1.0
        quit_scale = HOVER_SCALE if hover_quit else 1.0

        play_img = scale_image(play_img0, play_scale)
        quit_img = scale_image(quit_img0, quit_scale)

        play_rect = play_img.get_rect(center=play_center)
        quit_rect = quit_img.get_rect(center=quit_center)

        # Mise à jour des hitbox avec le scale
        play_hit = pygame.Rect(0, 0, int(play_bbox0.w * play_scale), int(play_bbox0.h * play_scale))
        quit_hit = pygame.Rect(0, 0, int(quit_bbox0.w * quit_scale), int(quit_bbox0.h * quit_scale))

        play_hit.center = (
            int(play_center[0] + play_off[0] * play_scale),
            int(play_center[1] + play_off[1] * play_scale)
        )
        quit_hit.center = (
            int(quit_center[0] + quit_off[0] * quit_scale),
            int(quit_center[1] + quit_off[1] * quit_scale)
        )

        # Dessin
        canvas.blit(background, (0, 0))
        canvas.blit(play_img, play_rect)
        canvas.blit(quit_img, quit_rect)

        # Canvas -> écran réel
        scale, off_x, off_y = compute_scale_and_offset()
        canvas_scaled = pygame.transform.smoothscale(
            canvas, (int(BASE_W * scale), int(BASE_H * scale))
        )

        window.fill((0, 0, 0))
        window.blit(canvas_scaled, (int(off_x), int(off_y)))

        pygame.display.flip()
        clock.tick(60)


# =========================
# MENU DES NIVEAUX
# =========================

def level_menu():
    canvas = pygame.Surface((BASE_W, BASE_H)).convert()

    # Musique du jeu
    pygame.mixer.music.load("Assets/Game music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)

    # Background
    background_level = pygame.image.load("Assets/house.png").convert()
    background_level = pygame.transform.scale(background_level, (BASE_W, BASE_H))

    # Images des mini-jeux
    minigame_1 = pygame.image.load("Assets/Minigame1.png").convert_alpha()
    minigame_2 = pygame.image.load("Assets/Minigame2.png").convert_alpha()
    minigame_3 = pygame.image.load("Assets/Minigame3.png").convert_alpha()

    # Positions
    r1 = minigame_1.get_rect(topleft=(200, 400))
    r2 = minigame_2.get_rect(topleft=(800, 400))
    r3 = minigame_3.get_rect(topleft=(1300, 400))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = mouse_screen_to_base(event.pos)
                if r1.collidepoint(pos):
                    from Minigames import Minigame1 
                elif r2.collidepoint(pos):
                    from Minigames import Minigame2
                elif r3.collidepoint(pos):
                    Minigame3.start_mini_game3()

        canvas.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        title = font.render("Choose a level", True, (255, 255, 255))
        canvas.blit(title, (740, 120))

        canvas.blit(background_level, (0, 0))
        canvas.blit(minigame_1, r1)
        canvas.blit(minigame_2, r2)
        canvas.blit(minigame_3, r3)

        scale, off_x, off_y = compute_scale_and_offset()
        canvas_scaled = pygame.transform.smoothscale(
            canvas, (int(BASE_W * scale), int(BASE_H * scale))
        )

        window.fill((0, 0, 0))
        window.blit(canvas_scaled, (int(off_x), int(off_y)))

        pygame.display.flip()
        clock.tick(60)


# =========================
# FLUX PRINCIPAL
# =========================

def main():
    # Menu principal
    start = start_menu()

    if not start:
        pygame.mixer.music.stop()
        pygame.quit()
        return

    # Vidéo d’intro avec audio
    pygame.mixer.music.stop()
    play_video("Assets/video_intro.mp4", "Assets/video_audio.mp3")

    # Menu de sélection des niveaux
    level_menu()

    pygame.quit()


if __name__ == "__main__":
    main()
