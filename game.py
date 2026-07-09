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

# Oyunun başlangıç durumu
game_state = MENU

# Ses açık mı kapalı mı bilgisi
sound_enabled = True


def draw():
    """Oyun ekranını mevcut duruma göre çizer."""
    screen.clear()

    if game_state == MENU:
        screen.fill(MENU_COLOR)
        screen.draw.text(
            "MENU",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=60,
            color="white"
        )
        screen.draw.text(
            "Press ENTER to Start",
            center=(WIDTH // 2, HEIGHT // 2 + 20),
            fontsize=35,
            color="yellow"
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


def on_key_down(key):
    """Klavye tuşlarına basıldığında çalışır."""
    global game_state

    # Menüden oyuna geç
    if game_state == MENU and key == keys.RETURN:
        game_state = PLAYING

    # Test amacıyla kazanma ve kaybetme ekranları
    elif game_state == PLAYING:
        if key == keys.W:
            game_state = WIN
        elif key == keys.L:
            game_state = LOSE

    # Kazanma veya kaybetme ekranından menüye dön
    elif game_state in (WIN, LOSE) and key == keys.ESCAPE:
        game_state = MENU