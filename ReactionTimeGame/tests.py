import pygame
import random
import time

import main


reaction_times = []

def random_position():
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

    for _ in range(main.GAME_DURATION):
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
        