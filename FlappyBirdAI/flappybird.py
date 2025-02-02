import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Stałe
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 50
GAP_HEIGHT = 200
SPEED = 3
PIPE_SPAWN_TIME = 2000  # 2 sekundy w milisekundach

# Kolory
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tworzenie okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, PIPE_SPAWN_TIME)

# Klasa ptaka
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 15
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity
    
    def draw(self):
        pygame.draw.circle(screen, BLUE, (self.x, int(self.y)), self.radius)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

# Klasa przeszkód
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
    
    def move(self):
        self.x -= SPEED
    
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + GAP_HEIGHT, PIPE_WIDTH, HEIGHT))
    
    def get_rects(self):
        return [
            pygame.Rect(self.x, 0, PIPE_WIDTH, self.height),
            pygame.Rect(self.x, self.height + GAP_HEIGHT, PIPE_WIDTH, HEIGHT)
        ]

# Inicjalizacja obiektów
bird = Bird()
pipes = [Pipe(WIDTH + i * 200) for i in range(3)]  # Inicjalizacja kilku przeszkód
score = 0
running = True

# Pętla gry
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.flap()
        if event.type == pygame.USEREVENT:
            pipes.append(Pipe(pipes[-1].x + 200))  # Generowanie nowych przeszkód za ostatnią
    
    bird.move()
    bird.draw()
    
    for pipe in pipes[:]:
        pipe.move()
        pipe.draw()
        if pipe.x + PIPE_WIDTH < 0:
            pipes.remove(pipe)
            score += 1
        
        for rect in pipe.get_rects():
            if bird.get_rect().colliderect(rect):
                running = False
    
    if bird.y > HEIGHT or bird.y < 0:
        running = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
