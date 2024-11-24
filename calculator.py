import tkinter as tk

class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.parent.title("Kalkulator")  
        self.parent.geometry("500x300")  
        
        self.wynik = ""
        
        # Tworzymy pole tekstowe do wyświetlania wyniku
        self.rezultat = tk.Text(self, height=2, width=18, font=("Arial Black", 20))
        self.rezultat.grid(columnspan=5)
        
        # Tworzymy przyciski kalkulatora
        self.stworz_przyciski()

    def stworz_przyciski(self):
        przyciski = [
            ("1", 2, 1), ("2", 2, 2), ("3", 2, 3),
            ("4", 3, 1), ("5", 3, 2), ("6", 3, 3),
            ("7", 4, 1), ("8", 4, 2), ("9", 4, 3),
            ("0", 5, 1), ("+", 2, 4), ("-", 3, 4),
            ("*", 4, 4), ("/", 5, 4), ("(", 5, 2),
            (")", 5, 3), ("=", 6, 2, 2), ("C", 6, 1),
            (".", 6, 4)
        ]
        
        for (tekst, wiersz, kolumna, *colspan) in przyciski:
            colspan_value = colspan[0] if colspan else 1  # Jeśli brak colspan, ustawiamy na 1
            self.stworz_przycisk(tekst, wiersz, kolumna, colspan_value)

    def stworz_przycisk(self, tekst, wiersz, kolumna, colspan=1):
        if tekst == "=":
            przycisk = tk.Button(self, text=tekst, command=self.podsumuj, width=12, font=("Arial", 16))
        elif tekst == "C":
            przycisk = tk.Button(self, text=tekst, command=self.clear, width=5, font=("Arial", 16))
        else:
            przycisk = tk.Button(self, text=tekst, command=lambda znak=tekst: self.zmiana_wyniku(znak), width=5, font=("Arial", 16))
        
        przycisk.grid(row=wiersz, column=kolumna, columnspan=colspan)

    def zmiana_wyniku(self, znak):
        self.wynik += str(znak)
        self.rezultat.delete(1.0, "end")
        self.rezultat.insert(1.0, self.wynik)

    def podsumuj(self):
        try:
            self.wynik = str(eval(self.wynik))  
            self.rezultat.delete(1.0, "end")
            self.rezultat.insert(1.0, self.wynik)
        except:
            self.clear()
            self.rezultat.insert(1.0, "Wystąpił Błąd!!!")

    def clear(self):
        self.wynik = ""
        self.rezultat.delete(1.0, "end")


if __name__ == "__main__":
    root = tk.Tk()
    Main(root).pack(side="top", fill="both", expand=True)
    root.mainloop()