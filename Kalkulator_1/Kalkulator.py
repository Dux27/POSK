import tkinter as tk
from tkinter import messagebox

from time import *
import math
import os


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """
        Inicjalizuje główną ramkę kalkulatora, ustawia tytuł, rozmiar, ikonę oraz tworzy pole tekstowe i przyciski.
        Ustawia również obsługę naciśnięć klawiszy.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.parent.title("Kalkulator")  
        self.parent.geometry("525x365")  
        self.parent.resizable(False, False)
        self.parent.configure(bg="white")
        self.configure(bg="white")
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.current_dir, "assets", "clock150.png")
        self.icon_path = os.path.join(self.current_dir, "assets", "KalKulator_icon.png")
        
        icon_image = tk.PhotoImage(file=self.icon_path)
        self.parent.iconphoto(True, icon_image)
        
        self.parent.bind("<Key>", self.handle_keypress)
        
        self.stworz_pole_tekstowe()
        self.stworz_przyciski()
    
    def handle_keypress(self, event):
        """
        Obsługuje naciśnięcia klawiszy. Dodaje cyfry i operatory do wyrażenia, obsługuje klawisz BackSpace do usuwania znaków
        oraz klawisz Enter do obliczania wyniku. Sprawdza, czy naciśnięty klawisz jest dozwolony, a następnie odpowiednio
        aktualizuje wyrażenie lub wynik.
        """
        # print(f"Key pressed: {event.char}")  # Debugging 
        valid_keys = "0123456789+-*/.()"
        
        if event.char in valid_keys:
            self.zmiana_wyniku(event.char)
        elif event.keysym == "BackSpace":
            self.wynik = self.wynik[:-1]
            self.rezultat.delete(1.0, "end")
            self.rezultat.insert(1.0, self.wynik)
        elif event.keysym == "Return":
            self.podsumuj() 
    
    def stworz_pole_tekstowe(self):
        """
        Tworzy pole tekstowe do wyświetlania bieżącego wyrażenia i wyniku. Ustawia odpowiednie właściwości pola tekstowego,
        takie jak wysokość, szerokość, czcionka i kolor tła. Ustawia również fokus na pole tekstowe.
        """
        self.rezultat = tk.Text(self, height=2, width=17, font=("Arial Black", 20), bg="#F5F5F5")
        self.rezultat.grid(columnspan=5, pady=10)
        self.wynik = ""

        self.rezultat.focus_set()
        
    def stworz_przyciski(self):
        """
        Tworzy przyciski kalkulatora i umieszcza je w odpowiednich miejscach na siatce. Definiuje listę przycisków z ich
        tekstem, pozycją w siatce oraz opcjonalnym colspan. Następnie iteruje przez listę przycisków i tworzy je za pomocą
        metody stworz_przycisk.
        """
        self.buttons = []
        
        przyciski = [
            ("1", 2, 1), ("2", 2, 2),   ("3", 2, 3), ("+", 2, 4),
            ("4", 3, 1), ("5", 3, 2),   ("6", 3, 3), ("-", 3, 4),
            ("7", 4, 1), ("8", 4, 2),   ("9", 4, 3), ("*", 4, 4),
            ("0", 5, 1), ("(", 5, 2),   (")", 5, 3), ("/", 5, 4),
            (".", 6, 1), ("=", 6, 2, 2),             ("C", 6, 4),
        ]
        
        for (tekst, wiersz, kolumna, *colspan) in przyciski:
            colspan_value = colspan[0] if colspan else 1  # Jeśli brak colspan, ustawiamy na 1
            self.stworz_przycisk(tekst, wiersz, kolumna, colspan_value)

    def stworz_przycisk(self, tekst, wiersz, kolumna, colspan=1):
        """
        Tworzy pojedynczy przycisk kalkulatora z odpowiednią funkcjonalnością w zależności od tekstu na przycisku.
        Jeśli tekst przycisku to '=', przycisk oblicza wynik wyrażenia. Jeśli tekst to 'C', przycisk czyści pole tekstowe.
        W przeciwnym razie przycisk dodaje odpowiedni znak do wyrażenia.
        """
        if tekst == "=":
            przycisk = tk.Button(self, text=tekst, command=self.podsumuj, width=12, font=("Arial", 16))
        elif tekst == "C":
            przycisk = tk.Button(self, text=tekst, command=self.clear, width=5, font=("Arial", 16))          
        else:
            przycisk = tk.Button(self, text=tekst, command=lambda znak=tekst: self.zmiana_wyniku(znak), width=5, font=("Arial", 16))
        
        self.buttons.append(przycisk)
        przycisk.grid(row=wiersz, column=kolumna, columnspan=colspan, padx=5, pady=5)
        

    def zmiana_wyniku(self, znak):
        """
        Aktualizuje bieżące wyrażenie na podstawie wprowadzonego znaku i wyświetla je w polu tekstowym.
        Dodaje znak do bieżącego wyrażenia, a następnie aktualizuje zawartość pola tekstowego.
        """
        self.wynik += str(znak)
        # print(f"Current expression: {self.wynik}")  # Debugging line
        self.rezultat.delete(1.0, "end")
        self.rezultat.insert(1.0, self.wynik)

    def podsumuj(self):
        """
        Oblicza wynik bieżącego wyrażenia i wyświetla go w polu tekstowym. W przypadku błędu wyświetla komunikat 'Error'.
        Pobiera bieżące wyrażenie, usuwa białe znaki, oblicza wynik za pomocą funkcji eval i aktualizuje pole tekstowe.
        Jeśli wystąpi błąd, czyści pole tekstowe i wyświetla komunikat 'Error'.
        """
        try:
            expression = self.wynik.strip()

            self.wynik = str(eval(expression))  
            self.rezultat.delete(1.0, "end")  # Clear the Text widget
            self.rezultat.insert(1.0, self.wynik)  # Insert the evaluated result
        except:
            self.clear()
            self.rezultat.insert(1.0, "Error")

    def clear(self):
        """
        Czyści bieżące wyrażenie i pole tekstowe. Ustawia bieżące wyrażenie na pusty ciąg znaków i usuwa zawartość
        pola tekstowego.
        """
        self.wynik = ""
        self.rezultat.delete(1.0, "end")        
        
    def change_button_color(self, color: str):
        """
        Zmienia kolor wszystkich przycisków kalkulatora na podany kolor. Iteruje przez listę przycisków i ustawia
        ich kolor tła na podany kolor.
        """
        for b in self.buttons:
            b.configure(bg=color)


class ClockFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """
        Inicjalizuje ramkę zegara i wybiera typ zegara (analogowy lub cyfrowy). Ustawia tło ramki na biały kolor
        i wywołuje metodę choose_clock, aby zainicjalizować odpowiedni zegar.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.configure(bg="white")
        
        self.clock = ""
        self.choose_clock(self.clock)     
    
    def choose_clock(self, clock: str):
        """
        Wybiera typ zegara (analogowy lub cyfrowy) i inicjalizuje odpowiedni zegar. Usuwa wszystkie istniejące widgety
        z ramki, a następnie wywołuje odpowiednią metodę inicjalizacji zegara w zależności od wartości parametru clock.
        """
        for widget in self.winfo_children():
            widget.destroy()
        
        if clock == "analog":
            self.inicialize_analog_clock()   
        else:   
            self.inicialize_digital_clock()         
                          
    ### DIGITAL CLOCK FUNCTIONS
    def inicialize_digital_clock(self):
        """
        Inicjalizuje zegar cyfrowy i ustawia jego aktualizację co sekundę. Tworzy etykietę zegara cyfrowego z odpowiednią
        czcionką, kolorem tekstu i tła, a następnie wywołuje metodę update_digital_timer, aby rozpocząć aktualizację czasu.
        """
        self.digitalTimer = tk.Label(self, font=('calibri', 30, 'bold'), foreground='black', bg="white")
        self.digitalTimer.pack(pady=20)
        self.update_digital_timer()
    
    def update_digital_timer(self):
        """
        Aktualizuje czas na zegarze cyfrowym co sekundę. Pobiera bieżący czas w formacie HH:MM:SS, ustawia tekst etykiety
        zegara cyfrowego na pobrany czas, a następnie ustawia wywołanie tej samej metody po upływie jednej sekundy.
        """
        string = strftime('%H:%M:%S')  
        self.digitalTimer.config(text=string)   
        self.digitalTimer.after(1000, self.update_digital_timer)
   
   
    ### ANALOG CLOCK FUNCTIONS
    def inicialize_analog_clock(self):
        """
        Inicjalizuje zegar analogowy, tworzy płótno, tarczę zegara i wskazówki oraz ustawia ich aktualizację co sekundę.
        Ustawia rozmiar płótna, długości i szerokości wskazówek, a następnie wywołuje metody create_clock_canvas,
        create_clock_face i create_sticks, aby utworzyć elementy zegara. Na końcu wywołuje metodę update_analog_timer,
        aby rozpocząć aktualizację czasu.
        """
        self.canvas_size = 150
        self.x = self.canvas_size / 2
        self.y = self.canvas_size / 2
        self.stickLength = 50
        self.stickLengths = [self.stickLength * 0.7, self.stickLength * 0.9, self.stickLength]
        self.stickWidth = 5
        self.stickWidths = [self.stickWidth, self.stickWidth * 0.8, self.stickWidth * 0.5]
        self.create_clock_canvas()
        self.create_clock_face()
        self.create_sticks()
        self.update_analog_timer()
    
    def create_clock_canvas(self):
        """
        Tworzy płótno dla zegara analogowego. Ustawia wysokość, szerokość i kolor tła płótna, a następnie dodaje płótno
        do ramki.
        """
        self.clockCanvas = tk.Canvas(self, height=self.canvas_size, width=self.canvas_size, background="white")
        self.clockCanvas.pack(pady=10)
    
    def create_clock_face(self):
        """
        Tworzy tarczę zegara analogowego. Próbuje załadować obraz tarczy zegara z pliku, a jeśli obraz nie zostanie
        znaleziony, wyświetla komunikat o błędzie na płótnie.
        """
        try:
            self.clockFaceImg = tk.PhotoImage(file=main_frame.image_path)
            self.clockCanvas.create_image(self.x, self.y, image=self.clockFaceImg)   
        except tk.TclError as e:
            print(f"Error loading image: {e}")
            self.clockCanvas.create_text(self.x, self.y, text="Image not found", fill="red")     
    
    def create_sticks(self):
        """
        Tworzy wskazówki zegara analogowego. Tworzy trzy wskazówki (godzinową, minutową i sekundową) o odpowiednich
        długościach i szerokościach, a następnie dodaje je do płótna.
        """
        self.sticks = []
        for i in range(3):
            stick=self.clockCanvas.create_line(self.x, self.y,
                                          self.x + self.stickLengths[i],
                                          self.y + self.stickLengths[i],
                                          width = self.stickWidths[i], 
                                          fill='black')
            self.sticks.append(stick)     

    def update_analog_timer(self):
        """
        Aktualizuje czas na zegarze analogowym co sekundę, przeliczając pozycje wskazówek. Pobiera bieżący czas lokalny,
        przelicza godzinę na format 12-godzinny i mnoży przez 5, aby uzyskać odpowiednią pozycję wskazówki godzinowej.
        Następnie oblicza nowe współrzędne x i y dla każdej wskazówki za pomocą trygonometrii i aktualizuje pozycje
        wskazówek na płótnie. Na końcu ustawia wywołanie tej samej metody po upływie jednej sekundy.
        """
        now=localtime() # Get the current local time
        t = strptime(str(now.tm_hour), "%H") # Get the current hour
        hour = int(strftime( "%I", t ))*5 # Convert the hour to a 12-hour format and multiply by 5
        now=(hour,now.tm_min,now.tm_sec) # Update the tuple to include hour, minute, and second
        
        # Loop over each of the (hour, minute, second) values
        for n, i in enumerate(now):
            x,y=self.clockCanvas.coords(self.sticks[n])[0:2] # Get the current coordinates of each stick
            cr=[x,y] # Start with the current coordinates of the stick (the center of the clock)
            
            # Calculate the new x and y coordinates for each clock hand using trigonometry
            cr.append(self.stickLengths[n]*math.cos(math.radians(i*6)-math.radians(90))+self.x)
            cr.append(self.stickLengths[n]*math.sin(math.radians(i*6)-math.radians(90))+self.y)
            self.clockCanvas.coords(self.sticks[n], tuple(cr))
            
        self.clockCanvas.after(1000, self.update_analog_timer) # Update the position of the stick (clock hand) on the canvas


