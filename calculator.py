import tkinter as tk
from tkinter import ttk

from time import *
import math

class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.parent.title("Kalkulator")  
        self.parent.geometry("500x300")  
        
        self.wynik = ""
        
        self.rezultat = tk.Text(self, height=2, width=18, font=("Arial Black", 20))
        self.rezultat.grid(columnspan=5)
        
        self.stworz_przyciski()
        
        self.inicialize_digital_clock()
        self.inicialize_analog_clock()

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

    
    ### DIGITAL CLOCK FUNCTIONS
    def inicialize_digital_clock(self):
        self.digitalTimer = ttk.Label(self, font=('calibri', 30, 'bold'), foreground='black')
        self.digitalTimer.pack(side="top", anchor='center')
        self.update_digital_timer()
    
    def update_digital_timer(self):
        string = strftime('%H:%M:%S')  
        self.digitalTimer.config(text=string)   
        self.digitalTimer.after(1000, self.update_digital_timer)
   
   
    ### ANALOG CLOCK FUNCTIONS
    def inicialize_analog_clock(self):
        self.x = 320    
        self.y = 320
        self.stickLength = 50
        self.stickLengths = [self.stickLength * 0.7, self.stickLength * 0.9, self.stickLength]
        self.stickWidth = 5
        self.stickWidths = [self.stickWidth, self.stickWidth * 0.8, self.stickWidth * 0.5]
        self.create_clock_canvas()
        self.create_clock_face()
        self.create_sticks()
        self.update_analog_timer()
    
    def create_clock_canvas(self):
        self.clockCanvas = tk.Canvas(self)
        self.clockCanvas.pack(expand=True, fill='both')
    
    def create_clock_face(self):
        try:
            self.clockFaceImg = tk.PhotoImage(file="img/clock150.png")
            self.clockCanvas.create_image(320, 320, image=self.clockFaceImg)   
        except tk.TclError as e:
            print(f"Error loading image: {e}")
            self.clockCanvas.create_text(150, 150, text="Image not found", fill="red")     
    
    def create_sticks(self):
        self.sticks = []
        for i in range(3):
            stick=self.clockCanvas.create_line(self.x, self.y,
                                          self.x + self.stickLengths[i],
                                          self.y + self.stickLengths[i],
                                          width = self.stickWidths[i], 
                                          fill='black')
            self.sticks.append(stick)     

    def update_analog_timer(self):
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


if __name__ == "__main__":
    root = tk.Tk() 
    Main(root).pack(side="top", fill="both", expand=True)
    root.mainloop()