import sys
import pygame
import random
import time
from utils import WIDTH,HEIGHT,screen, draw_text, screensettings

# Inicjalizacja ekranu
screensettings()

class Bird:
    def __init__(self):
        self.image = pygame.image.load("assets/bird.png")
        self.image = pygame.transform.smoothscale(self.image, (50, 50))  # Zmieniamy rozmiar ptaka na 50x50
        self.x = 100  # Pozycja X ptaka (stała)
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.radius = 25  # Dopasowanie promienia do rozmiaru ptaka
        self.angle = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, can_move):
        if can_move:
            self.velocity += self.gravity
        else:
            self.velocity = min(self.velocity + self.gravity, 10)  # Ograniczamy prędkość opadania
        self.y += self.velocity

        if self.velocity > 0:  # Spadanie
            self.angle = max(self.angle - 5, -90)
        elif self.velocity < 0:  # Skok
            self.angle = min(self.angle + 10, 45)

    def jump(self):
        self.velocity = self.jump_power
        self.angle = 45

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x, int(self.y)))
        screen.blit(rotated_image, rotated_rect.topleft)

        #Poniższy kod można od-Hashować, aby pokazać hitbox ptaka

        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius, 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap = 160
        self.height_top = random.randint(110, 270)
        self.height_bottom = HEIGHT - self.height_top - self.gap
        self.passed = False

        # Wczytujemy tekstury rur bez skalowania
        self.up_pipe_image = pygame.image.load("assets/upPipe.png")
        self.down_pipe_image = pygame.image.load("assets/downPipe.png")

        # Zapisujemy wymiary tekstur
        self.up_pipe_width = self.up_pipe_image.get_width()
        self.up_pipe_height = self.up_pipe_image.get_height()

        self.down_pipe_width = self.down_pipe_image.get_width()
        self.down_pipe_height = self.down_pipe_image.get_height()

    def move(self):
        self.x -= 3

    def draw(self):
        # Rysowanie górnej rury
        screen.blit(self.up_pipe_image, (self.x, self.height_top - self.up_pipe_height))

        # Rysowanie dolnej rury
        screen.blit(self.down_pipe_image, (self.x, HEIGHT - self.height_bottom))


        # !!!! Poniższy kod można od-Hashować, aby pokazać hitbox rór !!!!

        #pygame.draw.rect(screen, (255, 0, 0), (self.x, 0, self.up_pipe_width, self.height_top), 2)

        #pygame.draw.rect(screen, (255, 0, 0),
        #(self.x, HEIGHT - self.height_bottom, self.down_pipe_width, self.height_bottom), 2)

    def collides_with(self, bird):
        bird_hitbox = pygame.Rect(
            bird.x - bird.radius, bird.y - bird.radius, bird.radius * 2, bird.radius * 2
        )
        top_rect = pygame.Rect(self.x, 0, self.up_pipe_width, self.height_top)
        bottom_rect = pygame.Rect(self.x, HEIGHT - self.height_bottom, self.down_pipe_width, self.height_bottom)

        return bird_hitbox.colliderect(top_rect) or bird_hitbox.colliderect(bottom_rect)

    def passed_by(self, bird):
        return self.x + self.up_pipe_width < bird.x and not self.passed

    def mark_as_passed(self):
        self.passed = True


def show_game_over(score):
    from menu import show_menu,save_score

    font = pygame.font.SysFont(None, 48)

    save_score(score)

    while True:
        screen.fill((125, 196, 240))  # jasnoniebieskie tło (ekran końcowy)

        # Wyświetlanie tekstu "Game Over" i wyniku
        draw_text("Game Over", font, (255, 0, 0), WIDTH // 2, HEIGHT // 4)
        draw_text(f"Your Score: {score}", pygame.font.SysFont(None, 36), (255, 255, 255), WIDTH // 2, HEIGHT // 2)

        # Przycisk "Back to Menu"
        back_button_rect = draw_text("Back to Menu", pygame.font.SysFont(None, 36), (255, 255, 255), WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.update()  # Aktualizacja wyświetlanych elementów na ekranie

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Jeśli użytkownik kliknie myszką
                pos = pygame.mouse.get_pos()  # Pobieramy pozycję kliknięcia

                # Sprawdzamy, czy kliknięto "Back to Menu"
                if back_button_rect.collidepoint(pos):
                    show_menu()  # Od razu wywołaj show_menu() żeby przejść do menu
                    return  # Kończymy ekran końcowy gry, bo już poszliśmy do menu


def play_game(): 
    bird = Bird()
    pipes = [Pipe(WIDTH)]
    score = 0
    last_pipe_time = time.time()

    bird_falling = False
    game_over = False

    while not game_over:
        screen.fill((135, 206, 250))  # Tło
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not bird_falling:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                if event.key == pygame.K_ESCAPE:
                    from menu import show_menu  # Opóźniony import przy ESC
                    show_menu()  # Jeśli gracz wciśnie ESC, to wracamy do menu

        if time.time() - last_pipe_time > 2:
            pipes.append(Pipe(WIDTH))
            last_pipe_time = time.time()

        for pipe in pipes:
            if not bird_falling:
                pipe.move()
            pipe.draw()

            if not bird_falling and pipe.collides_with(bird):
                bird_falling = True  # Zatrzymanie sterowania ptakiem po kolizji

            if pipe.passed_by(bird):
                pipe.mark_as_passed()
                score += 1

        pipes = [pipe for pipe in pipes if pipe.x + pipe.up_pipe_width > 0]

        draw_text(f"{score}", pygame.font.SysFont(None, 48), (255, 255, 255), WIDTH // 2, 130)

        # Sprawdzanie, czy ptak dotknął ziemi
        if bird.y >= HEIGHT - 50:
            game_over = True

        bird.update(can_move=not bird_falling)  # Blokowanie kontroli ptaka po kolizji
        bird.draw()

        pygame.display.update()
        pygame.time.Clock().tick(60)

    show_game_over(score)