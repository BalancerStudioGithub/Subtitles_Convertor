import ctypes
import sys
import tkinter as tk
from tkinter import filedialog
import re
from datetime import timedelta

# 隐藏控制台窗口（仅限于Windows）
if sys.platform.startswith('win'):
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    SW_HIDE = 0
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, SW_HIDE)

def parse_time(time_str):
    """将时间字符串（mm:ss或hh:mm:ss）转换为SRT格式的时间戳（HH:mm:ss,SSS）"""
    if ':' not in time_str:
        return "00:00:00,000"
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = map(int, parts)
        hours = 0
    elif len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
    else:
        return "00:00:00,000"
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},000"

def increment_time(time_str, seconds):
    """给定一个时间码和秒数，返回增加指定秒数后的时间码"""
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds_in = map(int, parts)
        hours = 0
    elif len(parts) == 3:
        hours, minutes, seconds_in = map(int, parts)
    delta = timedelta(hours=hours, minutes=minutes, seconds=seconds_in)
    new_delta = delta + timedelta(seconds=seconds)
    hours, remainder = divmod(new_delta.seconds + new_delta.days * 86400, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def read_txt_and_convert_to_srt(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read().splitlines()
    srt_lines = []
    sequence_number = 1
    prev_timecode = None
    prev_line = ""
    is_last_entry = False
    for index, line in enumerate(text_content):
        time_match = re.search(r'(\d{1,2}:\d{2}:\d{2}|\d{1,2}:\d{2})', line)
        if time_match:
            current_timecode = time_match.group(0)
            if prev_timecode:
                if index == len(text_content) - 1:
                    # 如果这是最后一行，增加1秒
                    end_timecode = increment_time(prev_timecode, 1)
                    is_last_entry = True
                else:
                    end_timecode = current_timecode
                srt_lines.append(
                    f"{sequence_number}\n"
                    f"{parse_time(prev_timecode)} --> {parse_time(end_timecode)}\n"
                    f"{prev_line.strip()}\n"
                )
                sequence_number += 1
            prev_timecode = current_timecode
            prev_line = line.replace(current_timecode, '').strip()
        else:
            prev_line += ' ' + line.strip()
    if prev_timecode and prev_line and not is_last_entry:
        # 如果最后一行没有时间码，这里处理
        end_timecode = increment_time(prev_timecode, 1)
        srt_lines.append(
            f"{sequence_number}\n"
            f"{parse_time(prev_timecode)} --> {parse_time(end_timecode)}\n"
            f"{prev_line.strip()}\n"
        )
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(srt_lines)

def select_input_file():
    global input_file_path
    input_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    input_label.config(text=input_file_path)

def select_output_location():
    global output_file_path
    output_file_path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")])
    output_label.config(text=output_file_path)

def generate_srt():
    if input_file_path and output_file_path:
        read_txt_and_convert_to_srt(input_file_path, output_file_path)
        status_label.config(text="完成")

# GUI主窗口
root = tk.Tk()
root.title("Srt Time Stamp Tool")

# 按钮和标签
input_button = tk.Button(root, text="原字幕", command=select_input_file)
input_button.pack()
input_label = tk.Label(root, text="")
input_label.pack()

location_button = tk.Button(root, text="位置", command=select_output_location)
location_button.pack()
output_label = tk.Label(root, text="")
output_label.pack()

generate_button = tk.Button(root, text="生成", command=generate_srt)
generate_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

# 初始化全局变量
input_file_path = None
output_file_path = None

root.mainloop()