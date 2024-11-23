import tkinter as tk
from tkinter import ttk

class Kalkulator:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x300")
        
        self.wynik = ""
        
        # Tworzymy pole tekstowe do wyświetlania wyniku
        self.rezultat = tk.Text(self.root, height=2, width=18, font=("Arial Black", 20))
        self.rezultat.grid(columnspan=5)
        
        # Tworzymy przyciski kalkulatora
        self.stworz_przyciski()

    def stworz_przyciski(self):
        # Lista przycisków i ich układ w grid
        przyciski = [
            ("1", 2, 1), ("2", 2, 2), ("3", 2, 3),
            ("4", 3, 1), ("5", 3, 2), ("6", 3, 3),
            ("7", 4, 1), ("8", 4, 2), ("9", 4, 3),
            ("0", 5, 1), ("+", 2, 4), ("-", 3, 4),
            ("*", 4, 4), ("/", 5, 4), ("(", 5, 2),
            (")", 5, 3), ("=", 6, 2, 2), ("C", 6, 1),
            (".", 6, 4)
        ]
        
        # Tworzymy przyciski
        for (tekst, wiersz, kolumna, *colspan) in przyciski:
            colspan_value = colspan[0] if colspan else 1  # Jeśli brak colspan, ustawiamy na 1
            self.stworz_przycisk(tekst, wiersz, kolumna, colspan_value)

    def stworz_przycisk(self, tekst, wiersz, kolumna, colspan=1):
        # Przycisk "=" (obliczenia)
        if tekst == "=":
            przycisk = tk.Button(self.root, text=tekst, command=self.podsumuj, width=12, font=("Arial", 16))
        # Przycisk "C" (czyszczenie)
        elif tekst == "C":
            przycisk = tk.Button(self.root, text=tekst, command=self.wyczysc, width=5, font=("Arial", 16))
        # Inne przyciski (cyfry i operatory)
        else:
            przycisk = tk.Button(self.root, text=tekst, command=lambda znak=tekst: self.zmiana_wyniku(znak), width=5, font=("Arial", 16))
        
        # Ustawiamy pozycję przycisku w gridzie
        przycisk.grid(row=wiersz, column=kolumna, columnspan=colspan)

    def zmiana_wyniku(self, znak):
        # Dodaje kliknięty znak do wyniku
        self.wynik += str(znak)
        self.rezultat.delete(1.0, "end")
        self.rezultat.insert(1.0, self.wynik)

    def podsumuj(self):
        # Oblicza wynik
        try:
            self.wynik = str(eval(self.wynik))  # Używamy eval do obliczeń
            self.rezultat.delete(1.0, "end")
            self.rezultat.insert(1.0, self.wynik)
        except:
            # Obsługuje błędy (np. nieprawidłowe wyrażenie)
            self.wyczysc()
            self.rezultat.insert(1.0, "Wystąpił Błąd!!!")

    def wyczysc(self):
        # Czyści wynik
        self.wynik = ""
        self.rezultat.delete(1.0, "end")


def main():
    # Tworzymy główne okno aplikacji
    root = tk.Tk()
    kalkulator = Kalkulator(root)  # Tworzymy obiekt kalkulatora
    root.mainloop()  # Uruchamiamy główną pętlę GUI

if __name__ == "__main__":
    main()
    