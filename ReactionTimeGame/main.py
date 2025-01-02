import pygame
import random
import time
import matplotlib.pyplot as plt
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Test reakcji")

def draw_button(text, x, y):
    button_width = 200
    button_height = 50
    button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)
    return button_rect


def display_text(text, y_offset=0):
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)


def main_menu():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        display_text("Główne menu", -100)
        test_button_rect = draw_button("Test reakcji", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50)
        exit_button_rect = draw_button("Wyjście", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 50)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if test_button_rect.collidepoint(event.pos):
                    test_reaction() 
                    running = False
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit() 
def test_reaction():
    running = True
    screen.fill(BACKGROUND_COLOR)
    display_text("Test reakcji", -50)
    display_text("Kliknij przycisk tak szybko, jak tylko się pojawi!", 0)
    display_text("Naciśnij SPACJĘ, aby rozpocząć.", 50)
    pygame.display.flip()

    waiting_for_space = True
    while waiting_for_space:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_space = False

    reaction_times = []
    for _ in range(10):
        screen.fill(BACKGROUND_COLOR)
        button_rect = draw_button("Kliknij mnie!", random.randint(0, WINDOW_WIDTH - 200), random.randint(0, WINDOW_HEIGHT - 50))
        pygame.display.flip()
        start_time = time.time()
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        reaction_time = time.time() - start_time
                        reaction_times.append(reaction_time)
                        clicked = True

    if reaction_times:
        average = sum(reaction_times) / len(reaction_times)
        best = min(reaction_times)

        screen.fill(BACKGROUND_COLOR)
        display_text("Wyniki:", -50)
        display_text(f"Średni czas: {average:.3f} s", 0)
        display_text(f"Najlepszy czas: {best:.3f} s", 50)

        back_button_rect = draw_button("Powrót do menu", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100)
        plot_button_rect = draw_button("Wyświetl wykres", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 170)
        pygame.display.flip()

        waiting_for_exit = True
        while waiting_for_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        waiting_for_exit = False 
                        main_menu() 
                    elif plot_button_rect.collidepoint(event.pos):
                        plot_results(reaction_times) 

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
