import sys
import pygame
import random
import time
from utils import WIDTH, HEIGHT, screen, draw_text, screensettings

# Inicjalizacja ekranu
screensettings()

# Wczytanie tła
t_background = pygame.image.load("assets/updated_background.png")
t_background = pygame.transform.scale(t_background, (WIDTH, HEIGHT))
background_x1 = 0
background_x2 = WIDTH
background_speed = 2.5

class Bird:
    def __init__(self):
        self.image = pygame.image.load("assets/bird.png")
        self.image = pygame.transform.smoothscale(self.image, (50, 50))
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.radius = 25
        self.angle = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, can_move):
        if can_move:
            self.velocity += self.gravity
        else:
            self.velocity = min(self.velocity + self.gravity, 10)
        self.y += self.velocity

        if self.velocity > 0:
            self.angle = max(self.angle - 5, -90)
        elif self.velocity < 0:
            self.angle = min(self.angle + 10, 45)

    def jump(self):
        self.velocity = self.jump_power
        self.angle = 45

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, int(self.y)))
        screen.blit(rotated_image, rotated_rect.topleft)

        #pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius, 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap = 160
        self.height_top = random.randint(110, 290)
        self.height_bottom = HEIGHT - self.height_top - self.gap
        self.passed = False
        self.up_pipe_image = pygame.image.load("assets/upPipe.png")
        self.down_pipe_image = pygame.image.load("assets/downPipe.png")
        self.up_pipe_width = self.up_pipe_image.get_width()
        self.down_pipe_width = self.down_pipe_image.get_width()

    def move(self):
        self.x -= 3

    def draw(self):
        screen.blit(self.up_pipe_image, (self.x, self.height_top - self.up_pipe_image.get_height()))
        screen.blit(self.down_pipe_image, (self.x, HEIGHT - self.height_bottom))

    def collides_with(self, bird):
        bird_hitbox = pygame.Rect(bird.x - bird.radius, bird.y - bird.radius, bird.radius * 2, bird.radius * 2)
        top_rect = pygame.Rect(self.x, 0, self.up_pipe_width, self.height_top)
        bottom_rect = pygame.Rect(self.x, HEIGHT - self.height_bottom, self.down_pipe_width, self.height_bottom)
        return bird_hitbox.colliderect(top_rect) or bird_hitbox.colliderect(bottom_rect)

    def passed_by(self, bird):
        return self.x + self.up_pipe_width < bird.x and not self.passed

    def mark_as_passed(self):
        self.passed = True


def play_game():
    global background_x1, background_x2, background_speed

    # Resetowanie pozycji tła i prędkości przy każdej nowej grze
    background_x1 = 0
    background_x2 = WIDTH
    background_speed = 3  # RESET prędkości tła

    # Załaduj najwyższy wynik
    from menu import load_scores
    high_scores = load_scores()
    highest_score = high_scores[0] if high_scores else 0  # Ustaw najwyższy wynik na 0, jeśli brak wyników

    bird = Bird()
    pipes = [Pipe(WIDTH)]
    score = 0
    last_pipe_time = time.time()
    bird_falling = False
    game_over = False
    new_high_score = False  # Flaga informująca o nowym rekordzie

    while not game_over:
        screen.fill((135, 206, 250))

        if not bird_falling:
            background_x1 -= background_speed
            background_x2 -= background_speed

        if background_x1 <= -WIDTH:
            background_x1 = WIDTH
        if background_x2 <= -WIDTH:
            background_x2 = WIDTH

        screen.blit(t_background, (background_x1, 0))
        screen.blit(t_background, (background_x2, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not bird_falling:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_ESCAPE:
                    from menu import show_menu
                    show_menu()

        if time.time() - last_pipe_time > 2:
            pipes.append(Pipe(WIDTH))
            last_pipe_time = time.time()

        for pipe in pipes:
            if not bird_falling:
                pipe.move()
            pipe.draw()
            if not bird_falling and pipe.collides_with(bird):
                bird_falling = True
                background_speed = 0
            if pipe.passed_by(bird):
                pipe.mark_as_passed()
                score += 1

                # Sprawdź, czy wynik jest nowym rekordem
                if score > highest_score and not new_high_score:
                    new_high_score = True

        pipes = [pipe for pipe in pipes if pipe.x + pipe.up_pipe_width > 0]

        # Wyświetl wynik
        draw_text(f"{score}", pygame.font.SysFont(None, 120), (100, 100, 255), WIDTH // 2, 130)

        # Wyświetl powiadomienie o nowym rekordzie
        if new_high_score:
            draw_text("New High Score!", pygame.font.SysFont(None, 48), (255, 215, 0), WIDTH // 2, 60)

        if bird.y >= HEIGHT - 50:
            game_over = True

        bird.update(can_move=not bird_falling)
        bird.draw()

        pygame.display.update()
        pygame.time.Clock().tick(60)

    from menu import show_game_over,save_score
    save_score(score)
    show_game_over(score)
