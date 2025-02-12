import pygame
import random
import time
import logging

# Inicjalizacja pygame
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Symulator kontroli linii produkcyjnej")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Czcionka
FONT = pygame.font.Font(None, 28)
LARGE_FONT = pygame.font.Font(None, 40)
ALERT_FONT = pygame.font.Font(None, 60)  # Dodano większą czcionkę dla alertów
PANEL_TITLE_FONT = pygame.font.Font(None, 36)  # Dodano większą czcionkę dla tytułów paneli

# Timer obecności operatora
PRESENCE_INTERVAL = 30  # Sekundy
last_presence_time = time.time()
presence_confirmed = False

# Inicjalizacja logowania
logging.basicConfig(filename='Linia_produkcji_3\\log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Parametry "procesu produkcyjnego"
temperature = 50  # Temperatura (w °C)
fan_speed = 1200  # Prędkość wentylatora (RPM)
process_speed = 100  # Prędkość linii produkcyjnej
power_consumption = 0  # Zużycie prądu
alarm_active = False

# Flaga do potwierdzenia obecności operatora
lamp_on = False  # Ustawienie lampki na żółto na początku

# Flagi do obsługi przeciągania suwaków
dragging_fan_slider = False
dragging_process_slider = False
dragging_fan_control_slider = False

# Flaga do obsługi przycisku potwierdzenia
confirmation_button_clicked = False

# Czas ostatniego logowania
last_log_time = time.time()

# Czas, kiedy lampka stała się czerwona
lamp_red_time = None

# Czas, kiedy lampka alarmu temperatury stała się czerwona
temp_alarm_red_time = None

def draw_title_bar():
    pygame.draw.rect(SCREEN, BLUE, (0, 0, WIDTH, 50))
    title_text = LARGE_FONT.render("Stanowisko Kontrolne", True, WHITE)
    SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))

