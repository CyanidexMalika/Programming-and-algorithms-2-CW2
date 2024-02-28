import tkinter as tk
from tkinter import Menu, messagebox
import subprocess

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Enumeration Tools")
        self.root.geometry("400x200")

        # Menu Bar
        menubar = Menu(root)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.exit_application)
        menubar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menubar)

        # Title Label
        title_label = tk.Label(root, text="Welcome to Enumeration with Cyanide", font=("Helvetica", 16, "bold"), fg="cyan")
        title_label.pack(pady=10)

        # Labelling
        subtitle_label = tk.Label(root, text="Choose Enumeration Tool:", font=("Helvetica", 14))
        subtitle_label.pack()

        # SSH Enumeration Button
        ssh_button = tk.Button(root, text="SSH Enumeration", command=self.open_ssh_tool, font=("Helvetica", 12))
        ssh_button.pack(pady=10)

        # Directory Enumeration Button
        directory_button = tk.Button(root, text="Directory Enumeration", command=self.open_directory_tool, font=("Helvetica", 12))
        directory_button.pack(pady=10)

        # Menu Panel Decoration
        self.menu_panel = tk.Label(root, bg="black", fg="white", height=1, width=400)
        self.menu_panel.pack(side="top", fill="x")
        menu_label = tk.Label(self.menu_panel, text="File", bg="black", fg="white", font=("Helvetica", 12, "bold"))
        menu_label.pack(side="left", padx=10, pady=5)

    # Hide the main GUI panel after clicking button both ssh and directory
    
    def open_ssh_tool(self):
        self.root.withdraw()  
        subprocess.Popen(["python", "ssh.py"], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)

    def open_directory_tool(self):
        self.root.withdraw()  
        subprocess.Popen(["python", "directory.py"], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)

    def exit_application(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
