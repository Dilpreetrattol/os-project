import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import os
import time

# --- Simulated Commands Logic ---
def simulate_command(cmd, args):
    if cmd == "echo":
        text = ' '.join(args)
        # Prevent function/class definitions from being echoed
        if text.strip().startswith(("def ", "class ")) or "(): " in text or text.strip().endswith(":"):
            return "Code definitions are not allowed in echo."
        return text
    elif cmd == "ls":
        return "file1.txt\nfile2.txt\ndirectory/"
    elif cmd == "pwd":
        return "/home/user/project"
    elif cmd == "cd":
        if args:
            return f"Changed to directory: {args[0]}"
        return "No directory specified."
    elif cmd == "expr":
        expr_input = ' '.join(args)
        # Prevent function/class definitions from being evaluated
        if expr_input.strip().startswith(("def ", "class ")) or "(): " in expr_input or expr_input.strip().endswith(":"):
            return "Code definitions are not allowed in expr."
        try:
            return f"Result: {eval(expr_input)}"
        except Exception as e:
            return f"Error: {e}"
    elif cmd == "grep":
        return "Simulated grep output..."
    elif cmd == "sort":
        return "alpha\nbravo\ncharlie"
    elif cmd == "chmod":
        return f"Permissions changed for {args[-1]}"
    elif cmd == "ps":
        return "PID TTY          TIME CMD\n1234 pts/0    00:00:00 bash\n5678 pts/0    00:00:00 python"
    elif cmd == "man":
        return f"Manual page for {args[0]} not available in simulation."
    elif cmd == "ping":
        return f"Simulated ping to {args[0]}: 64 bytes from {args[0]}..."
    return "Command not recognized."

