import pygame
import random
from .fruit import Fruit
from .sounds import SoundBank

# Game Engine

WHITE = (255, 255, 255)
GREY = (170, 175, 190)
RED = (230, 70, 70)
BOMB_BLACK = (30, 30, 30)
BUTTON_COLOR = (45, 55, 90)
BUTTON_HOVER = (70, 85, 140)
FRUIT_COLORS = [(220, 60, 60), (230, 140, 40), (230, 200, 40), (90, 180, 90)]

# Spawn rate, bomb chance and launch speed for each difficulty.
DIFFICULTIES = {
    "Easy":   {"spawn_interval": 70, "bomb_chance": 0.08, "speed_scale": 0.95},
    "Medium": {"spawn_interval": 55, "bomb_chance": 0.15, "speed_scale": 1.0},
    "Hard":   {"spawn_interval": 38, "bomb_chance": 0.25, "speed_scale": 1.1},
}

TRAIL_LENGTH = 15
TRAIL_LIFETIME = 8  # frames a blade point stays visible after the mouse stops
BLADE_MARGIN = 4  # extra pixels of reach so the drawn line's width also counts
GAME_OVER_SOUND_DELAY = 30  # frames to let the bomb sound play first

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)
        self.big_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.sounds = SoundBank()

        self.best_score = 0
        self.quit_requested = False
        self.reset("Medium")

    def reset(self, difficulty):
        settings = DIFFICULTIES[difficulty]
        self.difficulty = difficulty
        self.spawn_interval = settings["spawn_interval"]  # frames between spawns
        self.bomb_chance = settings["bomb_chance"]
        self.speed_scale = settings["speed_scale"]

        self.fruits = []
        self.trail = []  # recent (x, y, frame) mouse positions, drawn as the "blade"
        self._frame = 0
        self._spawn_timer = 0

        self.lives = 3
        self.score = 0
        self.game_over = False
        self.game_over_reason = ""
        self._game_over_sound_timer = None

    def spawn_fruit(self):
        x = random.randint(60, self.width - 60)
        vy = -random.uniform(13, 16) * self.speed_scale
        vx = random.uniform(-2, 2)
        gravity = 0.35
        kind = "bomb" if random.random() < self.bomb_chance else "fruit"

        fruit = Fruit(x, self.height + 30, vx, vy, gravity, kind=kind)
        fruit.color = BOMB_BLACK if kind == "bomb" else random.choice(FRUIT_COLORS)
        self.fruits.append(fruit)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self._handle_motion(event.pos)
        elif event.type == pygame.WINDOWLEAVE:
            # Don't join the blade across the gap when the mouse re-enters.
            self.trail.clear()
        elif self.game_over:
            self._handle_menu_event(event)

    def _handle_motion(self, pos):
        x, y = pos
        self.trail.append((x, y, self._frame))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

    def _check_blade_hits(self):
        # The visible trail is the blade: every segment still on screen is
        # tested against each fruit's current position. Testing only at the
        # moment the mouse moved missed fruit that flew into the trail just
        # after the cursor passed, even though the line was drawn across it.
        segments = list(zip(self.trail, self.trail[1:]))
        for fruit in self.fruits:
            if fruit.sliced:
                continue
            for (x1, y1, _), (x2, y2, _) in segments:
                if fruit.segment_hits(x1, y1, x2, y2, BLADE_MARGIN):
                    self._slice(fruit)
                    break
            if self.game_over:
                return

    def _slice(self, fruit):
        fruit.sliced = True
        if fruit.kind == "bomb":
            self.sounds.play("bomb")
            self._end_game("You sliced a bomb!", GAME_OVER_SOUND_DELAY)
        else:
            self.sounds.play("slice")
            self.score += 1

    def _end_game(self, reason, sound_delay=0):
        self.game_over = True
        self.game_over_reason = reason
        self.best_score = max(self.best_score, self.score)
        self._game_over_sound_timer = sound_delay

    def _menu_buttons(self):
        labels = [("1  Easy", "Easy"), ("2  Medium", "Medium"), ("3  Hard", "Hard"), ("Q  Quit", "Quit")]
        width, height, gap = 130, 50, 18
        total = len(labels) * width + (len(labels) - 1) * gap
        left = (self.width - total) // 2
        top = 400
        return [
            (pygame.Rect(left + i * (width + gap), top, width, height), text, choice)
            for i, (text, choice) in enumerate(labels)
        ]

    def _handle_menu_event(self, event):
        choice = None
        if event.type == pygame.KEYDOWN:
            keys = {
                pygame.K_1: "Easy", pygame.K_KP1: "Easy",
                pygame.K_2: "Medium", pygame.K_KP2: "Medium",
                pygame.K_3: "Hard", pygame.K_KP3: "Hard",
                pygame.K_q: "Quit", pygame.K_ESCAPE: "Quit",
            }
            choice = keys.get(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect, _, button_choice in self._menu_buttons():
                if rect.collidepoint(event.pos):
                    choice = button_choice

        if choice == "Quit":
            self.quit_requested = True
        elif choice:
            self.reset(choice)

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    def update(self):
        self._frame += 1
        self.trail = [p for p in self.trail if self._frame - p[2] <= TRAIL_LIFETIME]

        if self.game_over:
            if self._game_over_sound_timer is not None:
                if self._game_over_sound_timer <= 0:
                    self.sounds.play("game_over")
                    self._game_over_sound_timer = None
                else:
                    self._game_over_sound_timer -= 1
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            self.spawn_fruit()

        for fruit in self.fruits:
            fruit.update()

        self._check_blade_hits()
        self.fruits = [fruit for fruit in self.fruits if not fruit.sliced]
        if self.game_over:
            return

        still_alive = []
        for fruit in self.fruits:
            if fruit.off_screen(self.height):
                if fruit.kind == "fruit":
                    self.lives = max(0, self.lives - 1)
                continue
            still_alive.append(fruit)
        self.fruits = still_alive

        if self.lives <= 0:
            self._end_game("You ran out of lives!")

    def render(self, screen):
        for fruit in self.fruits:
            color = getattr(fruit, "color", WHITE)
            pygame.draw.circle(screen, color, (int(fruit.x), int(fruit.y)), fruit.radius)
            if fruit.kind == "bomb":
                pygame.draw.circle(screen, RED, (int(fruit.x), int(fruit.y)), fruit.radius, 2)

        if len(self.trail) >= 2:
            pygame.draw.lines(screen, WHITE, False, [(x, y) for x, y, _ in self.trail], 3)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (self.width - 130, 10))
        difficulty_text = self.small_font.render(self.difficulty, True, GREY)
        screen.blit(difficulty_text, difficulty_text.get_rect(midtop=(self.width // 2, 14)))

        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        center_x = self.width // 2
        lines = [
            (self.big_font, "GAME OVER", RED, 150),
            (self.small_font, self.game_over_reason, GREY, 215),
            (self.font, f"Final Score: {self.score}", WHITE, 270),
            (self.small_font, f"Best this session: {self.best_score}", GREY, 310),
            (self.small_font, "Choose a difficulty to play again:", WHITE, 370),
        ]
        for font, text, color, y in lines:
            surface = font.render(text, True, color)
            screen.blit(surface, surface.get_rect(center=(center_x, y)))

        mouse_pos = pygame.mouse.get_pos()
        for rect, text, _ in self._menu_buttons():
            color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, GREY, rect, 2, border_radius=8)
            label = self.small_font.render(text, True, WHITE)
            screen.blit(label, label.get_rect(center=rect.center))
