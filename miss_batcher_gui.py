
import os
import tkinter as tk
from tkinter import messagebox
import subprocess

# Path where batch files are stored
BATCH_DIR = os.path.join(os.path.expanduser("~"), "MissBatcher", "scripts")

def run_batch(filename):
    filepath = os.path.join(BATCH_DIR, filename)
    if os.path.exists(filepath):
        subprocess.run(['cmd', '/c', filepath], shell=True)
    else:
        messagebox.showerror("Oops!", f"File not found:\n{filepath}")

def panic_exit():
    messagebox.showinfo("Don't worry 😌", "No files were harmed.\nYour chaotic PC is safe!\n\nSee you next time 🐢")
    root.destroy()

def explain_batch():
    messagebox.showinfo("What's a batch file?", 
        "A batch file (or 'batchje') is like a list of computer instructions.\n"
        "Instead of clicking 10 times, 1 click does it all for you!\n\n"
        "Miss. Batcher uses batchjes to help clean up and organize your PC.\n"
        "Safely. With backups. Always. 🙂"
    )

root = tk.Tk()
root.title("Miss. Batcher 🧹 - Your PC Assistant")
root.geometry("450x400")
root.config(bg="#f0f8ff")

tk.Label(root, text="Welcome to Miss. Batcher 💻", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)
tk.Label(root, text="Batching made easy, safe, and maybe a little fun 😊", bg="#f0f8ff").pack(pady=5)

tk.Button(root, text="🧽 Clean My Desktop", width=30, command=lambda: run_batch("clean_desktop.bat")).pack(pady=5)
tk.Button(root, text="📁 Sort My Downloads", width=30, command=lambda: run_batch("sort_downloads.bat")).pack(pady=5)
tk.Button(root, text="🔍 Find Big Files", width=30, command=lambda: run_batch("find_large_files.bat")).pack(pady=5)

tk.Label(root, text="----------------------------", bg="#f0f8ff").pack(pady=5)

tk.Button(root, text="❓ What is a batch file?", width=30, command=explain_batch, bg="#d0eaff").pack(pady=5)
tk.Button(root, text="🏃 Too much for me! Exit now", width=30, command=panic_exit, bg="#ffcccc").pack(pady=5)

tk.Label(root, text="Miss. Batcher v1.0 by Brigitte & ChatGPT", font=("Helvetica", 8), bg="#f0f8ff").pack(side="bottom", pady=10)

root.mainloop()
