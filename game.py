from pygame import Rect

# --- Window and game state ---
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

# --- Shared tuning and animation frames ---
PLAYER_START_X = 100
PLAYER_WIDTH = 159
PLAYER_HEIGHT = 64
PLAYER_SPEED = 4
PLAYER_GRAVITY = 0.5
PLAYER_JUMP_POWER = -12
PLAYER_ANIMATION_SPEED = 10

PLAYER_IDLE_FRAMES = (
    "idle3",
    "idle4",
    "idle5",
    "idle6",
    "idle7",
    "idle8",
)

PLAYER_RUN_FRAMES = (
    "run1",
    "run2",
    "run3",
    "run4",
    "run5",
    "run6",
    "run7",
    "run8",
)

PLAYER_JUMP_FRAMES = (
    "jump1",
    "jump2",
    "jump3",
)

ENEMY_ANIMATION_SPEED = 10
ENEMY_IDLE_PAUSE = 45
ENEMY_IDLE_FRAMES = (
    "enemy_idle_0",
    "enemy_idle_1",
)
ENEMY_WALK_FRAMES = (
    "enemy_walk_0",
    "enemy_walk_1",
)

game_state = MENU
sound_enabled = True
score = 0

start_button = Rect((250, 180), (300, 60))
sound_button = Rect((250, 270), (300, 60))
exit_button = Rect((250, 360), (300, 60))

ground = Rect((0, 510), (800, 90))
platform_1 = Rect((150, 400), (180, 25))
platform_2 = Rect((430, 320), (180, 25))
platform_3 = Rect((250, 240), (160, 25))

platforms = [ground, platform_1, platform_2, platform_3]

PLAYER_HITBOX_INSET_LEFT = 30
PLAYER_HITBOX_INSET_RIGHT = 30
PLAYER_HITBOX_INSET_TOP = 8
PLAYER_HITBOX_INSET_BOTTOM = 8

ENEMY_HITBOX_INSET_LEFT = 21
ENEMY_HITBOX_INSET_RIGHT = 21
ENEMY_HITBOX_INSET_TOP = 14
ENEMY_HITBOX_INSET_BOTTOM = 16


def create_hitbox(
    x,
    y,
    width,
    height,
    inset_left,
    inset_top,
    inset_right,
    inset_bottom,
):
    return Rect(
        (x + inset_left, y + inset_top),
        (
            width - inset_left - inset_right,
            height - inset_top - inset_bottom,
        ),
    )


# --- Audio helpers ---
def stop_all_audio():
    """Stop the background music and all sound effects."""
    music.stop()
    sounds.coin.stop()
    sounds.jump.stop()
    sounds.hit.stop()
    sounds.win.stop()


def start_background_music():
    """Start the background music when sound is enabled."""
    if sound_enabled:
        music.stop()
        music.play("background")


# --- UI helpers ---
def draw_menu_button(label, button_rect):
    screen.draw.filled_rect(button_rect, BUTTON_COLOR)
    screen.draw.text(
        label,
        center=button_rect.center,
        fontsize=35,
        color=TEXT_COLOR,
    )


