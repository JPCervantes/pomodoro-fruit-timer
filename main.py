import threading
from tkinter import *
import math
from random import choice
from playsound import playsound

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECKMARK = "✔"
reps = 0
timer_active = None
fruits_list = ["grapes", "tomato", "pineapple", "lemon", "lemon2", "apple", "orange"]
random_fruit = choice(fruits_list)
photo_image_list = []
tel = "media/telephone.mp3"

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global reps, random_fruit
    window.after_cancel(timer_active)
    time_label.config(text="Timer", fg=GREEN)
    check_label.config(text="")
    canvas.itemconfig(timer, text="00:00")
    random_fruit = choice(fruits_list)
    canvas.itemconfig(fruit_dynamic, image=choice(photo_image_list))
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps, random_fruit
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        time_countdown(long_break_sec)
        time_label.config(text="Break", fg=RED)
        sound_thread = threading.Thread(target=lambda: playsound(tel))
        sound_thread.start()
    elif reps % 2 == 0:
        time_countdown(short_break_sec)
        time_label.config(text="Break", fg=PINK)
        sound_thread = threading.Thread(target=lambda: playsound(tel))
        sound_thread.start()
    else:
        time_countdown(work_sec)
        time_label.config(text="Work", fg=GREEN)
        sound_thread = threading.Thread(target=lambda: playsound(tel))
        sound_thread.start()

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 


def time_countdown(count):
    minute_count = math.floor(count/60)
    second_count = count % 60
    if second_count < 10:
        second_count = f"0{second_count}"

    canvas.itemconfig(timer, text=f"{minute_count}:{second_count}")
    if count > 0:
        global timer_active
        timer_active = canvas.after(1000, time_countdown, count - 1)
    else:
        start_timer()
        if reps % 2 == 0:
            check_label.config(text=CHECKMARK * math.floor(reps/2))

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=100, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

for img in fruits_list:
    fruit_img = PhotoImage(file=f"img/{img}.png")
    photo_image_list.append(fruit_img)

fruit_dynamic = canvas.create_image(100, 112, image=choice(photo_image_list))
timer = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

time_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 40, "bold"))
time_label.grid(column=1, row=0)

start_btn = Button(text="Start", highlightthickness=0, command=start_timer)
start_btn.grid(column=0, row=2)

reset_btn = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_btn.grid(column=2, row=2)

check_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 20, "bold"))
check_label.grid(column=1, row=3)


window.mainloop()
