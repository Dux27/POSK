import pygame
import random
import time
import main

def test_reaction():
    running = True
    main.screen.fill(main.BACKGROUND_COLOR)
    main.display_text("Test reakcji", -50)
    main.display_text("Kliknij przycisk tak szybko, jak tylko się pojawi!", 0)
    main.display_text("Naciśnij SPACJĘ, aby rozpocząć.", 50)
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
    for _ in range(20):
        main.screen.fill(main.BACKGROUND_COLOR)
        button_rect = main.draw_button("Kliknij mnie!", random.randint(0, main.WINDOW_WIDTH - 200), random.randint(0, main.WINDOW_HEIGHT - 50))
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

        main.screen.fill(main.BACKGROUND_COLOR)
        main.display_text("Wyniki:", -50)
        main.display_text(f"Średni czas: {average:.3f} s", 0)
        main.display_text(f"Najlepszy czas: {best:.3f} s", 50)

        back_button_rect = main.draw_button("Powrót do menu", main.WINDOW_WIDTH // 2 - 100, main.WINDOW_HEIGHT // 2 + 100)
        plot_button_rect = main.draw_button("Wyświetl wykres", main.WINDOW_WIDTH // 2 - 100, main.WINDOW_HEIGHT // 2 + 170)
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
                        main.main_menu() 
                    elif plot_button_rect.collidepoint(event.pos):
                        main.plot_results(reaction_times)