class Player:
    def __init__(self, x, y):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.animation_speed = PLAYER_ANIMATION_SPEED

        self.reset(x, y)

    def get_rect(self):
        return Rect(
            (self.x, self.y),
            (self.width, self.height)
        )

    def get_hitbox(self):
        return create_hitbox(
            self.x,
            self.y,
            self.width,
            self.height,
            PLAYER_HITBOX_INSET_LEFT,
            PLAYER_HITBOX_INSET_TOP,
            PLAYER_HITBOX_INSET_RIGHT,
            PLAYER_HITBOX_INSET_BOTTOM
        )

    def reset(self, x=None, y=None):
        self.x = PLAYER_START_X if x is None else x
        self.y = ground.top - self.height if y is None else y
        self.speed = PLAYER_SPEED
        self.velocity_y = 0
        self.gravity = PLAYER_GRAVITY
        self.jump_power = PLAYER_JUMP_POWER
        self.is_on_ground = True

        self.idle_frames = PLAYER_IDLE_FRAMES
        self.run_frames = PLAYER_RUN_FRAMES
        self.jump_frames = PLAYER_JUMP_FRAMES

        self.current_frame = 0
        self.animation_timer = 0
        self.current_animation = "idle"
        self.is_running = False

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

            if sound_enabled:
                sounds.jump.stop()
                sounds.jump.play()

        old_bottom = self.y + self.height - PLAYER_HITBOX_INSET_BOTTOM

        self.velocity_y += self.gravity
        self.y += self.velocity_y

        new_bottom = self.y + self.height - PLAYER_HITBOX_INSET_BOTTOM

        player_hitbox = self.get_hitbox()

        self.is_on_ground = False

        for platform in platforms:
            player_left = player_hitbox.left
            player_right = player_hitbox.right

            horizontal_collision = (
                player_right > platform.left
                and player_left < platform.right
            )

            vertical_collision = (
                self.velocity_y >= 0
                and old_bottom <= platform.top
                and new_bottom >= platform.top
            )

            if horizontal_collision and vertical_collision:
                self.y = platform.top - self.height + PLAYER_HITBOX_INSET_BOTTOM
                self.velocity_y = 0
                self.is_on_ground = True
                break

        self.x = max(0, min(self.x, WIDTH - self.width))

        self.animate()

    def animate(self):
        if not self.is_on_ground:
            new_animation = "jump"
        elif self.is_running:
            new_animation = "run"
        else:
            new_animation = "idle"

        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_frame = 0
            self.animation_timer = 0

        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            if self.current_animation == "run":
                frame_count = len(self.run_frames)
            elif self.current_animation == "jump":
                frame_count = len(self.jump_frames)
            else:
                frame_count = len(self.idle_frames)

            self.current_frame = (
                self.current_frame + 1
            ) % frame_count

    def draw(self):
        if self.current_animation == "run":
            image_name = self.run_frames[self.current_frame]
        elif self.current_animation == "jump":
            image_name = self.jump_frames[self.current_frame]
        else:
            image_name = self.idle_frames[self.current_frame]

        screen.blit(getattr(images, image_name), (self.x, self.y))


class Enemy:
    def __init__(self, x, y, left_limit, right_limit, speed):
        self.start_x = x
        self.start_y = y

        self.x = x
        self.y = y

        self.width = 64
        self.height = 64

        self.left_limit = left_limit
        self.right_limit = right_limit
        self.speed = speed
        self.animation_speed = ENEMY_ANIMATION_SPEED
        self.idle_frames = ENEMY_IDLE_FRAMES
        self.walk_frames = ENEMY_WALK_FRAMES

        self.reset()

    def get_rect(self):
        return Rect(
            (self.x, self.y),
            (self.width, self.height)
        )

    def get_hitbox(self):
        return create_hitbox(
            self.x,
            self.y,
            self.width,
            self.height,
            ENEMY_HITBOX_INSET_LEFT,
            ENEMY_HITBOX_INSET_TOP,
            ENEMY_HITBOX_INSET_RIGHT,
            ENEMY_HITBOX_INSET_BOTTOM
        )

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = 1
        self.pause_timer = 0
        self.current_frame = 0
        self.animation_timer = 0
        self.current_animation = "walk"

    def update(self):
        if self.pause_timer > 0:
            self.pause_timer -= 1
            self.animate(moving=False)
            return

        self.x += self.speed * self.direction

        if self.x <= self.left_limit:
            self.x = self.left_limit
            self.direction = 1
            self.pause_timer = ENEMY_IDLE_PAUSE

        elif self.x >= self.right_limit:
            self.x = self.right_limit
            self.direction = -1
            self.pause_timer = ENEMY_IDLE_PAUSE

        self.animate(moving=self.speed != 0)

    def animate(self, moving=True):
        new_animation = "walk" if moving else "idle"

        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.current_frame = 0
            self.animation_timer = 0

        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.current_animation == "walk":
                frame_count = len(self.walk_frames)
            else:
                frame_count = len(self.idle_frames)

            self.current_frame = (
                self.current_frame + 1
            ) % frame_count

    def draw(self):
        if self.current_animation == "idle":
            image_name = self.idle_frames[self.current_frame]
        else:
            image_name = self.walk_frames[self.current_frame]

        screen.blit(getattr(images, image_name), (self.x, self.y))


class Coin:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y

        self.x = x
        self.y = y

        self.width = 32
        self.height = 32

        self.collected = False

    def get_rect(self):
        return Rect(
            (self.x, self.y),
            (self.width, self.height)
        )

    def draw(self):
        if not self.collected:
            screen.blit(images.coin, (self.x, self.y))

    def reset(self):
        self.collected = False


class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 40
        self.height = 60

    def get_rect(self):
        return Rect(
            (self.x, self.y),
            (self.width, self.height)
        )

    def draw(self):
        screen.blit(images.flag, (self.x, self.y))


player = Player(PLAYER_START_X, ground.top - PLAYER_HEIGHT)

enemy_1 = Enemy(
    170,
    platform_1.top - 64,
    platform_1.left,
    platform_1.right - 64,
    2
)

