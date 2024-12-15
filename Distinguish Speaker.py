import sys
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox

# Hide console window (Windows only)
if sys.platform.startswith('win'):
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, 0)

def convert_spaces_to_underscores(text, interviewer_name):
    lines = text.split('\n')
    result = []
    for line in lines:
        if f'[{interviewer_name}]' in line:
            parts = line.split(']', 1)
            parts[1] = parts[1].replace(' ', '_')
            result.append(']'.join(parts))
        else:
            result.append(line)
    return '\n'.join(result)

def convert_to_uppercase(text, interviewer_name):
    lines = text.split('\n')
    result = []
    for line in lines:
        if f'[{interviewer_name}]' in line:
            parts = line.split(']', 1)
            parts[1] = parts[1].upper()
            result.append(']'.join(parts))
        else:
            result.append(line)
    return '\n'.join(result)

def restore_original_format(text, interviewer_name):
    lines = text.split('\n')
    result = []
    for line in lines:
        if f'[{interviewer_name}]' in line:
            parts = line.split(']', 1)
            parts[1] = parts[1].replace('_', ' ')
            result.append(']'.join(parts))
        else:
            result.append(line)
    return '\n'.join(result)

def convert_to_title_case(text, interviewer_name):
    lines = text.split('\n')
    result = []
    for line in lines:
        if f'[{interviewer_name}]' in line:
            parts = line.split(']', 1)
            parts[1] = parts[1].title()  # Convert text to title case
            result.append(']'.join(parts))
        else:
            result.append(line)
    return '\n'.join(result)

def update_text_area(func):
    text = text_area.get('1.0', tk.END)
    interviewer_name = name_entry.get().strip()
    if not interviewer_name:
        messagebox.showerror("Error", "Please enter an Interviewer Name.")
        return
    updated_text = func(text, interviewer_name)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, updated_text)

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_area.delete('1.0', tk.END)
            text_area.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_area.get('1.0', tk.END))
        messagebox.showinfo("Success", "File saved successfully!")

# GUI setup
root = tk.Tk()
root.title("Distinguish_Speaker")
root.configure(bg='gray')

text_area = tk.Text(root, wrap='word', bg='light gray', fg='black')
text_area.pack(expand=True, fill='both')

button_frame = tk.Frame(root, bg='gray')
button_frame.pack(fill='x')

name_label = tk.Label(button_frame, text="Interviewer Name:", bg='gray', fg='white')
name_label.pack(side='left', padx=5, pady=5)

name_entry = tk.Entry(button_frame)
name_entry.pack(side='left', padx=5, pady=5)

load_button = tk.Button(button_frame, text="Load TXT", command=load_file, bg='dark gray', fg='white')
load_button.pack(side='left', padx=5, pady=5)

underscores_button = tk.Button(button_frame, text="Spaces to Underscores", command=lambda: update_text_area(convert_spaces_to_underscores), bg='dark gray', fg='white')
underscores_button.pack(side='left', padx=5, pady=5)

restore_button = tk.Button(button_frame, text="Restore Original", command=lambda: update_text_area(restore_original_format), bg='dark gray', fg='white')
restore_button.pack(side='left', padx=5, pady=5)

save_button = tk.Button(button_frame, text="Save TXT", command=save_file, bg='dark gray', fg='white')
save_button.pack(side='left', padx=5, pady=5)

uppercase_button = tk.Button(button_frame, text="To Uppercase", command=lambda: update_text_area(convert_to_uppercase), bg='dark gray', fg='white')
uppercase_button.pack(side='left', padx=5, pady=5)

title_case_button = tk.Button(button_frame, text="To Title Case", command=lambda: update_text_area(convert_to_title_case), bg='dark gray', fg='white')
title_case_button.pack(side='left', padx=5, pady=5)

root.mainloop()