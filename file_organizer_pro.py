import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# File categories
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"]
}

log_file = "organizer_log.txt"


# Write logs
def write_log(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")


# Organize by file type
def organize_by_type(folder_path):

    files = os.listdir(folder_path)

    for file in files:

        file_path = os.path.join(folder_path, file)

        if os.path.isdir(file_path):
            continue

        extension = os.path.splitext(file)[1].lower()
        moved = False

        for folder, extensions in file_types.items():

            if extension in extensions:

                target = os.path.join(folder_path, folder)

                if not os.path.exists(target):
                    os.makedirs(target)

                shutil.move(file_path, os.path.join(target, file))

                write_log(f"Moved {file} -> {folder}")
                moved = True
                break

        if not moved:

            other = os.path.join(folder_path, "Others")

            if not os.path.exists(other):
                os.makedirs(other)

            shutil.move(file_path, os.path.join(other, file))
            write_log(f"Moved {file} -> Others")


# Organize by date
def organize_by_date(folder_path):

    files = os.listdir(folder_path)

    for file in files:

        file_path = os.path.join(folder_path, file)

        if os.path.isdir(file_path):
            continue

        timestamp = os.path.getmtime(file_path)

        date_folder = datetime.fromtimestamp(timestamp).strftime("%Y-%m")

        target = os.path.join(folder_path, date_folder)

        if not os.path.exists(target):
            os.makedirs(target)

        shutil.move(file_path, os.path.join(target, file))

        write_log(f"Moved {file} -> {date_folder}")


# Select folder
def select_folder():

    folder = filedialog.askdirectory()

    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)


# Run organizer
def run_organizer():

    folder = folder_entry.get()

    if folder == "":
        messagebox.showwarning("Error", "Please select a folder")
        return

    try:

        if mode.get() == "type":
            organize_by_type(folder)

        elif mode.get() == "date":
            organize_by_date(folder)

        messagebox.showinfo("Success", "Files organized successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI
root = tk.Tk()
root.title("File Organizer Pro")
root.geometry("500x300")
root.resizable(False, False)

title = tk.Label(root, text="File Organizer Pro", font=("Arial", 16, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

folder_entry = tk.Entry(frame, width=40)
folder_entry.grid(row=0, column=0)

browse_btn = tk.Button(frame, text="Browse", command=select_folder)
browse_btn.grid(row=0, column=1)

mode = tk.StringVar(value="type")

type_radio = tk.Radiobutton(root, text="Organize by File Type", variable=mode, value="type")
type_radio.pack()

date_radio = tk.Radiobutton(root, text="Organize by Date", variable=mode, value="date")
date_radio.pack()

run_btn = tk.Button(root, text="Organize Files", command=run_organizer, bg="green", fg="white")
run_btn.pack(pady=20)

root.mainloop()