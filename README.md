# Earth-Project-INT2-Group-5-Game

## Overview

**Earth-Project-INT2-Group-5-Game** is an educational environmental game developed using Python and Pygame. The game aims to raise awareness about environmental issues through interactive minigames and quizzes. Players navigate through various challenges that highlight topics like waste management, energy conservation, and sustainable living.

## Features

- **Main Menu**: Start the game or quit.
- **Intro Video**: Engaging video introduction with audio.
- **Level Selection**: Choose from multiple minigames.
- **Minigames**:
  - **Minigame 1v2**: A side-scrolling fighter game where you avoid enemies and survive for 20 seconds.
  - **Minigame 2**: [Description to be added]
  - **Minigame 3**: [Description to be added]
  - **Minigame 4**: Kitchen quiz with interactive buttons to learn about waste management.
- **Score System**: Earn points based on performance in minigames.
- **Fullscreen Support**: Runs in fullscreen mode for immersive experience.
- **Pixel Art UI**: Custom pixel art style for score display.

## Requirements

- **Python**: Version 3.8 or higher
- **Pygame**: For game graphics and audio
- **OpenCV**: For video playback (`cv2`)
- **NumPy**: Required by OpenCV and Pygame

## Installation

1. **Clone or Download the Repository**:
   ```
   git clone https://github.com/your-repo/Earth-Project-INT2-Group-5-Game.git
   cd Earth-Project-INT2-Group-5-Game
   ```

2. **Install Dependencies**:
   ```
   pip install pygame opencv-python numpy
   ```

3. **Ensure Assets are Present**:
   - All game assets (images, sounds, videos) are located in the `Assets/` folder.
   - Make sure the following files exist:
     - `Assets/Background.png`
     - `Assets/Start_button.png`
     - `Assets/Quit_button.png`
     - `Assets/Game music.mp3`
     - `Assets/Test music.mp3`
     - `Assets/video_intro.mp4`
     - `Assets/video_audio.mp3`
     - `Assets/background_lvl.png`
     - `Assets/for dors.png`
     - `Assets/placehordler.mp4`
     - `Assets/test music.mp3`
     - And other minigame-specific assets.

## How to Run

1. **Run the Main Game**:
   ```
   python Main.py
   ```

2. **Game Flow**:
   - Start from the main menu.
   - Watch the intro video.
   - Select a minigame from the level menu.
   - Play and earn scores.
   - Return to the level menu after completing a minigame.

## Controls

### General
- **ESC**: Quit the game or return to previous menu.

### Minigame 1v2 (Fighter)
- **Q**: Move left
- **D**: Move right
- **Z**: Jump
- **S**: Crouch
- **R**: Restart (when game over)

### Minigame 4 (Kitchen Quiz)
- **Mouse Click**: Interact with buttons to view info popups.

## Project Structure

```
Earth-Project-INT2-Group-5-Game/
├── Main.py                 # Main game file with menus and flow
├── Data.py                 # Game data and constants
├── README.md               # This file
├── Assets/                 # Game assets (images, sounds, videos)
│   ├── Background.png
│   ├── Start_button.png
│   ├── Quit_button.png
│   ├── Game music.mp3
│   ├── Test music.mp3
│   ├── video_intro.mp4
│   ├── video_audio.mp3
│   ├── background_lvl.png
│   ├── for dors.png
│   ├── placehordler.mp4
│   ├── test music.mp3
│   ├── trash_info.png
│   ├── light_info.png
│   └── ...
├── Minigames/              # Individual minigame files
│   ├── __init__.py
│   ├── Minigame1.py
│   ├── Minigame1v2.py      # Active fighter minigame
│   ├── Minigame2.py
│   ├── Minigame3.py
│   └── Minigame4.py        # Kitchen quiz minigame
```

## Development Notes

- **Fullscreen Mode**: The game runs in fullscreen by default. To change, modify `pygame.display.set_mode()` in `Main.py` and minigame files.
- **Resolution**: Designed for 1920x1080 logical resolution with scaling.
- **Score Update**: Scores are updated via `update_score()` function in `Main.py`.
- **Video Playback**: Uses OpenCV for video rendering, synchronized with Pygame audio.
- **Pixel Font**: Custom pixel art font for score display.

## Credits

- **Developers**: Group 5, INT2 Class
- **Libraries**: Pygame, OpenCV, NumPy
- **Assets**: Custom created for the project
