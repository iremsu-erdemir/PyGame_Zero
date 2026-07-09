import sys

WIDTH = 800
HEIGHT = 600
TITLE = "Forest Runner"

# Oyun durumları
MENU = "menu"
PLAYING = "playing"
WIN = "win"
LOSE = "lose"

# Arka plan renkleri
MENU_COLOR = (30, 30, 80)
PLAY_COLOR = (100, 200, 255)
WIN_COLOR = (50, 180, 50)
LOSE_COLOR = (180, 50, 50)

# Buton renkleri
BUTTON_COLOR = (70, 70, 180)
TEXT_COLOR = "white"

# Oyunun başlangıç durumu
game_state = MENU

# Ses açık mı kapalı mı bilgisi
sound_enabled = True

# Menü butonları
start_button = Rect((250, 180), (300, 60))
sound_button = Rect((250, 270), (300, 60))
exit_button = Rect((250, 360), (300, 60))


def draw():
    """Oyun ekranını mevcut duruma göre çizer."""
    screen.clear()

    if game_state == MENU:
        screen.fill(MENU_COLOR)

        screen.draw.text(
            "FOREST RUNNER",
            center=(WIDTH // 2, 80),
            fontsize=60,
            color="white"
        )

        # Start Game butonu
        screen.draw.filled_rect(start_button, BUTTON_COLOR)
        screen.draw.text(
            "Start Game",
            center=start_button.center,
            fontsize=35,
            color=TEXT_COLOR
        )

        # Sound butonu
        screen.draw.filled_rect(sound_button, BUTTON_COLOR)
        sound_text = "Sound: ON" if sound_enabled else "Sound: OFF"

        screen.draw.text(
            sound_text,
            center=sound_button.center,
            fontsize=35,
            color=TEXT_COLOR
        )

        # Exit butonu
        screen.draw.filled_rect(exit_button, BUTTON_COLOR)
        screen.draw.text(
            "Exit",
            center=exit_button.center,
            fontsize=35,
            color=TEXT_COLOR
        )

    elif game_state == PLAYING:
        screen.fill(PLAY_COLOR)
        screen.draw.text(
            "GAME SCREEN",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=50,
            color="black"
        )

    elif game_state == WIN:
        screen.fill(WIN_COLOR)
        screen.draw.text(
            "YOU WIN!",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=60,
            color="white"
        )

    elif game_state == LOSE:
        screen.fill(LOSE_COLOR)
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=60,
            color="white"
        )


def update():
    """Her karede çalışan oyun güncelleme fonksiyonu."""
    pass


def on_mouse_down(pos):
    """Menü butonlarını kontrol eder."""
    global game_state, sound_enabled

    if game_state != MENU:
        return

    if start_button.collidepoint(pos):
        game_state = PLAYING

    elif sound_button.collidepoint(pos):
        sound_enabled = not sound_enabled

    elif exit_button.collidepoint(pos):
        sys.exit()


def on_key_down(key):
    """Klavye tuşlarına basıldığında çalışır."""
    global game_state

    # Test amacıyla kazanma ve kaybetme ekranları
    if game_state == PLAYING:
        if key == keys.W:
            game_state = WIN
        elif key == keys.L:
            game_state = LOSE

    # Kazanma veya kaybetme ekranından menüye dön
    elif game_state in (WIN, LOSE) and key == keys.ESCAPE:
        game_state = MENU