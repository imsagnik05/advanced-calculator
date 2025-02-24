import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DesmosCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Desmos-Inspired Calculator")
        master.geometry("800x600")
        self.history = []
        self.dark_mode = False

        # Set up styling and theme
        self.style = ttk.Style()
        self.apply_theme()

        # Create menu bar
        self.create_menu()

        # Create main frames: one for calculator and one for graphing
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.calc_frame = ttk.Frame(self.main_frame)
        self.calc_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.graph_frame = ttk.Frame(self.main_frame)
        self.graph_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(10, 0))

        # Calculator UI
        self.create_calculator_ui(self.calc_frame)

        # Graphing UI (initially hidden)
        self.create_graph_ui(self.graph_frame)
        self.graph_frame.pack_forget()  # Hide graph frame initially

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Graph/Calculator", command=self.toggle_view)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)

    def create_calculator_ui(self, parent):
        # Greeting
        greeting = ttk.Label(parent, text="Enter your calculation below:", font=("Arial", 16))
        greeting.grid(row=0, column=0, columnspan=5, pady=(0,10))

        # Display entry
        self.display = ttk.Entry(parent, font=("Arial", 18), justify="right")
        self.display.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)
        self.display.focus_set()

        # Buttons configuration (basic + scientific)
        buttons = [
            (2, 0, "7", lambda: self.add_to_display("7")),
            (2, 1, "8", lambda: self.add_to_display("8")),
            (2, 2, "9", lambda: self.add_to_display("9")),
            (2, 3, "/", lambda: self.add_to_display("/")),
            (2, 4, "C", self.clear_display),

            (3, 0, "4", lambda: self.add_to_display("4")),
            (3, 1, "5", lambda: self.add_to_display("5")),
            (3, 2, "6", lambda: self.add_to_display("6")),
            (3, 3, "*", lambda: self.add_to_display("*")),
            (3, 4, "⌫", self.backspace),

            (4, 0, "1", lambda: self.add_to_display("1")),
            (4, 1, "2", lambda: self.add_to_display("2")),
            (4, 2, "3", lambda: self.add_to_display("3")),
            (4, 3, "-", lambda: self.add_to_display("-")),
            (4, 4, "(", lambda: self.add_to_display("(")),

            (5, 0, "0", lambda: self.add_to_display("0")),
            (5, 1, ".", lambda: self.add_to_display(".")),
            (5, 2, "=", self.calculate),
            (5, 3, "+", lambda: self.add_to_display("+")),
            (5, 4, ")", lambda: self.add_to_display(")")),

            # Scientific functions
            (6, 0, "sin", lambda: self.add_to_display("math.sin(")),
            (6, 1, "cos", lambda: self.add_to_display("math.cos(")),
            (6, 2, "tan", lambda: self.add_to_display("math.tan(")),
            (6, 3, "√", lambda: self.add_to_display("math.sqrt(")),
            (6, 4, "log", lambda: self.add_to_display("math.log(")),
        ]

        for (r, c, text, cmd) in buttons:
            btn = ttk.Button(parent, text=text, command=cmd)
            btn.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

        # Configure grid expansion
        for i in range(7):
            parent.rowconfigure(i, weight=1)
        for j in range(5):
            parent.columnconfigure(j, weight=1)

        # Calculation history
        history_label = ttk.Label(parent, text="History:", font=("Arial", 12))
        history_label.grid(row=7, column=0, columnspan=5, pady=(10, 0))
        self.history_area = scrolledtext.ScrolledText(parent, height=5, font=("Arial", 10), state="disabled")
        self.history_area.grid(row=8, column=0, columnspan=5, sticky="nsew", padx=5, pady=(0, 10))

    def create_graph_ui(self, parent):
        # Graphing UI: function input and variable options
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        func_label = ttk.Label(top_frame, text="f(var) =", font=("Arial", 12))
        func_label.pack(side=tk.LEFT, padx=(0,5))
        self.func_entry = ttk.Entry(top_frame, font=("Arial", 14))
        self.func_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        var_label = ttk.Label(top_frame, text="Variable:", font=("Arial", 12))
        var_label.pack(side=tk.LEFT, padx=(10,5))
        self.var_entry = ttk.Entry(top_frame, font=("Arial", 12), width=5)
        self.var_entry.insert(0, "x")
        self.var_entry.pack(side=tk.LEFT)

        range_frame = ttk.Frame(parent)
        range_frame.pack(fill=tk.X, padx=5, pady=5)
        x_min_label = ttk.Label(range_frame, text="Min:", font=("Arial", 12))
        x_min_label.pack(side=tk.LEFT, padx=(0,5))
        self.x_min_entry = ttk.Entry(range_frame, font=("Arial", 12), width=8)
        self.x_min_entry.insert(0, "-10")
        self.x_min_entry.pack(side=tk.LEFT, padx=(0,15))
        x_max_label = ttk.Label(range_frame, text="Max:", font=("Arial", 12))
        x_max_label.pack(side=tk.LEFT, padx=(0,5))
        self.x_max_entry = ttk.Entry(range_frame, font=("Arial", 12), width=8)
        self.x_max_entry.insert(0, "10")
        self.x_max_entry.pack(side=tk.LEFT)

        plot_btn = ttk.Button(parent, text="Plot Function", command=self.plot_function)
        plot_btn.pack(pady=5)

        # Canvas for plotting
        self.canvas_frame = ttk.Frame(parent)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def add_to_display(self, text):
        self.display.insert(tk.END, text)

    def clear_display(self):
        self.display.delete(0, tk.END)

    def backspace(self):
        current = self.display.get()
        if current:
            self.display.delete(len(current)-1, tk.END)

    def calculate(self):
        expression = self.display.get()
        try:
            result = eval(expression, {"__builtins__": None, "math": math, "abs": abs})
            self.history.append(f"{expression} = {result}")
            self.refresh_history()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Check your expression.\nError: {e}")

    def refresh_history(self):
        self.history_area.config(state="normal")
        self.history_area.delete("1.0", tk.END)
        for line in self.history[-10:]:
            self.history_area.insert(tk.END, line + "\n")
        self.history_area.config(state="disabled")

    def toggle_view(self):
        # Toggle between calculator and graphing views
        if self.graph_frame.winfo_ismapped():
            self.graph_frame.pack_forget()
            self.calc_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.calc_frame.pack_forget()
            self.graph_frame.pack(fill=tk.BOTH, expand=True)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.style.theme_use("clam")
            self.master.configure(bg="#2e2e2e")
            self.style.configure("TButton", background="#424242", foreground="white")
            self.style.configure("TEntry", fieldbackground="#424242", foreground="white")
            self.style.configure("TLabel", background="#2e2e2e", foreground="white")
        else:
            self.style.theme_use("default")
            self.master.configure(bg="#f0f0f0")
            self.style.configure("TButton", background="#e0e0e0", foreground="black")
            self.style.configure("TEntry", fieldbackground="white", foreground="black")
            self.style.configure("TLabel", background="#f0f0f0", foreground="black")

    def plot_function(self):
        func_text = self.func_entry.get().strip()
        var_name = self.var_entry.get().strip() or "x"
        try:
            x_min = float(self.x_min_entry.get().strip())
            x_max = float(self.x_max_entry.get().strip())
            if x_min >= x_max:
                raise ValueError("Min must be less than Max.")
        except Exception as err:
            messagebox.showerror("Input Error", f"Invalid range: {err}")
            return

        # Create x values using numpy
        x = np.linspace(x_min, x_max, 400)
        safe_dict = {"math": math, "np": np, var_name: x}
        try:
            y = eval(func_text, {"__builtins__": None}, safe_dict)
        except Exception as err:
            messagebox.showerror("Function Error", f"Error evaluating function:\n{err}")
            return

        # Clear previous plot if any
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        ax.set_title(f"f({var_name}) = {func_text}")
        ax.set_xlabel(var_name)
        ax.set_ylabel(f"f({var_name})")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = DesmosCalculator(root)
    root.mainloop()
