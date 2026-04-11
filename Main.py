# =========================
# IMPORTS
# =========================

import pygame              # Main engine (window, events, images, sounds)
import cv2                 # OpenCV to read video (images only)
from Minigames import Minigame3  # Mini-games


# =========================
# INITIALISATION
# =========================

pygame.init()              # Initialize all pygame modules
pygame.mixer.init()        # Initialize audio system


# =========================
# CONSTANTS
# =========================

BASE_W, BASE_H = 1920, 1080    # Game logical resolution
HOVER_SCALE = 1.08             # Button hover scaling factor


# =========================
# MAIN WINDOW
# =========================

# Native fullscreen window (actual screen size)
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()    # To limit FPS


# =========================
# SCALING TOOLS
# =========================

def compute_scale_and_offset():
    """
    Computes:
    - scale: scale factor between logical resolution (1920x1080)
             and actual window
    - off_x / off_y: black bars (letterbox)
    """
    ww, wh = window.get_size()
    scale = min(ww / BASE_W, wh / BASE_H)
    off_x = (ww - BASE_W * scale) / 2
    off_y = (wh - BASE_H * scale) / 2
    return scale, off_x, off_y


def mouse_screen_to_base(mouse_pos):
    """
    Converts mouse position (actual screen)
    to logical coordinates (1920x1080)
    """
    scale, off_x, off_y = compute_scale_and_offset()
    mx, my = mouse_pos
    return ((mx - off_x) / scale, (my - off_y) / scale)


def scale_image(img, s):
    """
    Scales an image by factor s
    (used for hover animation)
    """
    w = max(1, int(img.get_width() * s))
    h = max(1, int(img.get_height() * s))
    return pygame.transform.smoothscale(img, (w, h))


PIXEL_FONT = {
    "0": [" xxx ", "x   x", "x  xx", "x x x", "xx  x", "x   x", " xxx "],
    "1": ["  x  ", " xx  ", "x x  ", "  x  ", "  x  ", "  x  ", "xxxxx"],
    "2": [" xxx ", "x   x", "    x", "   x ", "  x  ", " x   ", "xxxxx"],
    "3": [" xxx ", "x   x", "    x", "  xx ", "    x", "x   x", " xxx "],
    "4": ["   x ", "  xx ", " x x ", "x  x ", "xxxxx", "   x ", "   x "],
    "5": ["xxxxx", "x    ", "xxxx ", "    x", "    x", "x   x", " xxx "],
    "6": [" xxx ", "x    ", "x    ", "xxxx ", "x   x", "x   x", " xxx "],
    "7": ["xxxxx", "    x", "   x ", "  x  ", " x   ", " x   ", " x   "],
    "8": [" xxx ", "x   x", "x   x", " xxx ", "x   x", "x   x", " xxx "],
    "9": [" xxx ", "x   x", "x   x", " xxxx", "    x", "    x", " xxx "],
    "S": [" xxx ", "x   x", "x    ", " xxx ", "    x", "x   x", " xxx "],
    "C": [" xxx ", "x   x", "x    ", "x    ", "x    ", "x   x", " xxx "],
    "O": [" xxx ", "x   x", "x   x", "x   x", "x   x", "x   x", " xxx "],
    "R": ["xxxx ", "x   x", "x   x", "xxxx ", "x  x ", "x   x", "x   x"],
    "E": ["xxxxx", "x    ", "x    ", "xxxx ", "x    ", "x    ", "xxxxx"],
    ":": ["     ", "  x  ", "     ", "     ", "  x  ", "     ", "     "],
    " ": ["     ", "     ", "     ", "     ", "     ", "     ", "     "]
}


def render_pixel_text(text, pixel_size=8, color=(255, 255, 255), spacing=2):
    """Creates a surface containing pixel art style text."""
    text = text.upper()
    patterns = [PIXEL_FONT.get(ch, PIXEL_FONT[" "]) for ch in text]
    char_width = len(patterns[0][0]) if patterns else 0
    height = len(patterns[0]) * pixel_size if patterns else 0
    width = sum(len(pattern[0]) for pattern in patterns) * pixel_size + max(0, len(patterns) - 1) * spacing

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    x = 0
    for pattern in patterns:
        for y, row in enumerate(pattern):
            for col, pixel in enumerate(row):
                if pixel != " ":
                    surface.fill(color, (x + col * pixel_size, y * pixel_size, pixel_size, pixel_size))
        x += len(pattern[0]) * pixel_size + spacing

    return surface


# =========================
# VIDEO PLAYBACK
# =========================

