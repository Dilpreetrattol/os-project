import tkinter as tk
from tkinter import ttk

# Main data
linux_commands = {
    "Internal vs External": "Internal: Built into shell (cd, pwd, echo)\n"
                            "External: Separate executables (ls, grep, sort)",
    "Pipelining": "Sends output of one command as input to another\n"
                  "Usage: command1 | command2\nExample: ls | sort",
    "Combining Commands": "Semicolon (;): Run sequentially\nAND (&&): Run if first succeeds\n"
                          "Example: cd Documents && ls",
    "File Permissions": "chmod: Change file permissions\nExample: chmod 755 file.txt"
}

thread_concepts = {
    "User-Level Threads": "- Managed by user-level libraries\n- Fast context switching\n"
                          "- Kernel is unaware of threads",
    "Kernel-Level Threads": "- Managed by the OS kernel\n- More overhead, better system integration\n"
                            "- Each thread is treated independently by the OS",
    "User vs Kernel Threads": "- User threads: fast, low overhead, but no parallelism\n"
                              "- Kernel threads: true concurrency, but more overhead"
}

# GUI class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Linux & Threads Learner")
        self.geometry("600x400")
        self.configure(bg="#f0f0f0")

        self.container = ttk.Frame(self)
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        self.show_main_menu()

    def clear_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_frame()
        ttk.Label(self.container, text="Explore Topics", font=("Helvetica", 18)).pack(pady=10)

        ttk.Button(self.container, text="Linux Commands", width=25,
                   command=self.show_linux_menu).pack(pady=5)
        ttk.Button(self.container, text="Thread Concepts", width=25,
                   command=self.show_threads_menu).pack(pady=5)
        ttk.Button(self.container, text="Exit", width=25, command=self.quit).pack(pady=20)

    def show_linux_menu(self):
        self.clear_frame()
        ttk.Label(self.container, text="Linux Commands", font=("Helvetica", 16)).pack(pady=10)

        for topic in linux_commands:
            ttk.Button(self.container, text=topic, width=40,
                       command=lambda t=topic: self.show_content(t, linux_commands[t])).pack(pady=2)

        ttk.Button(self.container, text="Back", command=self.show_main_menu).pack(pady=10)

    def show_threads_menu(self):
        self.clear_frame()
        ttk.Label(self.container, text="Thread Concepts", font=("Helvetica", 16)).pack(pady=10)

        for topic in thread_concepts:
            ttk.Button(self.container, text=topic, width=40,
                       command=lambda t=topic: self.show_content(t, thread_concepts[t])).pack(pady=2)

        ttk.Button(self.container, text="Back", command=self.show_main_menu).pack(pady=10)

    def show_content(self, title, content):
        self.clear_frame()
        ttk.Label(self.container, text=title, font=("Helvetica", 16)).pack(pady=10)

        text_widget = tk.Text(self.container, wrap="word", height=10)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled", font=("Courier", 12))
        text_widget.pack(expand=True, fill="both", padx=10, pady=10)

        ttk.Button(self.container, text="Back", command=self.show_main_menu).pack(pady=10)

# Run the app
if __name__ == "__main__":
    app = App()
    app.mainloop()