# Funkcje pomocnicze
def draw_lower_panel():
    global lamp_color, temp_alarm_color
    pygame.draw.rect(SCREEN, BLACK, (0, 50, WIDTH, HEIGHT - 50))
    pygame.draw.line(SCREEN, WHITE, (WIDTH // 2, 50), (WIDTH // 2, HEIGHT))

    # Lewa strona: Dane procesu
    process_text = PANEL_TITLE_FONT.render("Parametry procesu", True, WHITE)
    SCREEN.blit(process_text, (10, 60))

    temp_text = FONT.render("Temperatura:", True, WHITE)
    SCREEN.blit(temp_text, (10, 100))
    temp_value_text = FONT.render(f"{temperature:.1f} °C", True, ORANGE)
    SCREEN.blit(temp_value_text, (250, 100))

    fan_text = FONT.render("Prędkość wentylatora:", True, WHITE)
    SCREEN.blit(fan_text, (10, 140))
    fan_value_text = FONT.render(f"{fan_speed} RPM", True, ORANGE)
    SCREEN.blit(fan_value_text, (250, 140))

    speed_text = FONT.render("Prędkość linii:", True, WHITE)
    SCREEN.blit(speed_text, (10, 180))
    speed_value_text = FONT.render(f"{process_speed}%", True, ORANGE)
    SCREEN.blit(speed_value_text, (250, 180))

    power_text = FONT.render("Zużycie prądu:", True, WHITE)
    SCREEN.blit(power_text, (10, 220))
    power_value_text = FONT.render(f"{power_consumption:.1f} kW", True, ORANGE)
    SCREEN.blit(power_value_text, (250, 220))
    pygame.draw.rect(SCREEN, WHITE, (10, 240, 200, 10))
    pygame.draw.rect(SCREEN, GREEN, (10, 240, int((power_consumption - 0.5) * 40), 10))

    # Prawa strona: Kontrolki
    controls_text = PANEL_TITLE_FONT.render("Kontroler", True, WHITE)
    SCREEN.blit(controls_text, (WIDTH // 2 + 10, 60))

    # Slider prędkości wentylatora na prawej stronie
    pygame.draw.rect(SCREEN, WHITE, (WIDTH // 2 + 20, 200, 200, 10))
    pygame.draw.rect(SCREEN, GREEN, (WIDTH // 2 + 20, 200, int((fan_speed - 800) / 11), 10))
    fan_speed_control_text = FONT.render("Kontrola prędkości wentylatora", True, WHITE)
    SCREEN.blit(fan_speed_control_text, (WIDTH // 2 + 20, 180))

    # Slider prędkości linii produkcyjnej na prawej stronie
    pygame.draw.rect(SCREEN, WHITE, (WIDTH // 2 + 20, 260, 200, 10))
    pygame.draw.rect(SCREEN, GREEN, (WIDTH // 2 + 20, 260, int((process_speed - 50) * 2), 10))
    process_speed_control_text = FONT.render("Kontrola prędkości linii", True, WHITE)
    SCREEN.blit(process_speed_control_text, (WIDTH // 2 + 20, 240))

    # Lampka alarmu temperatury
    temp_alarm_color = RED if alarm_active else GREEN
    pygame.draw.circle(SCREEN, temp_alarm_color, (WIDTH // 2 + 120, 320), 20)
    temp_alarm_text = FONT.render("Alarm temperatury", True, WHITE)
    SCREEN.blit(temp_alarm_text, (WIDTH // 2 + 20, 350))

    # Lampka obecności
    lamp_color = RED if not presence_confirmed else (GREEN if lamp_on else YELLOW)
    pygame.draw.circle(SCREEN, lamp_color, (WIDTH // 2 + 120, 440), 20)
    lamp_text = FONT.render("Lampa obecności", True, WHITE)
    SCREEN.blit(lamp_text, (WIDTH // 2 + 20, 470))

    # Przycisk potwierdzenia
    pygame.draw.rect(SCREEN, BLUE, (WIDTH // 2 + 20, HEIGHT - 60, 300, 40))
    button_text = FONT.render("Potwierdź obecność", True, WHITE)
    SCREEN.blit(button_text, (WIDTH // 2 + 30, HEIGHT - 50))

def update_parameters():
    global temperature, fan_speed, process_speed, power_consumption, alarm_active, last_log_time, lamp_red_time, temp_alarm_red_time, lamp_color, temp_alarm_color

    # Symulacja parametrów
    old_temperature = temperature
    temperature += random.uniform(-0.5, 0.5)
    fan_speed += random.randint(-10, 10)
    process_speed += random.randint(-1, 1)

    # Ograniczenia parametrów
    temperature = max(30, min(90, temperature))
    fan_speed = max(800, min(3000, fan_speed))
    process_speed = max(50, min(150, process_speed))

    # Logika alarmów
    if temperature > 75:
        alarm_active = True
    else:
        alarm_active = False

    # Logowanie zmian parametrów co 5 sekund
    if time.time() - last_log_time >= 5:
        logging.info(f'Temperature: {temperature:.1f} C, Fan Speed: {fan_speed} RPM, Process Speed: {process_speed}%, Power Consumption: {power_consumption:.1f} kW')
        last_log_time = time.time()

    # Aktualizacja temperatury na podstawie prędkości wentylatora
    if fan_speed > 2000:
        temperature -= 0.1
    elif fan_speed < 1000:
        temperature += 0.1

    # Aktualizacja temperatury na podstawie prędkości linii produkcyjnej
    if process_speed > 100:
        temperature += 0.1
    elif process_speed < 100:
        temperature -= 0.1

    # Aktualizacja zużycia prądu na podstawie prędkości linii produkcyjnej i prędkości wentylatora
    power_consumption = (process_speed / 100) * (fan_speed / 1000)

def handle_presence_check():
    global lamp_on, last_presence_time, presence_confirmed, lamp_red_time
    # Sprawdzanie czasu od ostatniego potwierdzenia
    if time.time() - last_presence_time > PRESENCE_INTERVAL:
        lamp_on = False
        presence_confirmed = False
        if lamp_red_time is None:
            lamp_red_time = time.time()
    else:
        lamp_on = True
        lamp_red_time = None

def reset_presence():
    global last_presence_time, presence_confirmed, lamp_on, lamp_red_time
    last_presence_time = time.time()
    presence_confirmed = True
    lamp_on = True
    lamp_red_time = None  # Resetowanie czasu czerwonej lampki

def main():
    global presence_confirmed, fan_speed, process_speed
    global dragging_fan_slider, dragging_process_slider, dragging_fan_control_slider
    global confirmation_button_clicked, lamp_color, lamp_red_time, temp_alarm_red_time

    clock = pygame.time.Clock()
    running = True

    while running:
        SCREEN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and lamp_on:
                    reset_presence()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Obsługa suwaka wentylatora
                if 10 <= x <= 210 and 160 <= y <= 170:
                    dragging_fan_slider = True
                # Obsługa suwaka produkcji
                elif 10 <= x <= 210 and 220 <= y <= 230:
                    dragging_process_slider = True
                # Obsługa suwaka wentylatora na prawej stronie
                elif WIDTH // 2 + 20 <= x <= WIDTH // 2 + 220 and 200 <= y <= 210:
                    dragging_fan_control_slider = True
                # Obsługa suwaka prędkości linii produkcyjnej na prawej stronie
                elif WIDTH // 2 + 20 <= x <= WIDTH // 2 + 220 and 260 <= y <= 270:
                    dragging_process_slider = True
                # Obsługa przycisku potwierdzenia
                elif WIDTH // 2 + 20 <= x <= WIDTH // 2 + 320 and HEIGHT - 60 <= y <= HEIGHT - 20:
                    confirmation_button_clicked = True
                    reset_presence()
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_fan_slider = False
                dragging_process_slider = False
                dragging_fan_control_slider = False
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if dragging_fan_slider:
                    fan_speed = int(800 + (x - 10) * 11)
                elif dragging_process_slider:
                    process_speed = int(50 + (x - (WIDTH // 2 + 20)) / 2)
                elif dragging_fan_control_slider:
                    fan_speed = int(800 + (x - (WIDTH // 2 + 20)) * 11)

        # Aktualizacja
        if lamp_on or confirmation_button_clicked:
            handle_presence_check()
            update_parameters()

        draw_title_bar()
        draw_lower_panel()

        # Wyświetlanie alarmu lub kończenie gry
        if lamp_color == RED:
            if lamp_red_time is None:
                lamp_red_time = time.time()
            elif time.time() - lamp_red_time > 20:
                alarm_text = ALERT_FONT.render("Błąd: Brak potwierdzenia obecności!", True, RED)
                SCREEN.blit(alarm_text, (WIDTH // 2 - alarm_text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False
        else:
            lamp_red_time = None

        if temp_alarm_color == RED:
            if temp_alarm_red_time is None:
                temp_alarm_red_time = time.time()
            elif time.time() - temp_alarm_red_time > 20:
                alarm_text = ALERT_FONT.render("ALARM: Wysoka temperatura!", True, RED)
                SCREEN.blit(alarm_text, (WIDTH // 2 - alarm_text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False
        else:
            temp_alarm_red_time = None

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()