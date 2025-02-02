import pygame
import sys
from utils import WIDTH,HEIGHT,screen, draw_text, screensettings
from game import play_game

# Inicjalizacja ekranu
screensettings()


# Funkcja do rysowania tekstu
def draw_text(text, font, color, x, y):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(x, y))
    screen.blit(rendered_text, text_rect.topleft)
    return text_rect  # Zwracamy prostokąt do obsługi kliknięć

# Funkcja do wczytywania wyników z pliku
def load_scores():
    try:
        with open("assets/high_scores.txt", "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
            return sorted(scores, reverse=True)  # Sortujemy malejąco
    except FileNotFoundError:
        return []  # Jeśli plik nie istnieje, zwracamy pustą listę

# Funkcja menu głównego
def show_menu():
    while True:
        # Tło ekranu
        screen.fill((135, 206, 250))  # Jasnoniebieskie tło

        # Wyświetlanie nagłówka
        draw_text("Flappy Bird", pygame.font.SysFont(None, 48), (255, 255, 0), WIDTH // 2, HEIGHT // 4)

        # Przyciski menu
        play_rect = draw_text("Play", pygame.font.SysFont(None, 48), (255, 255, 255), WIDTH // 2, HEIGHT // 2 - 50)
        scores_rect = draw_text("High Scores", pygame.font.SysFont(None, 48), (255, 255, 255), WIDTH // 2, HEIGHT // 2)
        exit_rect = draw_text("Exit", pygame.font.SysFont(None, 48), (255, 255, 255), WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.update()  # Aktualizacja ekranu

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Wyjście z gry
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Obsługuje kliknięcia myszką
                pos = pygame.mouse.get_pos()

                if play_rect.collidepoint(pos):  # Przycisk "Play"
                    play_game()  # Uruchomienie gry
                    return

                if scores_rect.collidepoint(pos):  # Przycisk "High Scores"
                    show_high_scores()  # Wyświetlenie tabeli wyników
                    return

                if exit_rect.collidepoint(pos):  # Przycisk "Exit"
                    pygame.quit()
                    sys.exit()

# Funkcja do zapisywania nowego wyniku
def save_score(new_score):
    scores = load_scores()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:10]  # Zapisujemy tylko 10 najlepszych wyników
    with open("assets/high_scores.txt", "w") as file:
        for score in scores:
            file.write(f"{score}\n")

# Funkcja do wyświetlania wyników
def show_high_scores():
    scores = load_scores()  # Pobieramy wyniki z pliku
    while True:
        # Tło ekranu
        screen.fill((135, 206, 250))

        # Wyświetlanie nagłówka
        draw_text("High Scores", pygame.font.SysFont(None, 48), (255, 255, 0), WIDTH // 2, HEIGHT // 4)

        # Wyświetlanie listy wyników
        y_offset = HEIGHT // 4 + 50
        if not scores:  # Jeśli nie ma wyników, wyświetlamy komunikat
            draw_text("No high scores yet", pygame.font.SysFont(None, 36), (255, 255, 255), WIDTH // 2, y_offset)
        else:
            for i, score in enumerate(scores[:5]):
                draw_text(f"{i + 1}. {score}", pygame.font.SysFont(None, 36), (255, 255, 255), WIDTH // 2, y_offset)
                y_offset += 40

        # Przycisk powrotu do menu
        back_button_rect = pygame.Rect(WIDTH // 2 - 100, y_offset + 50, 200, 40)
        pygame.draw.rect(screen, (255, 255, 255), back_button_rect, 2)  # Ramka przycisku
        draw_text("Back to Menu", pygame.font.SysFont(None, 36), (255, 255, 255), WIDTH // 2, y_offset + 70)

        pygame.display.update()  # Aktualizacja ekranu

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # Kliknięcie myszką
                pos = pygame.mouse.get_pos()

                if back_button_rect.collidepoint(pos):  # Kliknięcie "Back to Menu"
                    show_menu()  # Powrót do menu głównego, kończymy tę funkcję
                