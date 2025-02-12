import tkinter as tk
from tkinter import ttk, messagebox

# Funkcja wczytująca listę wulgaryzmów z pliku
# Każde słowo jest przekształcane na małe litery i dodawane do listy
# Pominięte są puste linie
def load_profanity_list():
    with open("4\\profanity.txt", "r") as file:
        return [line.strip().lower() for line in file.readlines() if line.strip()]

# Funkcja filtrująca wulgaryzmy poprzez zamianę ich na gwiazdki
# Sprawdza, czy słowo zawiera wulgaryzm i zastępuje je odpowiednią ilością gwiazdek
def filter_profanity(text, profanity_list):
    words = text.split()
    filtered_words = ["*" * len(word) if any(profanity in word.lower() for profanity in profanity_list) else word for word in words]
    return ' '.join(filtered_words)

# Funkcja konwertująca tekst na format bitowy RS232
# Dodaje bity startu i stopu zgodnie ze standardem RS232
def text_to_rs232(text):
    rs232_bits = []
    encoded_text = text.encode('utf-8')
    for byte in encoded_text:
        bits = [0] + [int(x) for x in format(byte, '08b')] + [1, 1]  # Bit startu (0), 8 bitów danych, 2 bity stopu (1)
        rs232_bits.append(bits)
    return rs232_bits

# Funkcja obsługująca konwersję tekstu w oknie nadawcy
def sender_convert():
    input_text = entry_sender.get()
    filtered_text = filter_profanity(input_text, profanity_list)  # Filtracja wulgaryzmów
    rs232_bits = text_to_rs232(filtered_text)  # Konwersja na format RS232
    rs232_display_sender.config(state=tk.NORMAL)
    rs232_display_sender.delete(1.0, tk.END)
    for bits in rs232_bits:
        rs232_display_sender.insert(tk.END, ''.join(map(str, bits)) + '\n')
    rs232_display_sender.config(state=tk.DISABLED)

# Funkcja przesyłająca skonwertowane dane do okna odbiorcy
def sender_send():
    receiver_entry.config(state=tk.NORMAL)
    receiver_entry.delete(1.0, tk.END)
    receiver_entry.insert(tk.END, rs232_display_sender.get("1.0", tk.END))
    receiver_entry.config(state=tk.DISABLED)

# Funkcja dekodująca dane w RS232 i filtrująca wulgaryzmy po stronie odbiorcy
def receiver_convert():
    rs232_bits = receiver_entry.get("1.0", tk.END).strip().splitlines()
    decoded_bytes = [int(bits[1:9], 2) for bits in rs232_bits]  # Pominięcie bitu startu i stopu
    decoded_text = bytes(decoded_bytes).decode('utf-8')  # Konwersja bajtów na tekst
    filtered_text = filter_profanity(decoded_text, profanity_list)
    entry_receiver.config(state=tk.NORMAL)
    entry_receiver.delete(0, tk.END)
    entry_receiver.insert(tk.END, filtered_text)
    entry_receiver.config(state=tk.DISABLED)

# Funkcja zamykająca aplikację
def exit_program():
    root.quit()

# Funkcja zmieniająca motyw okien programu
def change_theme(theme):
    themes = {
        "morski": "#0077b6",
        "dziewczęcy": "#ffb6c1",
        "standardowy": "SystemButtonFace",
        "ciemny": "#2c2c2c"
    }
    color = themes.get(theme, "SystemButtonFace")
    sender_window.config(bg=color)
    receiver_window.config(bg=color)

# Funkcja wyświetlająca okno pomocy
def show_help():
    messagebox.showinfo("Pomoc", "Program symuluje transmisję danych w standardzie RS232. Nadawca wysyła tekst, który jest konwertowany i przesyłany do odbiorcy. Filtruje również wulgaryzmy.")

# Inicjalizacja głównego okna programu
root = tk.Tk()
root.title("Symulacja transmisji RS232")
root.withdraw()  # Ukrycie głównego okna
profanity_list = load_profanity_list()

# Tworzenie okna nadawcy
sender_window = tk.Toplevel(root)
sender_window.title("Okno Nadawcy")

# Pasek menu w oknie nadawcy
menu_bar = tk.Menu(sender_window)

# Menu zmiany motywu
menu_theme = tk.Menu(menu_bar, tearoff=0)
menu_theme.add_command(label="Morski", command=lambda: change_theme("morski"))
menu_theme.add_command(label="Dziewczęcy", command=lambda: change_theme("dziewczęcy"))
menu_theme.add_command(label="Standardowy", command=lambda: change_theme("standardowy"))
menu_theme.add_command(label="Ciemny", command=lambda: change_theme("ciemny"))
menu_bar.add_cascade(label="Motyw", menu=menu_theme)

# Menu pomocy
menu_help = tk.Menu(menu_bar, tearoff=0)
menu_help.add_command(label="Pomoc", command=show_help)
menu_bar.add_cascade(label="Pomoc", menu=menu_help)

# Konfiguracja menu w oknie nadawcy
sender_window.config(menu=menu_bar)

# Pola wejściowe i przyciski w oknie nadawcy
entry_sender = tk.Entry(sender_window, width=50)
entry_sender.grid(row=0, column=0, padx=10, pady=10)

convert_button_sender = tk.Button(sender_window, text="Konwertuj", command=sender_convert)
convert_button_sender.grid(row=0, column=1, padx=10, pady=10)

rs232_display_sender = tk.Text(sender_window, width=50, height=10, state=tk.DISABLED)
rs232_display_sender.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

send_button = tk.Button(sender_window, text="Wyślij", command=sender_send)
send_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

exit_button_sender = tk.Button(sender_window, text="Wyjdź", command=exit_program)
exit_button_sender.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

sender_window.protocol("WM_DELETE_WINDOW", exit_program)

# Tworzenie okna odbiorcy
receiver_window = tk.Toplevel(root)
receiver_window.title("Okno Odbiorcy")

receiver_entry = tk.Text(receiver_window, width=50, height=10, state=tk.DISABLED)
receiver_entry.grid(row=0, column=0, padx=10, pady=10)

convert_button_receiver = tk.Button(receiver_window, text="Konwertuj", command=receiver_convert)
convert_button_receiver.grid(row=1, column=0, padx=10, pady=10)

entry_receiver = tk.Entry(receiver_window, width=50)
entry_receiver.grid(row=2, column=0, padx=10, pady=10)

receiver_window.protocol("WM_DELETE_WINDOW", exit_program)

# Uruchomienie pętli głównej Tkinter
root.mainloop()