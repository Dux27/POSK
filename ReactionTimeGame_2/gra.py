import pygame
import random
import time
import os
import matplotlib.pyplot as plt

pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Test reakcji")

# Load a sound effect for the audio test
sound_file = "ReactionTimeGame\\sound.wav"
if os.path.exists(sound_file):
    audio_sound = pygame.mixer.Sound(sound_file)
else:
    print(f"Error: No file '{sound_file}' found in working directory '{os.getcwd()}'.")
    audio_sound = None

# Load animal images (replace with actual paths to your images)
cheetah_img = pygame.image.load("ReactionTimeGame\\cheetah.png")  # Cheetah image
rabbit_img = pygame.image.load("ReactionTimeGame\\rabbit.png")  # Rabbit image
elephant_img = pygame.image.load("ReactionTimeGame\\elephant.png")  # Elephant image

def draw_button(text, x, y):
    button_width = 200
    button_height = 50
    button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)
    return button_rect

def display_text(text, y_offset=0, color=TEXT_COLOR):
    text_surface = FONT.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 30 + y_offset))  # Position at the top
    screen.blit(text_surface, text_rect)

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

        # Display circle based on reaction time
        if reaction_time < 0.6:
            color = (0, 255, 0)  # Green
        elif reaction_time > 1.0:
            color = (255, 0, 0)  # Red
        else:
            color = (255, 255, 0)  # Yellow
        pygame.draw.circle(screen, color, (30, 30), 10)  # Draw the circle in the top left corner
        pygame.display.flip()
        pygame.time.delay(300)

    if reaction_times:
        average = sum(reaction_times) / len(reaction_times)
        best = min(reaction_times)

        screen.fill(BACKGROUND_COLOR)
        display_text("Wyniki:", -50)
        display_text(f"Średni czas: {average:.3f} s", 0)
        display_text(f"Najlepszy czas: {best:.3f} s", 50)

        # Display the appropriate animal icon based on the average reaction time
        if average < 0.6:
            animal_img = cheetah_img
        elif average > 1.0:
            animal_img = elephant_img
        else:
            animal_img = rabbit_img

        # Scale the image
        animal_img = pygame.transform.scale(animal_img, (100, 100))  # Scale the image

        # Adjust the position of the animal icon
        animal_img_x = (WINDOW_WIDTH // 2) - 50
        animal_img_y = (WINDOW_HEIGHT // 2)  # Adjust the y position to avoid overlap
        animal_rect = pygame.Rect(animal_img_x, animal_img_y, 100, 100)
        screen.blit(animal_img, (animal_img_x, animal_img_y))
        
        back_button_rect = draw_button("Powrót do menu", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 170)
        plot_button_rect = draw_button("Wyświetl wykres", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 240)
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

def main_menu():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        display_text("Główne menu", -100)
        test_reaction_button_rect = draw_button("Test reakcji", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100)
        audio_test_button_rect = draw_button("Test słuchowy", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 30)
        exit_button_rect = draw_button("Wyjście", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 40)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if test_reaction_button_rect.collidepoint(event.pos):
                    test_reaction()  # Call the reaction test
                    running = False
                elif audio_test_button_rect.collidepoint(event.pos):
                    audio_reaction_test()  # Call the audio reaction test
                    running = False
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def audio_reaction_test():
    if audio_sound is None:
        print("Error: Sound file not found. Cannot perform audio reaction test.")
        return

    running = True
    screen.fill(BACKGROUND_COLOR)
    display_text("Test słuchowy", -50)
    display_text("Naciśnij SPACJĘ, aby rozpocząć.", 50)
    display_text("Test polega na tym, że będziesz musiał kliknąć przycisk,", 100)
    display_text("gdy usłyszysz dźwięk.", 150)
    display_text("Dźwięk pojawi się w losowych momentach,", 200)
    display_text("więc bądź gotów na reakcję!", 250)
    pygame.display.flip()

    waiting_for_space = True
    while waiting_for_space:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_space = False

    points = 0
    attempts = 0
    max_attempts = 10
    is_playing = False
    sound_start_time = 0
    next_sound_time = pygame.time.get_ticks() + random.randint(2000, 10000)  # Initial random delay
    sound_played = False  # Flag to check if sound was already clicked
    sound_duration = audio_sound.get_length() * 1000  # Convert to milliseconds

    while attempts < max_attempts:
        screen.fill(BACKGROUND_COLOR)
        display_text("Słuchaj uważnie...", -50)
        display_text(f"Pozostałe kliknięcia: {max_attempts - attempts}", 0)
        click_button_rect = draw_button("Kliknij tutaj!", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100)
        pygame.display.flip()

        current_time = pygame.time.get_ticks()

        # Trigger sound at random intervals
        if not is_playing and current_time >= next_sound_time:
            audio_sound.play()
            sound_start_time = current_time
            is_playing = True
            sound_played = False  # Reset sound played flag for the new sound

        # Check if the sound has been played for the specified duration
        if is_playing and current_time - sound_start_time >= sound_duration:
            is_playing = False
            next_sound_time = current_time + random.randint(2000, 10000)  # Randomize next sound time

        # Check if the player clicked the button during the sound
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_button_rect.collidepoint(event.pos):
                    if is_playing and not sound_played:
                        points += 1
                        display_text("Super! Tak trzymaj!", 50, (0, 255, 0))
                        sound_played = True  # Prevent multiple points for the same sound
                    else:
                        display_text("Niestety, nie udało się", 50, (255, 0, 0))
                    attempts += 1  # Increment attempts (clicks)

        pygame.display.flip()
        pygame.time.delay(300)  # Wait for 300ms before clearing the screen and moving on

    # Display result after 10 attempts
    screen.fill(BACKGROUND_COLOR)
    display_text("Test zakończony!", -50)
    display_text(f"Twój wynik: {points}/{max_attempts}", 50)
    back_button_rect = draw_button("Powrót do menu", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100)
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

def main():
    main_menu()
    pygame.quit()

if __name__ == "__main__":
    main()