# --- Real Command Execution ---
def execute_real_command(full_cmd):
    try:
        result = subprocess.check_output(full_cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output

# --- Thread Simulation Example ---
def thread_task(name, output_box):
    for i in range(3):
        output_box.insert(tk.END, f"Thread {name} running iteration {i+1}\n")
        output_box.update()

# --- GUI Application ---
class LinuxThreadApp:
    # Define COLORS as a class variable
    COLORS = {
        'primary': '#1976D2',      # Blue
        'secondary': '#424242',    # Dark Gray
        'accent': '#2196F3',       # Light Blue
        'background': '#F5F5F5',   # Light Gray
        'text': '#212121',         # Almost Black
        'success': '#4CAF50'       # Green
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Linux Command & Thread Learning Tool")
        self.root.geometry("1000x750")
        self.root.minsize(900, 650)

        # --- Modern Theme ---
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles using the class COLORS
        style.configure('TNotebook', background=self.COLORS['background'])
        style.configure('TFrame', background=self.COLORS['background'])
        
        style.configure('TButton',
                       font=('Segoe UI', 11),
                       padding=12,
                       background=self.COLORS['primary'],
                       foreground='white')
        
        style.configure('Action.TButton',
                       font=('Segoe UI', 12, 'bold'),
                       padding=15,
                       background=self.COLORS['accent'])
        
        style.configure('TLabel',
                       font=('Segoe UI', 11),
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'])
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.COLORS['primary'],
                       background=self.COLORS['background'])
        
        style.configure('Section.TLabel',
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.COLORS['secondary'],
                       background=self.COLORS['background'])

        # Configure hover effects
        style.map('TButton',
                 background=[('active', self.COLORS['accent'])],
                 foreground=[('active', 'white')])

        # --- Main Notebook ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_home_tab()
        self.create_learn_tab()
        self.create_simulate_tab()
        self.create_thread_tab()

        # Add keyboard shortcuts
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<Control-h>', lambda e: self.notebook.select(self.home_tab))
    
    def show_help(self):
        help_text = """
        Keyboard Shortcuts:
        Ctrl + Q: Exit application
        F1: Show this help
        Ctrl + H: Go to home
        
        In Command Simulator:
        Enter: Execute command
        Up/Down: Navigate command history
        """
        messagebox.showinfo("Help", help_text)

    def show_learn_tab(self):
        self.start_frame.forget()
        self.notebook.pack(fill="both", expand=True)
        self.notebook.select(self.learn_tab)

    def show_thread_tab(self):
        self.start_frame.forget()
        self.notebook.pack(fill="both", expand=True)
        self.notebook.select(self.thread_tab)
        # Add Exit button in Thread tab if not already present
        if not hasattr(self, 'exit_thread_btn') or not self.exit_thread_btn.winfo_exists():
            self.exit_thread_btn = ttk.Button(self.thread_tab, text="Exit", command=self.root.quit)
            self.exit_thread_btn.pack(pady=5, side="bottom", anchor="e")

    def show_simulate_tab(self):
        self.start_frame.forget()
        self.notebook.pack(fill="both", expand=True)
        self.notebook.select(self.sim_tab)

    def create_learn_tab(self):
        self.learn_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.learn_tab, text="Basic Linux Commands")

        section = ttk.Frame(self.learn_tab, padding=30)
        section.pack(fill="both", expand=True)

        ttk.Label(section, text="Select a command to learn:", style='Section.TLabel').pack(anchor="w", pady=(0, 15))
        self.learn_commands = ["echo", "ls", "pwd", "cd", "expr", "grep", "sort", "chmod", "ps", "man", "ping"]
        self.learn_cmd_var = tk.StringVar(value=self.learn_commands[0])
        cmd_menu = ttk.Combobox(section, textvariable=self.learn_cmd_var, values=self.learn_commands, state="readonly", width=22, font=('Segoe UI', 13))
        cmd_menu.pack(anchor="w", pady=(0, 20))
        cmd_menu.focus_set()

        self.learn_info = ttk.Label(section, text="", foreground="#283593", wraplength=850, justify="left", font=('Segoe UI', 13))
        self.learn_info.pack(anchor="w", pady=(0, 20))

        def update_learn_info(event=None):
            cmd = self.learn_cmd_var.get()
            info = {
                "echo": (
                    "echo [text]\n"
                    "Description:\n"
                    "  Prints the text or variables you provide to the standard output (the screen).\n"
                    "  Commonly used in shell scripts and for displaying messages.\n"
                    "Example:\n"
                    "  echo Hello World\n"
                    "  Output: Hello World"
                ),
                "ls": (
                    "ls [directory]\n"
                    "Description:\n"
                    "  Lists files and directories in the specified directory. If no directory is given, it lists the current directory.\n"
                    "  Common options: -l (long format), -a (show hidden files).\n"
                    "Example:\n"
                    "  ls /home/user\n"
                    "  Output: file1.txt  file2.txt  directory/"
                ),
                "pwd": (
                    "pwd\n"
                    "Description:\n"
                    "  Prints the current working directory (the folder you are in).\n"
                    "Example:\n"
                    "  pwd\n"
                    "  Output: /home/user/project"
                ),
                "cd": (
                    "cd [directory]\n"
                    "Description:\n"
                    "  Changes the current working directory to the specified one.\n"
                    "  Use cd .. to go up one directory.\n"
                    "Example:\n"
                    "  cd Documents\n"
                    "  Output: (changes to Documents folder)"
                ),
                "expr": (
                    "expr [expression]\n"
                    "Description:\n"
                    "  Evaluates arithmetic expressions and prints the result.\n"
                    "  Useful for simple math in shell scripts.\n"
                    "Example:\n"
                    "  expr 2 + 2\n"
                    "  Output: 4"
                ),
                "grep": (
                    "grep [pattern] [file]\n"
                    "Description:\n"
                    "  Searches for lines matching a pattern in a file or input.\n"
                    "  Useful for finding text in files.\n"
                    "Example:\n"
                    "  grep hello file.txt\n"
                    "  Output: (lines containing 'hello')"
                ),
                "sort": (
                    "sort [file]\n"
                    "Description:\n"
                    "  Sorts the lines of a file alphabetically or numerically.\n"
                    "Example:\n"
                    "  sort names.txt\n"
                    "  Output: (sorted lines of names.txt)"
                ),
                "chmod": (
                    "chmod [permissions] [file]\n"
                    "Description:\n"
                    "  Changes the permissions of a file or directory.\n"
                    "  Permissions can be set numerically (e.g., 755) or symbolically (e.g., u+x).\n"
                    "Example:\n"
                    "  chmod 755 script.sh\n"
                    "  Output: (script.sh is now executable)"
                ),
                "ps": (
                    "ps\n"
                    "Description:\n"
                    "  Shows currently running processes for the current user/session.\n"
                    "  Common options: aux (show all processes).\n"
                    "Example:\n"
                    "  ps\n"
                    "  Output: PID TTY          TIME CMD\n       1234 pts/0    00:00:00 bash"
                ),
                "man": (
                    "man [command]\n"
                    "Description:\n"
                    "  Displays the manual page for a command, showing its usage, options, and examples.\n"
                    "Example:\n"
                    "  man ls\n"
                    "  Output: (manual page for ls)"
                ),
                "ping": (
                    "ping [host]\n"
                    "Description:\n"
                    "  Tests network connectivity to another host by sending ICMP echo requests.\n"
                    "  Useful for checking if a server or website is reachable.\n"
                    "Example:\n"
                    "  ping google.com\n"
                    "  Output: (shows response times from google.com)"
                ),
            }
            self.learn_info.config(text=info.get(cmd, ""))
        cmd_menu.bind("<<ComboboxSelected>>", update_learn_info)
        update_learn_info()

        btn_frame = ttk.Frame(section)
        btn_frame.pack(anchor="e", pady=(10, 0))
        ttk.Button(btn_frame, text="Back", command=lambda: self.notebook.select(self.home_tab), width=12).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Exit", command=self.root.quit, width=12).pack(side="left", padx=8)

    def create_simulate_tab(self):
        self.sim_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sim_tab, text="Simulate Commands")

        section = ttk.Frame(self.sim_tab, padding=30)
        section.pack(fill="both", expand=True)

        ttk.Label(section, text="Type a Linux command below (e.g., ls, echo hello):", style='Section.TLabel').pack(anchor="w", pady=(0, 15))
        self.input_entry = ttk.Entry(
            section,
            width=70,
            font=('Segoe UI', 12),
            style='Command.TEntry'
        )
        self.input_entry.pack(pady=(0, 15), fill="x")
        self.input_entry.focus_set()

        ttk.Button(section, text="Simulate", command=self.run_command, width=16).pack(anchor="w", pady=(0, 20))

        output_frame = ttk.Frame(section)
        output_frame.pack(fill="both", expand=True)
        self.output_text = tk.Text(
            output_frame,
            height=18,
            wrap="word",
            font=('Cascadia Code', 12),  # Modern monospace font
            bg='#FAFAFA',
            fg='#212121',
            padx=10,
            pady=10,
            borderwidth=1,
            relief="solid"
        )

        self.output_text.pack(side="left", fill="both", expand=True)
        output_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        output_scroll.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=output_scroll.set)

        # Add placeholder text
        self.input_entry.insert(0, "Type your command here...")
        self.input_entry.bind('<FocusIn>', lambda e: self.on_entry_click())
        self.input_entry.bind('<FocusOut>', lambda e: self.on_focus_out())

        btn_frame = ttk.Frame(section)
        btn_frame.pack(anchor="e", pady=(10, 0))
        ttk.Button(btn_frame, text="Back", command=lambda: self.notebook.select(self.home_tab), width=12).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Exit", command=self.root.quit, width=12).pack(side="left", padx=8)

    def create_thread_tab(self):
        self.thread_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.thread_tab, text="Thread Concepts")

        section = ttk.Frame(self.thread_tab, padding=30)
        section.pack(fill="both", expand=True)

        # Add thread state visualization
        self.thread_state = ttk.Label(
            section,
            text="Thread Status: Idle",
            font=('Segoe UI', 12, 'bold'),
            foreground=self.COLORS['primary']  # Use self.COLORS instead of COLORS
        )
        self.thread_state.pack(pady=(0, 10))

        # Thread type selection with improved visuals
        ttk.Label(section, text="Select Thread Type", style='Section.TLabel').pack(pady=(0, 15))

        btn_frame = ttk.Frame(section)
        btn_frame.pack(pady=10)

        thread_buttons = [
            ("User Thread 👤", self.show_user_thread),
            ("Kernel Thread 🔧", self.show_kernel_thread),
            ("Daemon Thread 👻", self.show_daemon_thread)
        ]

        for text, command in thread_buttons:
            btn = ttk.Button(btn_frame, text=text, command=command, width=20)
            btn.pack(side="left", padx=10)
            self.show_tooltip(btn, f"Click to learn about {text.split()[0]} {text.split()[1]}")

        # Add interactive demo section
        demo_frame = ttk.LabelFrame(section, text="Thread Demo", padding=10)
        demo_frame.pack(fill="x", pady=10)

        demo_controls = ttk.Frame(demo_frame)
        demo_controls.pack(fill="x")

        self.thread_count = ttk.Spinbox(
            demo_controls,
            from_=1,
            to=5,
            width=5,
            font=('Segoe UI', 11)
        )
        self.thread_count.set(2)
        self.thread_count.pack(side="left", padx=(0, 10))

        ttk.Button(
            demo_controls,
            text="Run Demo",
            command=self.run_thread_demo,
            style='Action.TButton'
        ).pack(side="left", padx=5)

        # Thread output display
        self.demo_output = tk.Text(
            demo_frame,
            height=6,
            wrap="word",
            font=('Cascadia Code', 11),
            bg='#f8f9fa',
            state='disabled'
        )
        self.demo_output.pack(fill="x", pady=(10, 0))

        # Thread explanation area
        output_frame = ttk.Frame(section)
        output_frame.pack(fill="both", expand=True, pady=(15, 5))

        self.thread_explanation = tk.Text(
            output_frame,
            height=8,
            wrap="word",
            state="disabled",
            font=('Consolas', 12),
            bg="#f5f5f5"
        )
        self.thread_explanation.pack(side="left", fill="both", expand=True)
        thread_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.thread_explanation.yview)
        thread_scroll.pack(side="right", fill="y")
        self.thread_explanation.config(yscrollcommand=thread_scroll.set)

        btn_frame2 = ttk.Frame(section)
        btn_frame2.pack(anchor="e", pady=(10, 0))
        ttk.Button(btn_frame2, text="Back", command=lambda: self.notebook.select(self.home_tab), width=12).pack(side="left", padx=8)
        ttk.Button(btn_frame2, text="Exit", command=self.root.quit, width=12).pack(side="left", padx=8)

    def run_thread_demo(self):
        """Run an interactive thread demonstration"""
        try:
            num_threads = int(self.thread_count.get())
            self.demo_output.config(state='normal')
            self.demo_output.delete(1.0, tk.END)
            self.demo_output.config(state='disabled')
            
            self.thread_state.config(text="Thread Status: Running")
            
            for i in range(num_threads):
                thread = threading.Thread(
                    target=self._demo_thread_task,
                    args=(f"Thread-{i+1}",),
                    daemon=True
                )
                thread.start()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of threads (1-5)")

    def _demo_thread_task(self, name):
        """Simulated thread task with visual feedback"""
        for i in range(3):
            self.demo_output.config(state='normal')
            self.demo_output.insert(tk.END, f"📍 {name} - Step {i+1}\n")
            self.demo_output.see(tk.END)
            self.demo_output.config(state='disabled')
            self.root.update_idletasks()
            time.sleep(0.5)
            
        if name == f"Thread-{int(self.thread_count.get())}":
            self.thread_state.config(text="Thread Status: Completed")

    def show_user_thread(self):
        explanation = (
            "User Thread:\n"
            "Managed by user-level libraries, not the OS kernel.\n"
            "Example: Python's threading.Thread (non-daemon).\n\n"
            "Implementation Example:\n"
            "import threading\n"
            "def task():\n"
            "    print('User thread running')\n"
            "t = threading.Thread(target=task)\n"
            "t.start()"
        )
        self.thread_explanation.config(state="normal")
        self.thread_explanation.delete("1.0", tk.END)
        self.thread_explanation.insert(tk.END, explanation)
        self.thread_explanation.config(state="disabled")

    def show_kernel_thread(self):
        explanation = (
            "Kernel Thread:\n"
            "Managed directly by the OS kernel. In Python, threading.Thread is mapped to kernel threads by the OS.\n"
            "Example: Python's threading.Thread (all threads are kernel threads in CPython).\n\n"
            "Implementation Example:\n"
            "import threading\n"
            "def task():\n"
            "    print('Kernel thread running')\n"
            "t = threading.Thread(target=task)\n"
            "t.start()"
        )
        self.thread_explanation.config(state="normal")
        self.thread_explanation.delete("1.0", tk.END)
        self.thread_explanation.insert(tk.END, explanation)
        self.thread_explanation.config(state="disabled")

    def show_daemon_thread(self):
        explanation = (
            "Daemon Thread:\n"
            "Background thread that exits when the main program exits.\n"
            "Example: Set daemon=True in threading.Thread.\n\n"
            "Implementation Example:\n"
            "import threading\n"
            "def task():\n"
            "    print('Daemon thread running')\n"
            "t = threading.Thread(target=task, daemon=True)\n"
            "t.start()"
        )
        self.thread_explanation.config(state="normal")
        self.thread_explanation.delete("1.0", tk.END)
        self.thread_explanation.insert(tk.END, explanation)
        self.thread_explanation.config(state="disabled")

    def run_command(self):
        user_input = self.input_entry.get().strip()
        self.output_text.delete("1.0", tk.END)
        if not user_input:
            self.output_text.insert(tk.END, "Please enter a command.")
            return
        parts = user_input.split()
        cmd = parts[0]
        args = parts[1:]
        result = simulate_command(cmd, args)
        self.output_text.insert(tk.END, result)
        self.input_entry.delete(0, tk.END)

    def create_home_tab(self):
        self.home_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.home_tab, text="Home")

        # Create main container with padding
        section = ttk.Frame(self.home_tab, padding=40)
        section.pack(expand=True, fill="both")

        # Welcome message with logo/icon space
        header_frame = ttk.Frame(section)
        header_frame.pack(fill="x", pady=(20, 50))
        
        ttk.Label(header_frame,
                 text="🐧 Linux Learning Hub",
                 style='Header.TLabel').pack(anchor="center")
        
        ttk.Label(header_frame,
                 text="Interactive learning tool for Linux commands and threading concepts",
                 style='TLabel').pack(anchor="center", pady=(10, 0))

        # Button container
        btn_frame = ttk.Frame(section)
        btn_frame.pack(expand=True)

        # Modern button styling
        btn_style = {
            'width': 35,
            'style': 'Action.TButton',
            'padding': 15
        }

        # Main navigation buttons
        ttk.Button(btn_frame,
                  text="📚 Learn Basic Linux Commands",
                  command=lambda: self.notebook.select(self.learn_tab),
                  **btn_style).pack(pady=12)
        
        ttk.Button(btn_frame,
                  text="💻 Simulate Commands",
                  command=lambda: self.notebook.select(self.sim_tab),
                  **btn_style).pack(pady=12)
        
        ttk.Button(btn_frame,
                  text="🧵 Explore Thread Concepts",
                  command=lambda: self.notebook.select(self.thread_tab),
                  **btn_style).pack(pady=12)

        # Footer with exit button
        footer_frame = ttk.Frame(section)
        footer_frame.pack(fill="x", pady=(50, 20))
        
        ttk.Button(footer_frame,
                  text="Exit Application",
                  command=self.root.quit,
                  width=20).pack(anchor="e")

    def on_entry_click(self):
        """Clear placeholder text on entry field click"""
        if self.input_entry.get() == "Type your command here...":
            self.input_entry.delete(0, tk.END)
            self.input_entry.config(foreground='black')

    def on_focus_out(self):
        """Restore placeholder text if entry is empty"""
        if not self.input_entry.get():
            self.input_entry.insert(0, "Type your command here...")
            self.input_entry.config(foreground='gray')

    def show_tooltip(self, widget, text):
        """Show tooltip on hover"""
        def on_enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
            
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(self.tooltip, text=text, justify='left',
                            background="#ffffe0", relief='solid', borderwidth=1,
                            font=("Segoe UI", 9))
            label.pack()

        def on_leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()

        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

# --- Run the Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LinuxThreadApp(root)
    root.mainloop()