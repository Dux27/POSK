import tkinter as tk
from tkinter import filedialog, messagebox

class ProcessorSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Processor")

        # Rejestry procesora
        self.registers = {
            'AX': 0,
            'BX': 0,
            'CX': 0,
            'DX': 0
        }

        # Instrukcje programu
        self.program = []
        self.current_instruction = 0

        # Interfejs użytkownika
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel for program code
        self.left_panel = tk.Frame(self.main_frame)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.program_label = tk.Label(self.left_panel, text="Program", font=("Consolas", 16))
        self.program_label.pack(anchor=tk.W, padx=10, pady=5)
        self.program_text = tk.Text(self.left_panel, height=25, width=60, font=("Consolas", 14))
        self.program_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Right panel for controls and registers
        self.right_panel = tk.Frame(self.main_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Control buttons
        self.controls_frame = tk.Frame(self.right_panel)
        self.controls_frame.pack(fill=tk.X, padx=10, pady=5)

        self.run_button = tk.Button(self.controls_frame, text="Run", command=self.run_program, font=("Consolas", 14))
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.step_button = tk.Button(self.controls_frame, text="Step", command=self.step_program, font=("Consolas", 14))
        self.step_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.controls_frame, text="Reset", command=self.reset_program, font=("Consolas", 14))
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.controls_frame, text="Save Program", command=self.save_program, font=("Consolas", 14))
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = tk.Button(self.controls_frame, text="Load Program", command=self.load_program, font=("Consolas", 14))
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Registers display
        self.registers_label = tk.Label(self.right_panel, text="Registers", font=("Consolas", 16))
        self.registers_label.pack(anchor=tk.W, padx=10, pady=5)
        self.registers_text = tk.Text(self.right_panel, height=15, width=60, font=("Consolas", 14))
        self.registers_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.update_register_display()

    def update_register_display(self):
        self.registers_text.delete(1.0, tk.END)
        for reg, value in self.registers.items():
            font = ("Consolas", 14, "bold") if reg in ['AX', 'BX', 'CX', 'DX'] else ("Consolas", 14)
            self.registers_text.insert(tk.END, f"{reg}: {value:04X}\n", font)

    def parse_instruction(self, instruction):
        parts = instruction.split()
        if len(parts) < 2:
            raise ValueError("Invalid instruction format")
        cmd = parts[0].upper()
        args = parts[1:]
        return cmd, args

    def execute_instruction(self, instruction):
        cmd, args = self.parse_instruction(instruction)

        if cmd == "MOV":
            if args[1].startswith("#"):
                value = int(args[1][1:], 16)
                self.registers[args[0]] = value
            else:
                self.registers[args[0]] = self.registers[args[1]]

        elif cmd == "ADD":
            if args[1].startswith("#"):
                value = int(args[1][1:], 16)
                self.registers[args[0]] += value
            else:
                self.registers[args[0]] += self.registers[args[1]]

        elif cmd == "SUB":
            if args[1].startswith("#"):
                value = int(args[1][1:], 16)
                self.registers[args[0]] -= value
            else:
                self.registers[args[0]] -= self.registers[args[1]]

        else:
            raise ValueError(f"Unknown command: {cmd}")

        # Ensure 16-bit values
        for reg in self.registers:
            self.registers[reg] &= 0xFFFF

    def run_program(self):
        self.program = self.program_text.get(1.0, tk.END).strip().splitlines()
        try:
            for instruction in self.program:
                self.execute_instruction(instruction)
            self.update_register_display()
            messagebox.showinfo("Success", "Program executed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def step_program(self):
        if not self.program:
            self.program = self.program_text.get(1.0, tk.END).strip().splitlines()

        if self.current_instruction < len(self.program):
            try:
                instruction = self.program[self.current_instruction]
                self.execute_instruction(instruction)
                self.current_instruction += 1
                self.update_register_display()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("Info", "Program execution complete.")

    def reset_program(self):
        self.registers = {key: 0 for key in self.registers}
        self.program = []
        self.current_instruction = 0
        self.update_register_display()
        messagebox.showinfo("Reset", "Processor reset successfully.")

    def save_program(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.program_text.get(1.0, tk.END))
            messagebox.showinfo("Saved", "Program saved successfully.")

    def load_program(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.program_text.delete(1.0, tk.END)
                self.program_text.insert(tk.END, file.read())
            messagebox.showinfo("Loaded", "Program loaded successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessorSimulator(root)
    root.mainloop()