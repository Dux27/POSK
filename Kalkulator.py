import tkinter as tk
from tkinter import messagebox

from time import *
import math
import os


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
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
        print(f"Key pressed: {event.char}")  # Debugging 
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
        self.rezultat = tk.Text(self, height=2, width=17, font=("Arial Black", 20), bg="#F5F5F5")
        self.rezultat.grid(columnspan=5, pady=10)
        self.wynik = ""

        self.rezultat.focus_set()
        
    def stworz_przyciski(self):
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
        if tekst == "=":
            przycisk = tk.Button(self, text=tekst, command=self.podsumuj, width=12, font=("Arial", 16))
        elif tekst == "C":
            przycisk = tk.Button(self, text=tekst, command=self.clear, width=5, font=("Arial", 16))          
        else:
            przycisk = tk.Button(self, text=tekst, command=lambda znak=tekst: self.zmiana_wyniku(znak), width=5, font=("Arial", 16))
        
        self.buttons.append(przycisk)
        przycisk.grid(row=wiersz, column=kolumna, columnspan=colspan, padx=5, pady=5)
        

    def zmiana_wyniku(self, znak):
        self.wynik += str(znak)
        print(f"Current expression: {self.wynik}")  # Debugging line
        self.rezultat.delete(1.0, "end")
        self.rezultat.insert(1.0, self.wynik)

    def podsumuj(self):
        try:
            expression = self.wynik.strip()

            self.wynik = str(eval(expression))  
            self.rezultat.delete(1.0, "end")  # Clear the Text widget
            self.rezultat.insert(1.0, self.wynik)  # Insert the evaluated result
        except:
            self.clear()
            self.rezultat.insert(1.0, "Error")

    def clear(self):
        self.wynik = ""
        self.rezultat.delete(1.0, "end")        
        
    def change_button_color(self, color: str):
        for b in self.buttons:
            b.configure(bg=color)


class ClockFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.configure(bg="white")
        
        self.clock = ""
        self.choose_clock(self.clock)     
    
    def choose_clock(self, clock: str):
        for widget in self.winfo_children():
            widget.destroy()
        
        if clock == "analog":
            self.inicialize_analog_clock()   
        else:   
            self.inicialize_digital_clock()         
                          
    ### DIGITAL CLOCK FUNCTIONS
    def inicialize_digital_clock(self):
        self.digitalTimer = tk.Label(self, font=('calibri', 30, 'bold'), foreground='black', bg="white")
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
        self.clockCanvas = tk.Canvas(self, height=self.canvas_size, width=self.canvas_size, background="white")
        self.clockCanvas.pack(pady=10)
    
    def create_clock_face(self):
        try:
            self.clockFaceImg = tk.PhotoImage(file=main_frame.image_path)
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


class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self.create_options_menu()
        self.create_help_menu()
        
        self.parent.config(menu=self)
        
        self.active_skin = ""

    def create_options_menu(self):
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
        self.active_skin = "sky"
        self.parent.configure(bg="lightblue")
        clock_frame.configure(bg="lightblue")
        main_frame.configure(bg="lightblue")
        main_frame.change_button_color("white")
        main_frame.rezultat.configure(bg="white")
        clock_frame.digitalTimer.configure(bg="lightblue", foreground="white")
        messagebox.showinfo("Skin Changed", "The skin has been changed to Sky!")

    def change_skin_white(self):
        self.active_skin = "white"
        self.parent.configure(bg="white")
        clock_frame.configure(bg="white")
        main_frame.configure(bg="white")
        main_frame.change_button_color("#F5F5F5")
        main_frame.rezultat.configure(bg="#F5F5F5")
        clock_frame.digitalTimer.configure(bg="white", foreground="black")
        messagebox.showinfo("Skin Changed", "The skin has been changed to White!")
        
    def change_skin_dark(self):
        self.active_skin = "dark"
        self.parent.configure(bg="gray10")
        clock_frame.configure(bg="gray10")
        main_frame.configure(bg="gray10")
        main_frame.change_button_color("lightgrey")
        main_frame.rezultat.configure(bg="lightgrey")
        clock_frame.digitalTimer.configure(bg="gray10", foreground="lightgrey")
        messagebox.showinfo("Skin Changed", "The skin has been changed to Dark!")
        
    def change_clock_analog(self):
        clock_frame.clock = "analog"
        clock_frame.choose_clock(clock_frame.clock)
        messagebox.showinfo("Clock Changed", "The clock has been changed to analog!")
    
    def change_clock_digital(self):
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
        self.parent.quit()

    def create_help_menu(self):
        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.add_cascade(label="Help", menu=help_menu)
    
    def show_about(self):
        messagebox.showinfo("About", "This is a simple calculator with a clock. Created with Tkinter. \nYou can choose skin and change type of the clock via options")


if __name__ == "__main__":
    root = tk.Tk() 
    
    main_frame = MainFrame(root)
    main_frame.pack(side="left", padx=10, anchor="n")

    clock_frame = ClockFrame(root)
    clock_frame.pack(side="right", padx=(10,20), anchor="n")

    MenuBar(root)
        
    root.mainloop()