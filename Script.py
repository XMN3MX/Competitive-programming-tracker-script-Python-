import time
import csv
import os
import tkinter as tk
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Setup
SHEET_NAME = "Sheet name"
JSON_KEYFILE = "JSON key"
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

# Configuration
log_file = "log.csv"
session_file = "session.txt"
timer_running = False
start_time = 0
elapsed_time = 0
problems_solved = 0
session_start_date = None

# Format Time
def format_time(seconds):
    return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02}"

# Save session to file
def save_session():
    global elapsed_time, problems_solved, session_start_date
    with open(session_file, "w") as f:
        f.write(f"{session_start_date},{elapsed_time},{problems_solved}")

# Load session from file
def load_session():
    global elapsed_time, problems_solved, session_start_date
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            data = f.read().strip().split(",")
            if len(data) == 3:
                session_start_date, elapsed_time, problems_solved = data[0], float(data[1]), int(data[2])

# Save log to CSV
def save_log():
    global elapsed_time, problems_solved, session_start_date
    if session_start_date:
        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([session_start_date, format_time(elapsed_time), problems_solved])

# Upload logs to Google Sheets
def upload_to_sheets():
    if not os.path.exists(log_file):
        return
    with open(log_file, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            sheet.append_row(row)
    clear_local_log()

# Clear local logs
def clear_local_log():
    open(log_file, "w").close()

def toggle_timer():
    global timer_running, start_time, elapsed_time
    if timer_running:
        elapsed_time += time.time() - start_time
        start_stop_button.config(text="Start Timer")
    else:
        start_time = time.time()
        start_stop_button.config(text="Stop Timer")
    timer_running = not timer_running
    save_session()
    update_display()

def increment_problem():
    global problems_solved
    if timer_running:
        problems_solved += 1
        save_session()
        update_display()

def update_display():
    global elapsed_time, timer_running
    time_spent = elapsed_time
    if timer_running:
        time_spent += time.time() - start_time
    time_label.config(text=f"Time Spent: {format_time(time_spent)}")
    problem_label.config(text=f"Problems Solved: {problems_solved}")
    root.after(1000, update_display)

def start_day():
    global session_start_date, elapsed_time, problems_solved
    session_start_date = datetime.today().strftime("%Y-%m-%d")
    elapsed_time = 0
    problems_solved = 0
    save_session()
    main_ui()

def close_day():
    global timer_running
    if timer_running:
        toggle_timer()
    save_log()
    upload_to_sheets()
    if os.path.exists(session_file):
        os.remove(session_file)
    start_screen()

def on_close():
    if timer_running:
        toggle_timer()
    save_session()
    root.destroy()

def main_ui():
    for widget in root.winfo_children():
        widget.destroy()
    global time_label, problem_label, start_stop_button
    time_label = tk.Label(root, text="Time Spent: 00:00:00", font=("Arial", 12))
    time_label.pack(pady=10)
    problem_label = tk.Label(root, text="Problems Solved: 0", font=("Arial", 12))
    problem_label.pack(pady=10)
    start_stop_button = tk.Button(root, text="Start Timer", command=toggle_timer, font=("Arial", 12))
    start_stop_button.pack(pady=5)
    problem_button = tk.Button(root, text="Solve Problem", command=increment_problem, font=("Arial", 12))
    problem_button.pack(pady=5)
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    close_day_button = tk.Button(button_frame, text="Close Day", command=close_day, font=("Arial", 12))
    close_day_button.pack(side=tk.LEFT, padx=5)
    exit_button = tk.Button(button_frame, text="Exit", command=on_close, font=("Arial", 12))
    exit_button.pack(side=tk.LEFT, padx=5)
    update_display()

def start_screen():
    for widget in root.winfo_children():
        widget.destroy()
    if os.path.exists(session_file):
        load_session()
        main_ui()
    else:
        start_button = tk.Button(root, text="Start a New Day", command=start_day, font=("Arial", 12))
        start_button.pack(pady=50)

root = tk.Tk()
root.title("Daily Timer Tracker")
root.geometry("300x200")
root.protocol("WM_DELETE_WINDOW", on_close)
start_screen()
root.mainloop()
