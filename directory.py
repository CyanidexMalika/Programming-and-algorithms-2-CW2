import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import requests
import threading
import json
import os
import time
 
def browse_wordlist():
    wordlist_file = filedialog.askopenfilename(title="Select Directory Wordlist")
    if wordlist_file:
        wordlist_entry.delete(0, tk.END)
        wordlist_entry.insert(0, wordlist_file)
 
def stop_checking():
    global stop_flag
    stop_flag = True
 
def clear_results():
    global directories, elapsed_time
    directories = []
    elapsed_time = 0
    progress_bar['value'] = 0
    result_text.set("")
    status_var.set("Ready")
 
def save_history():
    global directories
    history_data = {'url': url_entry.get(), 'directories': directories}
    with open('scan_history.json', 'w') as history_file:
        json.dump(history_data, history_file)
    result_text.set(result_text.get() + "Scan history saved.\n")
 
def load_history():
    global directories
    try:
        with open('scan_history.json', 'r') as history_file:
            history_data = json.load(history_file)
        url_entry.delete(0, tk.END)
        url_entry.insert(0, history_data['url'])
        directories = history_data['directories']
        result_text.set(result_text.get() + "Scan history loaded.\n")
    except FileNotFoundError:
        result_text.set(result_text.get() + "No scan history found.\n")
 
def enumerate_directories():
    global stop_flag, directories, elapsed_time
    stop_flag = False
    directories = []
    elapsed_time = 0
 
    url = url_entry.get()
    wordlist_file = wordlist_entry.get()
 
    if not url:
        result_text.set("Please enter a URL")
        return
    if not wordlist_file:
        result_text.set("Please select a wordlist file")
        return
 
    try:
        with open(wordlist_file, 'r') as f:
            wordlist = f.read().splitlines()
 
        progress_bar['maximum'] = len(wordlist)
        result_text.set("Enumerating directories...")
        start_time = time.time()
 
        def worker(word):
            global directories
            full_url = requests.compat.urljoin(url, word)
            try:
                headers = {'User-Agent': user_agent.get()}
                response = requests.head(full_url, headers=headers, timeout=request_timeout.get())
                progress_text = f"Checking: {full_url} - Status: {response.status_code}"
                if 200 <= response.status_code < 400:
                    response_size = len(response.content) if response.content else 0
                    progress_text += f" - Exists - Size: {response_size} bytes\n"
                    result_text.set(result_text.get() + progress_text)
                    directories.append({'url': full_url, 'status_code': response.status_code, 'size': response_size})
            except Exception as e:
                result_text.set(result_text.get() + f"Error: {e}\n")
            finally:
                progress_bar['value'] += 1
 
        for word in wordlist:
            if stop_flag:
                result_text.set("Enumeration stopped.")
                break
            threading.Thread(target=worker, args=(word,), daemon=True).start()
 
        elapsed_time = time.time() - start_time
        status_var.set(f"Enumeration completed in {elapsed_time:.2f} seconds")
 
    except Exception as e:
        result_text.set(f"Error: {e}")
 
def exit_application():
    if tk.messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.quit()
 
# Create main window
root = tk.Tk()
root.title("Directory Enumeration Tool")
 
# Create a style to use the 'clam' theme for a modern look
style = ttk.Style(root)
style.theme_use("clam")
 
# Main Frame
main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.grid(row=0, column=0, sticky="nsew")
 
# URL entry
url_label = ttk.Label(main_frame, text="Enter URL:")
url_label.grid(row=0, column=0, pady=5, sticky="w")
url_entry = ttk.Entry(main_frame, width=40)
url_entry.grid(row=0, column=1, pady=5, sticky="w")
 
# Wordlist selection
wordlist_label = ttk.Label(main_frame, text="Select Wordlist File:")
wordlist_label.grid(row=1, column=0, pady=5, sticky="w")
wordlist_entry = ttk.Entry(main_frame, width=30)
wordlist_entry.grid(row=1, column=1, pady=5, sticky="w")
browse_button = ttk.Button(main_frame, text="Browse", command=browse_wordlist)
browse_button.grid(row=1, column=2, pady=5, sticky="w")
 
# Request timeout entry
timeout_label = ttk.Label(main_frame, text="Request Timeout (seconds):")
timeout_label.grid(row=2, column=0, pady=5, sticky="w")
request_timeout = tk.DoubleVar()
timeout_entry = ttk.Entry(main_frame, textvariable=request_timeout, width=10)
timeout_entry.grid(row=2, column=1, pady=5, sticky="w")
request_timeout.set(5)  # Default timeout value
 
# User-Agent entry
user_agent_label = ttk.Label(main_frame, text="Custom User-Agent:")
user_agent_label.grid(row=3, column=0, pady=5, sticky="w")
user_agent = tk.StringVar()
user_agent_entry = ttk.Entry(main_frame, textvariable=user_agent, width=30)
user_agent_entry.grid(row=3, column=1, pady=5, sticky="w")
user_agent.set("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
 
# Enumerate button
enumerate_button = ttk.Button(main_frame, text="Enumerate Directories", command=enumerate_directories)
enumerate_button.grid(row=4, column=0, columnspan=3, pady=10, sticky="we")
 
# Stop button
stop_button = ttk.Button(main_frame, text="Stop Checking", command=stop_checking)
stop_button.grid(row=5, column=0, columnspan=3, pady=5, sticky="we")
 
# Save and load history buttons
save_history_button = ttk.Button(main_frame, text="Save Scan History", command=save_history)
save_history_button.grid(row=6, column=0, pady=5, sticky="we")
load_history_button = ttk.Button(main_frame, text="Load Scan History", command=load_history)
load_history_button.grid(row=6, column=1, pady=5, sticky="we")
 
# Clear results button
clear_results_button = ttk.Button(main_frame, text="Clear Results", command=clear_results)
clear_results_button.grid(row=6, column=2, pady=5, sticky="we")
 
# Progress bar
progress_bar = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
progress_bar.grid(row=7, column=0, columnspan=3, pady=10, sticky="we")
 
# Result label
result_text = tk.StringVar()
result_label = ttk.Label(main_frame, textvariable=result_text, wraplength=500, justify="left")
result_label.grid(row=8, column=0, columnspan=3, pady=10, sticky="we")
 
# Status bar
status_var = tk.StringVar()
status_bar = ttk.Label(main_frame, textvariable=status_var, relief="sunken", anchor="w")
status_bar.grid(row=9, column=0, columnspan=3, pady=5, sticky="we")
 
# Exit button
exit_button = ttk.Button(main_frame, text="Exit", command=exit_application)
exit_button.grid(row=10, column=0, columnspan=3, pady=5, sticky="we")
 
# Set weights for resizing
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
 
# Run the Tkinter event loop
root.mainloop()
