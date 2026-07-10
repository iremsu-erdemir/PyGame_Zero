from pygame import Rect, transform

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
score = 0

start_button = Rect((250, 180), (300, 60))
sound_button = Rect((250, 270), (300, 60))
exit_button = Rect((250, 360), (300, 60))

ground = Rect((0, 510), (800, 90))
platform_1 = Rect((150, 400), (180, 25))
platform_2 = Rect((430, 320), (180, 25))
platform_3 = Rect((250, 240), (160, 25))

platforms = [ground, platform_1, platform_2, platform_3]


def stop_all_audio():
    """Arka plan müziğini ve bütün efektleri durdurur."""
    music.stop()
    sounds.coin.stop()
    sounds.jump.stop()
    sounds.hit.stop()
    sounds.win.stop()


def start_background_music():
    """Ses açıksa arka plan müziğini başlatır."""
    if sound_enabled:
        music.stop()
        music.play("background")



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

        self.idle_frames = ["player_idle_0", "player_idle_1"]
        self.run_frames = ["player_run_0", "player_run_1"]

        self.current_frame = 0
        self.animation_timer = 0
        self.is_running = False

    def get_rect(self):
        return Rect(
            (self.x, self.y),
            (self.width, self.height)
        )

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

        # Hareketten önce oyuncunun alt kenarı
        old_bottom = self.y + self.height

        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Hareketten sonra oyuncunun alt kenarı
        new_bottom = self.y + self.height

        self.is_on_ground = False

        for platform in platforms:
            player_left = self.x
            player_right = self.x + self.width

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
                self.y = platform.top - self.height
                self.velocity_y = 0
                self.is_on_ground = True
                break

        self.x = max(0, min(self.x, WIDTH - self.width))

        self.animate()

    def animate(self):
        self.animation_timer += 1

        if self.animation_timer >= 10:
            self.animation_timer = 0

            if self.is_running:
                self.current_frame = (
                    self.current_frame + 1
                ) % len(self.run_frames)
            else:
                self.current_frame = (
                    self.current_frame + 1
                ) % len(self.idle_frames)

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
        self.direction = 1

        self.idle_frames = ["enemy_idle_0", "enemy_idle_1"]
        self.walk_frames = ["enemy_walk_0", "enemy_walk_1"]

        self.current_frame = 0
        self.animation_timer = 0

    def get_rect(self):
        return Rect(
            (self.x, self.y),
            (self.width, self.height)
        )

    def update(self):
        self.x += self.speed * self.direction

        if self.x <= self.left_limit:
            self.x = self.left_limit
            self.direction = 1

        elif self.x >= self.right_limit:
            self.x = self.right_limit
            self.direction = -1

        self.animate()

    def animate(self):
        self.animation_timer += 1

        if self.animation_timer >= 12:
            self.animation_timer = 0
            self.current_frame = (
                self.current_frame + 1
            ) % len(self.walk_frames)

    def draw(self):
        image_name = self.walk_frames[self.current_frame]

        # Düşman görselini çarpışma kutusuyla aynı boyuta getir.
        enemy_image = transform.scale(
            images.load(image_name),
            (self.width, self.height)
        )
        screen.blit(enemy_image, (self.x, self.y))

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.current_frame = 0
        self.animation_timer = 0
        self.direction = 1


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
            # Coin görselini 32x32 boyutunda çiz.
            coin_image = transform.scale(
                images.coin,
                (self.width, self.height)
            )
            screen.blit(coin_image, (self.x, self.y))

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
        # Bayrağı daha küçük çiz ve çarpışma kutusuyla eşleştir.
        flag_image = transform.scale(
            images.flag,
            (self.width, self.height)
        )
        screen.blit(flag_image, (self.x, self.y))


player = Player(100, ground.top - 90)

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

        screen.draw.filled_rect(
            start_button,
            BUTTON_COLOR
        )

        screen.draw.text(
            "Start Game",
            center=start_button.center,
            fontsize=35,
            color=TEXT_COLOR
        )

        screen.draw.filled_rect(
            sound_button,
            BUTTON_COLOR
        )

        sound_text = (
            "Sound: ON"
            if sound_enabled
            else "Sound: OFF"
        )

        screen.draw.text(
            sound_text,
            center=sound_button.center,
            fontsize=35,
            color=TEXT_COLOR
        )

        screen.draw.filled_rect(
            exit_button,
            BUTTON_COLOR
        )

        screen.draw.text(
            "Exit",
            center=exit_button.center,
            fontsize=35,
            color=TEXT_COLOR
        )

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

    # Oyuncu ekranın altına düşerse oyun kaybedilir.
    if player.y > HEIGHT:
        game_state = LOSE
        stop_all_audio()

        if sound_enabled:
            sounds.hit.play()

        return

    for enemy in enemies:
        enemy.update()

    player_rect = player.get_rect()

    # Coin toplama kontrolü
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

    # Düşman çarpışma kontrolü
    for enemy in enemies:
        if player_rect.colliderect(enemy.get_rect()):
            game_state = LOSE
            stop_all_audio()

            if sound_enabled:
                sounds.hit.play()

            return

    # Bütün coinler toplandıktan sonra hedefe ulaşma kontrolü
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

        if sound_enabled:
            # Menüde müzik başlamaz; oyun başlayınca çalar.
            stop_all_audio()
        else:
            stop_all_audio()

    elif exit_button.collidepoint(pos):
        stop_all_audio()
        exit()


def on_key_down(key):
    global game_state

    if game_state == PLAYING:
        if key == keys.W:
            game_state = WIN
            stop_all_audio()

            if sound_enabled:
                sounds.win.play()

        elif key == keys.L:
            game_state = LOSE
            stop_all_audio()

            if sound_enabled:
                sounds.hit.play()

    elif game_state in (WIN, LOSE):
        if key == keys.RETURN:
            stop_all_audio()
            reset_game()
            game_state = MENU

