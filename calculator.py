import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        # Optional: Configure the root window (parent)
        self.parent.title("Main Application")  # Set the window title
        self.parent.geometry("500x300")       # Set the default window size

        # Create a Label
        self.label = tk.Label(self, text="Hello, World!")
        self.label.pack(pady=50)
        
        # Create a Button
        self.button = tk.Button(self, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)
    
    # This method is triggered when the button is clicked
    def on_button_click(self):
        # Change label text after click
        self.label.config(text="You just clicked the button!")
        

if __name__ == "__main__":
    root = tk.Tk() # Create the root window
    MainApplication(root).pack(side="top", fill="both", expand=True) # Create the MainApplication frame and add it to the root window
    root.mainloop() # Start the Tkinter event loop