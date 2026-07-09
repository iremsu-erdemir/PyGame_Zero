from pygame import Rect

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

ground = Rect((0, 510), (800, 90))
platform_1 = Rect((150, 400), (180, 25))
platform_2 = Rect((430, 320), (180, 25))
platform_3 = Rect((250, 240), (160, 25))

platforms = [ground, platform_1, platform_2, platform_3]


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 60
        self.height = 90

        self.speed = 4
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_power = -12
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

    def get_rect(self):
        return Rect((self.x, self.y), (self.width, self.height))

    def update(self):
        self.is_running = False

        if keyboard.left or keyboard.a:
            self.x -= self.speed
            self.is_running = True

        if keyboard.right or keyboard.d:
            self.x += self.speed
            self.is_running = True

        if (keyboard.space or keyboard.up) and self.is_on_ground:
            self.velocity_y = self.jump_power
            self.is_on_ground = False

        old_y = self.y

        self.velocity_y += self.gravity
        self.y += self.velocity_y

        self.is_on_ground = False
        player_rect = self.get_rect()

        for platform in platforms:
            if player_rect.colliderect(platform):
                old_bottom = old_y + self.height

                if self.velocity_y >= 0 and old_bottom <= platform.top:
                    self.y = platform.top - self.height
                    self.velocity_y = 0
                    self.is_on_ground = True
                    player_rect = self.get_rect()

        self.x = max(0, min(self.x, WIDTH - self.width))

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
        self.y = ground.top - self.height
        self.velocity_y = 0
        self.is_on_ground = True
        self.current_frame = 0
        self.animation_timer = 0
        self.is_running = False


player = Player(100, ground.top - 90)


def draw_platforms():
    for platform in platforms:
        screen.draw.filled_rect(platform, (80, 120, 60))


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

        draw_platforms()
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
        player.reset()

    elif sound_button.collidepoint(pos):
        sound_enabled = not sound_enabled

    elif exit_button.collidepoint(pos):
        exit()


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