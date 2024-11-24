import tkinter as tk

from time import *
import math


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.parent.title("Kalkulator")  
        self.parent.geometry("520x365")  
        self.parent.resizable(False, False)
        
        self.wynik = ""
        
        self.rezultat = tk.Text(self, height=2, width=17, font=("Arial Black", 20))
        self.rezultat.grid(columnspan=5, pady=10)
        
        self.stworz_przyciski()
        
    def stworz_przyciski(self):
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
        if tekst == "=":
            przycisk = tk.Button(self, text=tekst, command=self.podsumuj, width=12, font=("Arial", 16))
        elif tekst == "C":
            przycisk = tk.Button(self, text=tekst, command=self.clear, width=5, font=("Arial", 16))          
        else:
            przycisk = tk.Button(self, text=tekst, command=lambda znak=tekst: self.zmiana_wyniku(znak), width=5, font=("Arial", 16))
        
        przycisk.grid(row=wiersz, column=kolumna, columnspan=colspan, padx=5, pady=5)
        

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


class ClockFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.inicialize_analog_clock()        
               
                          
    ### DIGITAL CLOCK FUNCTIONS
    def inicialize_digital_clock(self):
        self.digitalTimer = tk.Label(self, font=('calibri', 30, 'bold'), foreground='black')
        self.digitalTimer.pack(pady=20)
        self.update_digital_timer()
    
    def update_digital_timer(self):
        string = strftime('%H:%M:%S')  
        self.digitalTimer.config(text=string)   
        self.digitalTimer.after(1000, self.update_digital_timer)
   
   
    ### ANALOG CLOCK FUNCTIONS
    def inicialize_analog_clock(self):
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
        self.clockCanvas = tk.Canvas(self, height=self.canvas_size, width=self.canvas_size)
        self.clockCanvas.pack(pady=8)
    
    def create_clock_face(self):
        try:
            self.clockFaceImg = tk.PhotoImage(file="img/clock150.png")
            self.clockCanvas.create_image(self.x, self.y, image=self.clockFaceImg)   
        except tk.TclError as e:
            print(f"Error loading image: {e}")
            self.clockCanvas.create_text(self.x, self.y, text="Image not found", fill="red")     
    
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
    
    main_frame = MainFrame(root)
    main_frame.pack(side="left", padx=10, anchor="n")

    clock_frame = ClockFrame(root)
    clock_frame.pack(side="right", padx=10, anchor="n")
    
    root.mainloop()