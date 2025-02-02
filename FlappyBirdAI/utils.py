import pygame

# Inicjalizacja ekranu
def screensettings():
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    return WIDTH,HEIGHT,screen

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Funkcja do rysowania tekstu na ekranie
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect.topleft)
    return text_rect  # Zwracamy rect, aby można było sprawdzać kliknięcia

