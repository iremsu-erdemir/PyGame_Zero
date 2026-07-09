import sys

WIDTH = 800
HEIGHT = 600
TITLE = "Forest Runner"

MENU = "menu"
PLAYING = "playing"
WIN = "win"
LOSE = "lose"

MENU_COLOR = (30, 30, 80)
PLAY_COLOR = (100, 200, 255)
WIN_COLOR = (50, 180, 50)
LOSE_COLOR = (180, 50, 50)

BUTTON_COLOR = (70, 70, 180)
TEXT_COLOR = "white"

game_state = MENU
sound_enabled = True

start_button = Rect((250, 180), (300, 60))
sound_button = Rect((250, 270), (300, 60))
exit_button = Rect((250, 360), (300, 60))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 4
        self.velocity_y = 0
        self.is_on_ground = True

        self.idle_frames = [
            "player_idle_0",
            "player_idle_1"
        ]

        self.run_frames = [
            "player_run_0",
            "player_run_1"
        ]

        self.current_frame = 0
        self.animation_timer = 0
        self.is_running = False

    def update(self):
        self.is_running = False

        if keyboard.left:
            self.x -= self.speed
            self.is_running = True

        if keyboard.right:
            self.x += self.speed
            self.is_running = True

        # Oyuncunun ekrandan çıkmasını engeller
        self.x = max(0, min(self.x, WIDTH - 80))

        self.animate()

    def animate(self):
        self.animation_timer += 1

        if self.animation_timer >= 10:
            self.animation_timer = 0

            if self.is_running:
                self.current_frame = (self.current_frame + 1) % len(self.run_frames)
            else:
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)

    def draw(self):
        if self.is_running:
            image_name = self.run_frames[self.current_frame]
        else:
            image_name = self.idle_frames[self.current_frame]

        screen.blit(image_name, (self.x, self.y))

    def reset(self):
        self.x = 100
        self.y = 430
        self.velocity_y = 0
        self.is_on_ground = True
        self.current_frame = 0
        self.animation_timer = 0
        self.is_running = False


player = Player(100, 430)


def draw():
    screen.clear()

    if game_state == MENU:
        screen.fill(MENU_COLOR)

        screen.draw.text(
            "FOREST RUNNER",
            center=(WIDTH // 2, 80),
            fontsize=60,
            color="white"
        )

        screen.draw.filled_rect(start_button, BUTTON_COLOR)
        screen.draw.text(
            "Start Game",
            center=start_button.center,
            fontsize=35,
            color=TEXT_COLOR
        )

        screen.draw.filled_rect(sound_button, BUTTON_COLOR)
        sound_text = "Sound: ON" if sound_enabled else "Sound: OFF"

        screen.draw.text(
            sound_text,
            center=sound_button.center,
            fontsize=35,
            color=TEXT_COLOR
        )

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
            center=(WIDTH // 2, 80),
            fontsize=50,
            color="black"
        )

        player.draw()

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
    if game_state == PLAYING:
        player.update()


def on_mouse_down(pos):
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
    global game_state

    if game_state == PLAYING:
        if key == keys.W:
            game_state = WIN
        elif key == keys.L:
            game_state = LOSE

    elif game_state in (WIN, LOSE) and key == keys.ESCAPE:
        game_state = MENU
        player.reset()