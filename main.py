import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

SIZE_disk = (600, 600, 3)
CENTER = (SIZE_disk[0] // 2, SIZE_disk[1] // 2)
RADIUS = SIZE_disk[0] // 2
DELTA = 360 // 33

def get_colors():
    colors = [(255, 0, 0), (242, 255, 0), (26, 255, 0), (0, 255, 221), (0, 106, 255), (140, 0, 255), (255, 0, 242)]
    return colors

def get_alphabet():
    alphabet = {}
    colors = get_colors()
    q_colors = len(colors)

    color_counter = 0
    for i in range(1040, 1072):
        alphabet[chr(i)] = ((colors[q_colors - color_counter // q_colors - 1]), (colors[color_counter % q_colors]))
        color_counter += 1

    alphabet[" "] = ((255, 255, 255), (255, 255, 255))
    return alphabet

def draw_code(disk, msg: str, alphabet):
    angle = 0
    angle_message = 2 * DELTA * len(msg)

    while angle < 360:
        disk = cv.ellipse(disk, CENTER, (RADIUS, RADIUS), 0, angle, angle + DELTA, alphabet[msg[angle % angle_message // (2*DELTA)]][0], -1)
        angle += DELTA

        disk = cv.ellipse(disk, CENTER, (RADIUS, RADIUS), 0, angle, angle + DELTA, alphabet[msg[(angle - 8) % angle_message // (2*DELTA)]][1], -1)
        angle += DELTA

    return disk

def create_color_table(alphabet):
    table_size = (len(alphabet), 3, 3)

    table_image = np.ones(shape=table_size, dtype='uint8') * 255

    for i, (_, colors) in enumerate(alphabet.items()):
        table_image[i, 0, :] = 255
        table_image[i, 1, :] = colors[0]
        table_image[i, 2, :] = colors[1]

    return table_image

def plot_color_table(table_image, alphabet):
    _, ax = plt.subplots(figsize=(8, 10))
    ax.axis('off')

    table = ax.table(cellText=None, cellColours=table_image / 255.0, cellLoc='center', loc='center')

    for i, (letter, _) in enumerate(alphabet.items()):
        table[(i, 0)].get_text().set_text(letter)

    table[(len(alphabet) - 1, 0)].get_text().set_text("Пробел")

    plt.title("Алфавит")
    plt.show()

def on_alphabet_button_click():
    legend_image = create_color_table(alphabet)
    plot_color_table(legend_image, alphabet)

def on_encode_button_click():
    msg = entry.get()
    disk_image = np.zeros(shape=SIZE_disk, dtype='uint8')
    disk_image = cv.rectangle(disk_image, (0, 0), (SIZE_disk[0], SIZE_disk[1]), (220, 200, 200), -1)
    disk_image = cv.circle(disk_image, CENTER, RADIUS, (255, 255, 255), -1)
    disk_image = draw_code(disk_image, msg, alphabet)

    cv.imwrite("code.png", disk_image)

    cv.namedWindow("Disk")
    cv.imshow("Disk", disk_image)

root = tk.Tk()
root.title("Кодирование диска")
root.geometry("400x200")  # Задаем размеры окна

alphabet = get_alphabet()

alphabet_button = ttk.Button(root, text="Вывести алфавит", command=on_alphabet_button_click)
alphabet_button.pack(pady=10)

entry_label = ttk.Label(root, text="Введите слово:")
entry_label.pack()

entry = ttk.Entry(root)
entry.pack(pady=10)

encode_button = ttk.Button(root, text="Закодировать диск", command=on_encode_button_click)
encode_button.pack(pady=10)

root.mainloop()