enemy_2 = Enemy(
    450,
    platform_2.top - 64,
    platform_2.left,
    platform_2.right - 64,
    2
)

enemies = [enemy_1, enemy_2]


coin_1 = Coin(
    210,
    platform_1.top - 45
)

coin_2 = Coin(
    500,
    platform_2.top - 45
)

coin_3 = Coin(
    310,
    platform_3.top - 45
)

coin_4 = Coin(
    650,
    ground.top - 45
)

coins = [
    coin_1,
    coin_2,
    coin_3,
    coin_4
]


goal = Goal(
    745,
    ground.top - 60
)


def draw_platforms():
    for platform in platforms:
        screen.draw.filled_rect(
            platform,
            (80, 120, 60)
        )


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

        draw_menu_button("Start Game", start_button)

        sound_text = (
            "Sound: ON"
            if sound_enabled
            else "Sound: OFF"
        )

        draw_menu_button(sound_text, sound_button)
        draw_menu_button("Exit", exit_button)

    elif game_state == PLAYING:
        screen.fill(PLAY_COLOR)

        screen.draw.text(
            f"Score: {score}/{len(coins)}",
            topleft=(20, 20),
            fontsize=35,
            color="black"
        )

        draw_platforms()

        goal.draw()

        for coin in coins:
            coin.draw()

        for enemy in enemies:
            enemy.draw()

        player.draw()

        if score < len(coins):
            screen.draw.text(
                "Collect all coins!",
                center=(WIDTH // 2, 70),
                fontsize=30,
                color="black"
            )
        else:
            screen.draw.text(
                "Go to the flag!",
                center=(WIDTH // 2, 70),
                fontsize=30,
                color="black"
            )

    elif game_state == WIN:
        screen.fill(WIN_COLOR)

        screen.draw.text(
            "YOU WIN!",
            center=(WIDTH // 2, HEIGHT // 2 - 40),
            fontsize=60,
            color="white"
        )

        screen.draw.text(
            f"Score: {score}",
            center=(WIDTH // 2, HEIGHT // 2 + 30),
            fontsize=40,
            color="white"
        )

        screen.draw.text(
            "Press Enter to return menu",
            center=(WIDTH // 2, HEIGHT // 2 + 100),
            fontsize=25,
            color="white"
        )

    elif game_state == LOSE:
        screen.fill(LOSE_COLOR)

        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2 - 30),
            fontsize=60,
            color="white"
        )

        screen.draw.text(
            "Press Enter to return menu",
            center=(WIDTH // 2, HEIGHT // 2 + 50),
            fontsize=25,
            color="white"
        )


def update():
    global game_state, score

    if game_state != PLAYING:
        return

    player.update()

    # The player loses if they fall below the screen.
    if player.y > HEIGHT:
        game_state = LOSE
        stop_all_audio()

        if sound_enabled:
            sounds.hit.play()

        return

    for enemy in enemies:
        enemy.update()

    player_rect = player.get_rect()
    player_hitbox = player.get_hitbox()

    # Check coin collection.
    for coin in coins:
        if (
            not coin.collected
            and player_rect.colliderect(coin.get_rect())
        ):
            coin.collected = True
            score += 1

            if sound_enabled:
                sounds.coin.stop()
                sounds.coin.play()

    # Check enemy collisions.
    for enemy in enemies:
        if player_hitbox.colliderect(enemy.get_hitbox()):
            game_state = LOSE
            stop_all_audio()

            if sound_enabled:
                sounds.hit.play()

            return

    # Check whether the goal was reached after collecting all coins.
    if (
        score == len(coins)
        and player_rect.colliderect(goal.get_rect())
    ):
        game_state = WIN
        stop_all_audio()

        if sound_enabled:
            sounds.win.play()


def reset_game():
    global score

    score = 0
    player.reset()

    for enemy in enemies:
        enemy.reset()

    for coin in coins:
        coin.reset()


def on_mouse_down(pos):
    global game_state, sound_enabled

    if game_state != MENU:
        return

    if start_button.collidepoint(pos):
        stop_all_audio()
        reset_game()
        game_state = PLAYING
        start_background_music()

    elif sound_button.collidepoint(pos):
        sound_enabled = not sound_enabled
        # Menu music is only started when the game begins.
        stop_all_audio()

    elif exit_button.collidepoint(pos):
        stop_all_audio()
        exit()


def on_key_down(key):
    global game_state

    if game_state in (WIN, LOSE):
        if key == keys.RETURN:
            stop_all_audio()
            reset_game()
            game_state = MENU

