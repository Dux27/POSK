import pygame
import matplotlib.pyplot as plt
import tests

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Reaction Game")

FONT = pygame.font.Font(None, 36)
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)


def draw_button(text, x, y, width=200, height=50):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect) 
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return button_rect


def display_text(text, y_offset=0):
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(
        center=(
            WINDOW_WIDTH // 2, 
            WINDOW_HEIGHT // 2 + y_offset
        )
    )
    screen.blit(text_surface, text_rect)


def main_menu():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        display_text("Główne menu", -100)
        test_button_rect = draw_button("Testy", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50)
        exit_button_rect = draw_button("Wyjście", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if test_button_rect.collidepoint(event.pos):
                    tests.test_reaction() 
                    running = False
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit() 


def plot_results(reaction_times):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(reaction_times) + 1), reaction_times, marker='o', color='b')
    plt.title("Czas reakcji w poszczególnych próbach")
    plt.xlabel("Numer próby")
    plt.ylabel("Czas reakcji (s)")
    plt.grid(True)
    plt.show()


def main():
    main_menu() 
    pygame.quit()

if __name__ == "__main__":
    main()
