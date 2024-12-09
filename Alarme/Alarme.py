import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
from threading import Thread
import pygame

# Inicializar o mixer do pygame para som
pygame.mixer.init()

# Global Variables
alarms_list = []
alarm_id = 0
alarm_active = None
alarm_sound = "alarm.mp3"  # Coloque o caminho do seu arquivo de som

# Function to format time
def format_time(value):
    return f"{value:02d}"

# Function to update clock display
def update_clock():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        clock_label.config(text=current_time)

        # Check alarms
        for alarm in alarms_list:
            if alarm["is_active"] and alarm["time"] == now.strftime("%H:%M"):
                play_alarm_sound()
                break

        time.sleep(1)

# Function to play alarm sound
def play_alarm_sound():
    global alarm_active
    if alarm_active:
        return
    alarm_active = True
    pygame.mixer.music.load(alarm_sound)
    pygame.mixer.music.play(loops=-1)  # Loop infinito até ser parado
    messagebox.showinfo("Alarme", "Hora do alarme!")
    pygame.mixer.music.stop()
    alarm_active = False

# Function to add new alarm
def add_alarm():
    global alarm_id
    hour = hour_input.get()
    minute = minute_input.get()

    if not hour.isdigit() or not minute.isdigit():
        messagebox.showerror("Erro", "Insira valores válidos para horas e minutos.")
        return

    hour, minute = int(hour), int(minute)
    if not (0 <= hour <= 23) or not (0 <= minute <= 59):
        messagebox.showerror("Erro", "Insira horas (0-23) e minutos (0-59).")
        return

    alarm_time = f"{format_time(hour)}:{format_time(minute)}"
    alarms_list.append({"id": alarm_id, "time": alarm_time, "is_active": False})
    alarm_id += 1

    update_alarm_list()
    hour_input.delete(0, tk.END)
    minute_input.delete(0, tk.END)

# Function to update alarm list
def update_alarm_list():
    for widget in alarm_list_frame.winfo_children():
        widget.destroy()

    for alarm in alarms_list:
        alarm_frame = tk.Frame(alarm_list_frame, bg="white", pady=5)
        alarm_frame.pack(fill="x", padx=5)

        alarm_label = tk.Label(alarm_frame, text=alarm["time"], font=("Roboto Mono", 14), bg="white")
        alarm_label.pack(side="left", padx=10)

        toggle_btn = tk.Checkbutton(
            alarm_frame,
            text="Ativar",
            bg="white",
            command=lambda alarm=alarm: toggle_alarm(alarm)
        )
        toggle_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            alarm_frame,
            text="Excluir",
            bg="#FF6347",
            fg="white",
            command=lambda alarm=alarm: delete_alarm(alarm)
        )
        delete_btn.pack(side="right", padx=5)

# Function to toggle alarm status
def toggle_alarm(alarm):
    alarm["is_active"] = not alarm["is_active"]

# Function to delete an alarm
def delete_alarm(alarm):
    alarms_list.remove(alarm)
    update_alarm_list()

# Create GUI
root = tk.Tk()
root.title("Aplicativo de Alarme")
root.geometry("400x600")
root.config(bg="#377DFF")

# Clock Display
clock_label = tk.Label(root, text="00:00:00", font=("Roboto Mono", 40), bg="#377DFF", fg="white")
clock_label.pack(pady=20)

# Alarm Inputs
input_frame = tk.Frame(root, bg="white")
input_frame.pack(pady=20)

hour_input = tk.Entry(input_frame, width=5, font=("Roboto Mono", 20), justify="center")
hour_input.insert(0, "00")
hour_input.pack(side="left", padx=5)

minute_input = tk.Entry(input_frame, width=5, font=("Roboto Mono", 20), justify="center")
minute_input.insert(0, "00")
minute_input.pack(side="left", padx=5)

add_alarm_btn = tk.Button(input_frame, text="Adicionar Alarme", bg="#377DFF", fg="white", command=add_alarm)
add_alarm_btn.pack(side="left", padx=5)

# Active Alarms
alarm_list_frame = tk.Frame(root, bg="white")
alarm_list_frame.pack(fill="both", expand=True, padx=10, pady=20)

# Start Clock Thread
clock_thread = Thread(target=update_clock, daemon=True)
clock_thread.start()

root.mainloop()
