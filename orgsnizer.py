import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to categorize files
def categorize_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt"],
        "Music": [".mp3", ".wav"],
        "Videos": [".mp4", ".mkv"],
        "Archives": [".zip", ".rar"],
        "Code": [".py", ".java", ".c", ".cpp"]
    }
    for category, extensions in categories.items():
        if ext in extensions:
            return category
    return "Others"

# Function to organize files
def organize_files(folder_path, output_box, status_label):
    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder first!")
        return

    status_label.config(text="🟡 Organizing...", fg="orange")
    root.update_idletasks()

    files = os.listdir(folder_path)
    output_box.delete(1.0, tk.END)  # Clear previous text

    for item in files:
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            category = categorize_file(item)
            category_path = os.path.join(folder_path, category)
            os.makedirs(category_path, exist_ok=True)
            shutil.move(item_path, os.path.join(category_path, item))
            output_box.insert(tk.END, f"{item} -> moved to {category} folder\n")

    status_label.config(text="✅ Done", fg="green")
    messagebox.showinfo("Done ✅", "Files have been organized successfully!")

# Function to browse folder
def browse_folder(entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry.delete(0, tk.END)
        entry.insert(0, folder_selected)

# Function to clear output box
def clear_output(output_box, status_label):
    output_box.delete(1.0, tk.END)
    status_label.config(text="🟢 Ready", fg="blue")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("📂 File Organizer")
root.geometry("600x450")
root.configure(bg="#f4f4f9")  # soft background

# Heading
tk.Label(
    root, text="📁 File Organizer",
    font=("Arial", 18, "bold"),
    bg="#4CAF50", fg="white", pady=10
).pack(fill="x")

# Folder input
frame = tk.Frame(root, bg="#f4f4f9")
frame.pack(pady=20)

tk.Label(frame, text="Select Folder:", font=("Arial", 12), bg="#f4f4f9").grid(row=0, column=0, padx=5)
folder_path = tk.Entry(frame, width=40, font=("Arial", 12))
folder_path.grid(row=0, column=1, padx=5)
tk.Button(frame, text="Browse", bg="#2196F3", fg="white", command=lambda: browse_folder(folder_path)).grid(row=0, column=2, padx=5)

# Frame for output box + scrollbar
output_frame = tk.Frame(root, bg="#f4f4f9")
output_frame.pack(pady=10)

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_box = tk.Text(output_frame, height=10, width=60, font=("Courier New", 10), yscrollcommand=scrollbar.set)
output_box.pack(side=tk.LEFT)

scrollbar.config(command=output_box.yview)

# Organize button
tk.Button(
    root,
    text="🚀 Organize Files",
    font=("Arial", 14, "bold"),
    bg="#4CAF50", fg="white",
    padx=20, pady=10,
    command=lambda: organize_files(folder_path.get(), output_box, status_label)
).pack(pady=10)

# Clear button
tk.Button(
    root,
    text="🧹 Clear Output",
    font=("Arial", 12),
    bg="#f44336", fg="white",
    padx=15, pady=5,
    command=lambda: clear_output(output_box, status_label)
).pack()

# Status bar
status_label = tk.Label(
    root, text="🟢 Ready", bd=1, relief=tk.SUNKEN,
    anchor="w", bg="#f4f4f9", font=("Arial", 10), fg="blue"
)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
