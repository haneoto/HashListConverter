import os
import re
import tkinter as tk
from tkinter import filedialog
import tkinterdnd2 as tkdnd
import chardet

def move_continuous_chars_to_start(line, char_limit=40):
    pattern1 = r'([a-zA-Z0-9]{' + str(char_limit) + r',})'
    match = re.search(pattern1, line[::-1])
    if match:
        continuous_chars = match.group()[::-1]
        line = line[::-1].replace(continuous_chars, '', 1).strip()
        line = '*' + line[::-1]
        line = continuous_chars + ' ' + line
    else:
        pattern2 = r'([a-zA-Z0-9]{' + str(32) + r',})'
        match2 = re.search(pattern2, line[::-1])
        if match2:
            continuous_chars = match2.group()[::-1]
            line = line[::-1].replace(continuous_chars, '', 1).strip()
            line = '*' + line[::-1]
            line = continuous_chars + ' ' + line

    _, ext = os.path.splitext(line)
    if ext:
        line = line.replace(ext[4:], '')

    line = line.rstrip()

    return line

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        return result['encoding']

def process_file(input_file, output_file):
    encoding = detect_encoding(input_file)

    if encoding == 'GB2312':
        encoding = 'gbk'
    elif encoding == 'SHIFT_JIS':
        encoding = 'shift-jis'

    with open(input_file, 'r', encoding=encoding, errors='ignore') as file:
        lines = file.readlines()

    processed_lines = [move_continuous_chars_to_start(line.strip()) for line in lines if '-----' not in line and 'Bytes' not in line and line.strip()]

    encoding = 'utf-8'
    with open(output_file, 'w', encoding=encoding) as file:
        file.writelines([line + '\n' for line in processed_lines])

def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path.strip())
        entry.config(fg="black")
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, os.path.dirname(file_path))
        output_folder_entry.config(fg="black")

def browse_output_folder(entry):
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry.delete(0, tk.END)
        entry.insert(0, folder_path.strip())
        entry.config(fg="black")

def process_files():
    input_file = input_file_entry.get()
    output_folder = output_folder_entry.get()

    if input_file:
        if not output_folder:
            output_folder = os.path.dirname(input_file)
            output_folder_entry.insert(0, output_folder)
            output_folder_entry.config(fg="black")

        with open(input_file, 'rb') as file:
            rawdata = file.read()
            result = chardet.detect(rawdata)
            encoding = result['encoding']

        if encoding == 'GB2312':
            encoding = 'gbk'
        elif encoding == 'SHIFT_JIS':
            encoding = 'shift-jis'

        with open(input_file, 'r', encoding=encoding, errors='ignore') as file:
            text = file.read()

        pattern1 = r'([a-zA-Z0-9]{' + str(40) + r',})'
        match1 = re.search(pattern1, text)

        if match1:
            output_extension = '.sha'
        else:
            pattern2 = r'([a-zA-Z0-9]{' + str(32) + r',})'
            match2 = re.search(pattern2, text)
            if match2:
                output_extension = '.md5'

        input_filename = os.path.basename(input_file)
        output_filename = os.path.splitext(input_filename)[0] + output_extension
        output_file = os.path.join(output_folder, output_filename)

        try:
            process_file(input_file, output_file)
            result_label.config(text="File processed successfully.")
        except Exception as e:
            result_label.config(text=f"Error occurred while processing the file: {str(e)}")
    else:
        result_label.config(text="Please choose an input file first.")

def on_drop(event):
    file_path = event.data.strip('{}')
    if os.path.isfile(file_path) and file_path.lower().endswith('.txt'):
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)
        input_file_entry.config(fg="black")
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, os.path.dirname(file_path))
        output_folder_entry.config(fg="black")
    else:
        result_label.config(text="Please drop a single text file.")

root = tkdnd.TkinterDnD.Tk()
root.title("HashListConverter (.txt to .sha or .md5)")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 540
window_height = 165

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

input_file_label = tk.Label(root, text="Input File:")
input_file_label.grid(row=0, column=0, padx=5, pady=5)

input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=5, pady=5)
input_file_entry.insert(0, "Drop or choose a file")
input_file_entry.config(fg="gray")

browse_input_button = tk.Button(root, text="Browse", command=lambda: browse_file(input_file_entry))
browse_input_button.grid(row=0, column=2, padx=5, pady=5)

output_folder_label = tk.Label(root, text="Output Folder:")
output_folder_label.grid(row=1, column=0, padx=5, pady=5)

output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=5, pady=5)
output_folder_entry.insert(0, "Default: Same as input file directory")
output_folder_entry.config(fg="gray")

browse_output_button = tk.Button(root, text="Browse", command=lambda: browse_output_folder(output_folder_entry))
browse_output_button.grid(row=1, column=2, padx=5, pady=5)

process_button = tk.Button(root, text="Process File", command=process_files)
process_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

result_label = tk.Label(root, text="", wraplength=window_width - 20)
result_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

root.drop_target_register(tkdnd.DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Make the window always on top
root.attributes('-topmost', True)

root.mainloop()
