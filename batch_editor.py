import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def new_file():
    text_box.delete("1.0", tk.END)

def open_file():
    path = filedialog.askopenfilename(filetypes=[("Batch Files", "*.bat")])
    if path:
        with open(path, "r") as file:
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, file.read())
        root.title(f"Batch Editor - {os.path.basename(path)}")

def save_file():
    path = filedialog.asksaveasfilename(defaultextension=".bat",
                                        filetypes=[("Batch Files", "*.bat")])
    if path:
        with open(path, "w") as file:
            file.write(text_box.get("1.0", tk.END))
        messagebox.showinfo("Saved", "Batch file saved successfully.")

def run_file():
    content = text_box.get("1.0", tk.END)
    temp_path = "temp_run.bat"
    with open(temp_path, "w") as temp:
        temp.write(content)
    subprocess.run(temp_path, shell=True)

# Window setup
root = tk.Tk()
root.title("Batch File Editor")
root.geometry("600x400")

text_box = tk.Text(root, font=("Courier", 12))
text_box.pack(expand=True, fill="both")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open...", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menu.add_command(label="Run", command=run_file)

root.mainloop()
