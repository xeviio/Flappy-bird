import pygame
from utils import screensettings
from menu import show_menu

# Inicjalizacja Pygame
pygame.init()


# Ustawienia ekranu
screensettings()

# Funkcja uruchamiająca główną logikę
def main():
    show_menu()  # Odwołujemy się do funkcji menu, która obsługuje cały proces wyboru opcji

if __name__ == "__main__":
    main()