class MenuBar(tk.Menu):
    def __init__(self, parent):
        """
        Inicjalizuje pasek menu, tworzy menu opcji i menu pomocy oraz ustawia aktywną skórkę. Dodaje menu do okna głównego
        i ustawia aktywną skórkę na pusty ciąg znaków.
        """
        super().__init__(parent)
        self.parent = parent
        
        self.create_options_menu()
        self.create_help_menu()
        
        self.parent.config(menu=self)
        
        self.active_skin = ""

    def create_options_menu(self):
        """
        Tworzy menu opcji, które zawiera podmenu do zmiany skórki, zmiany typu zegara oraz opcję zamknięcia aplikacji.
        Tworzy podmenu do zmiany skórki z trzema opcjami (White, Sky, Dark) oraz podmenu do zmiany typu zegara z dwoma
        opcjami (Analog clock, Digital clock). Dodaje podmenu do menu opcji, a następnie dodaje separator i opcję zamknięcia
        aplikacji.
        """
        options_menu = tk.Menu(self, tearoff=0)
        
        skin_menu = tk.Menu(options_menu, tearoff=0)
        skin_menu.add_command(label="White", command=self.change_skin_white)
        skin_menu.add_command(label="Sky", command=self.change_skin_lightblue)
        skin_menu.add_command(label="Dark", command=self.change_skin_dark)
        
        clock_menu = tk.Menu(options_menu, tearoff=0)
        clock_menu.add_command(label="Analog clock", command=self.change_clock_analog)
        clock_menu.add_command(label="Digital clock", command=self.change_clock_digital)
        
        options_menu.add_cascade(label="Change skin", menu=skin_menu)
        options_menu.add_cascade(label="Change clock", menu=clock_menu)
        options_menu.add_separator()
        options_menu.add_command(label="Exit", command=self.exit_app)
        
        self.add_cascade(label="Options", menu=options_menu)
        
    def change_skin_lightblue(self):
        """
        Zmienia skórkę aplikacji na jasnoniebieską. Ustawia aktywną skórkę na 'sky', zmienia kolor tła okna głównego,
        ramki zegara i ramki kalkulatora na jasnoniebieski, zmienia kolor przycisków kalkulatora na biały, zmienia kolor
        tła pola tekstowego na biały oraz zmienia kolor tła i tekstu zegara cyfrowego na jasnoniebieski i biały.
        Wyświetla komunikat informujący o zmianie skórki.
        """
        self.active_skin = "sky"
        self.parent.configure(bg="lightblue")
        clock_frame.configure(bg="lightblue")
        main_frame.configure(bg="lightblue")
        main_frame.change_button_color("white")
        main_frame.rezultat.configure(bg="white")
        clock_frame.digitalTimer.configure(bg="lightblue", foreground="white")
        messagebox.showinfo("Skin Changed", "The skin has been changed to Sky!")

    def change_skin_white(self):
        """
        Zmienia skórkę aplikacji na białą. Ustawia aktywną skórkę na 'white', zmienia kolor tła okna głównego, ramki zegara
        i ramki kalkulatora na biały, zmienia kolor przycisków kalkulatora na #F5F5F5, zmienia kolor tła pola tekstowego
        na #F5F5F5 oraz zmienia kolor tła i tekstu zegara cyfrowego na biały i czarny. Wyświetla komunikat informujący
        o zmianie skórki.
        """
        self.active_skin = "white"
        self.parent.configure(bg="white")
        clock_frame.configure(bg="white")
        main_frame.configure(bg="white")
        main_frame.change_button_color("#F5F5F5")
        main_frame.rezultat.configure(bg="#F5F5F5")
        clock_frame.digitalTimer.configure(bg="white", foreground="black")
        messagebox.showinfo("Skin Changed", "The skin has been changed to White!")
        
    def change_skin_dark(self):
        """
        Zmienia skórkę aplikacji na ciemną. Ustawia aktywną skórkę na 'dark', zmienia kolor tła okna głównego, ramki zegara
        i ramki kalkulatora na gray10, zmienia kolor przycisków kalkulatora na lightgrey, zmienia kolor tła pola tekstowego
        na lightgrey oraz zmienia kolor tła i tekstu zegara cyfrowego na gray10 i lightgrey. Wyświetla komunikat informujący
        o zmianie skórki.
        """
        self.active_skin = "dark"
        self.parent.configure(bg="gray10")
        clock_frame.configure(bg="gray10")
        main_frame.configure(bg="gray10")
        main_frame.change_button_color("lightgrey")
        main_frame.rezultat.configure(bg="lightgrey")
        clock_frame.digitalTimer.configure(bg="gray10", foreground="lightgrey")
        messagebox.showinfo("Skin Changed", "The skin has been changed to Dark!")
        
    def change_clock_analog(self):
        """
        Zmienia zegar na analogowy. Ustawia typ zegara na 'analog', wywołuje metodę choose_clock ramki zegara, aby
        zainicjalizować zegar analogowy, a następnie wyświetla komunikat informujący o zmianie zegara.
        """
        clock_frame.clock = "analog"
        clock_frame.choose_clock(clock_frame.clock)
        messagebox.showinfo("Clock Changed", "The clock has been changed to analog!")
    
    def change_clock_digital(self):
        """
        Zmienia zegar na cyfrowy. Ustawia typ zegara na 'digital', wywołuje metodę choose_clock ramki zegara, aby
        zainicjalizować zegar cyfrowy, a następnie zmienia kolor tła i tekstu zegara cyfrowego w zależności od aktywnej
        skórki. Wyświetla komunikat informujący o zmianie zegara.
        """
        clock_frame.clock = "digital"
        clock_frame.choose_clock(clock_frame.clock)
        if self.active_skin == "sky":
            clock_frame.digitalTimer.configure(bg="lightblue", foreground="white")
        elif self.active_skin == "dark":
            clock_frame.digitalTimer.configure(bg="gray10", foreground="lightgrey")
        else:
            clock_frame.digitalTimer.configure(bg="white", foreground="black")
        messagebox.showinfo("Clock Changed", "The clock has been changed to digital!")
    
    def exit_app(self):
        """
        Zamyka aplikację. Wywołuje metodę quit okna głównego, aby zakończyć działanie aplikacji.
        """
        self.parent.quit()

    def create_help_menu(self):
        """
        Tworzy menu pomocy z opcją wyświetlenia informacji o aplikacji. Dodaje opcję 'About' do menu pomocy, która
        wywołuje metodę show_about.
        """
        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.add_cascade(label="Help", menu=help_menu)
    
    def show_about(self):
        """
        Wyświetla informacje o aplikacji. Wyświetla okno dialogowe z informacjami o aplikacji, takimi jak jej funkcje
        i autor.
        """
        messagebox.showinfo("About", "This is a simple calculator with a clock. Created with Tkinter. \nYou can choose skin and change type of the clock via options")


if __name__ == "__main__":
    """
    Główna funkcja uruchamiająca aplikację. Tworzy główne okno, ramkę kalkulatora, ramkę zegara oraz pasek menu.
    Ustawia odpowiednie pozycje ramek w oknie głównym i uruchamia główną pętlę aplikacji.
    """
    root = tk.Tk() 
    
    main_frame = MainFrame(root)
    main_frame.pack(side="left", padx=10, anchor="n")

    clock_frame = ClockFrame(root)
    clock_frame.pack(side="right", padx=(10,20), anchor="n")

    MenuBar(root)
        
    root.mainloop()