def play_video(video_path, audio_path=None):
    """
    Plays a video with OpenCV.
    If audio_path is provided, plays audio with pygame in parallel.
    """

    # Start audio if present
    if audio_path is not None:
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()        # Once only
        pygame.mixer.music.set_volume(1.0)

    # Open the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video:", video_path)
        if audio_path is not None:
            pygame.mixer.music.stop()
        return

    # Get video FPS
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30

    running_video = True
    while running_video:
        # Event handling (skip possible)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_video = False
            if event.type == pygame.KEYDOWN:
                running_video = False  # Press any key = skip

        # Read a frame
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Convert OpenCV (BGR) -> Pygame (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        # Fullscreen scaling
        frame_surf = pygame.transform.scale(frame_surf, window.get_size())

        # Display
        window.blit(frame_surf, (0, 0))
        pygame.display.flip()
        clock.tick(fps)

    cap.release()

    # Stop audio at end of video
    if audio_path is not None:
        pygame.mixer.music.stop()


# =========================
# MAIN MENU (START / QUIT)
# =========================

def start_menu():
    canvas = pygame.Surface((BASE_W, BASE_H)).convert()

    # Intro music
    pygame.mixer.music.load("Assets/Test music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)

    # Background
    background = pygame.image.load("Assets/Background.png").convert()
    background = pygame.transform.scale(background, (BASE_W, BASE_H))

    # Buttons
    play_img0 = pygame.image.load("Assets/Start_button.png").convert_alpha()
    quit_img0 = pygame.image.load("Assets/Quit_button.png").convert_alpha()

    # Center position of buttons
    play_center = (BASE_W // 2, BASE_H // 2)
    quit_center = (BASE_W // 2, BASE_H // 2 + 150)

    # Real bounding box (without transparency)
    play_bbox0 = play_img0.get_bounding_rect()
    quit_bbox0 = quit_img0.get_bounding_rect()

    # Offset between image center and bbox center
    play_off = (
        play_bbox0.centerx - play_img0.get_rect().centerx,
        play_bbox0.centery - play_img0.get_rect().centery
    )
    quit_off = (
        quit_bbox0.centerx - quit_img0.get_rect().centerx,
        quit_bbox0.centery - quit_img0.get_rect().centery
    )

    # Initial hitbox
    play_hit = pygame.Rect(0, 0, play_bbox0.w, play_bbox0.h)
    quit_hit = pygame.Rect(0, 0, quit_bbox0.w, quit_bbox0.h)

    play_hit.center = (play_center[0] + play_off[0], play_center[1] + play_off[1])
    quit_hit.center = (quit_center[0] + quit_off[0], quit_center[1] + quit_off[1])

    while True:
        # Hover detection
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

        # Hover animation
        play_scale = HOVER_SCALE if hover_play else 1.0
        quit_scale = HOVER_SCALE if hover_quit else 1.0

        play_img = scale_image(play_img0, play_scale)
        quit_img = scale_image(quit_img0, quit_scale)

        play_rect = play_img.get_rect(center=play_center)
        quit_rect = quit_img.get_rect(center=quit_center)

        # Update hitboxes with scale
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

        # Drawing
        canvas.blit(background, (0, 0))
        canvas.blit(play_img, play_rect)
        canvas.blit(quit_img, quit_rect)

        # Canvas -> actual screen
        scale, off_x, off_y = compute_scale_and_offset()
        canvas_scaled = pygame.transform.smoothscale(
            canvas, (int(BASE_W * scale), int(BASE_H * scale))
        )

        window.fill((0, 0, 0))
        window.blit(canvas_scaled, (int(off_x), int(off_y)))

        pygame.display.flip()
        clock.tick(60)


# =========================
# LEVEL MENU
# =========================

def level_menu():
    canvas = pygame.Surface((BASE_W, BASE_H)).convert()

    # Game music
    pygame.mixer.music.load("Assets/Game music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)

    # Background
    background_level = pygame.image.load("Assets/background_lvl.png").convert()
    background_level = pygame.transform.scale(background_level, (BASE_W, BASE_H))

    # Mini game images
    minigame_1 = pygame.image.load("Assets/for dors.png").convert_alpha()
    minigame_2 = pygame.image.load("Assets/for dors.png").convert_alpha()
    minigame_3 = pygame.image.load("Assets/for dors.png").convert_alpha()
    minigame_4 = pygame.image.load("Assets/for dors.png").convert_alpha()

    # Positions
    r1 = minigame_1.get_rect(topleft=(550, 200))
    r2 = minigame_2.get_rect(topleft=(1050, 200))
    r3 = minigame_3.get_rect(topleft=(75, 200))
    r5 = minigame_4.get_rect(topleft=(1450, 200))

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
                    from Minigames import Minigame1v2
                    Minigame1v2.start_mini_game1v2()
                elif r2.collidepoint(pos):
                    from Minigames import Minigame2
                elif r3.collidepoint(pos):
                    Minigame3.start_mini_game3()
                elif r5.collidepoint(pos):
                    from Minigames import Minigame4
        canvas.fill((0, 0, 0))
        canvas.blit(background_level, (0, 0))

        font = pygame.font.Font(None, 74)

        # shows score with pixel art style
        score_label = render_pixel_text("SCORE:", pixel_size=8, color=(255, 255, 255), spacing=2)
        score_digits = render_pixel_text(str(score), pixel_size=8, color=(255, 255, 255), spacing=2)
        canvas.blit(score_label, (50, 50))
        canvas.blit(score_digits, (50 + score_label.get_width() + 10, 50))

        canvas.blit(minigame_1, r1)
        canvas.blit(minigame_2, r2)
        canvas.blit(minigame_3, r3)
        canvas.blit(minigame_4, r5)

        scale, off_x, off_y = compute_scale_and_offset()
        canvas_scaled = pygame.transform.smoothscale(
            canvas, (int(BASE_W * scale), int(BASE_H * scale))
        )

        window.fill((0, 0, 0))
        window.blit(canvas_scaled, (int(off_x), int(off_y)))

        pygame.display.flip()
        clock.tick(60)

score = 0  

def update_score(points):
    global score
    score += points




def result (score):
    if score < 500:
        # BAD
        play_video("Assets/Defeat.mp4", "Assets/Defeat.mp3")
    elif score < 1000:
        # MID
        play_video("Assets/Almost.mp4", "Assets/Almost.mp3")
    else:
        # WIN
        play_video("Assets/Victory.mp4", "Assets/Victory.mp3")



# =========================
# MAIN FLOW
# =========================

def main():
    # Main menu
    start = start_menu()
    score = 0  

    if not start:
        pygame.mixer.music.stop()
        pygame.quit()
        return

    # Intro video with audio
    pygame.mixer.music.stop()
    play_video("Assets/video_intro.mp4", "Assets/video_audio.mp3")

    # Level selection menu
    level_menu()

    # Final result
    result(score)

    pygame.quit()


if __name__ == "__main__":
    main()
