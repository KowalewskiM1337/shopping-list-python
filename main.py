# -*-coding: utf-8-*-
# -*-coding: iso-8859-2-*-
import tkinter as tk
from tkinter import font, messagebox

# Window app and it's settings
root = tk.Tk()
root.title('Lista zakupów')
# root.resizable(False, True)
root.geometry('800x600')

# Configuration of grid layout
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=0)

# Custom fonts saved to variable so it can be used multiple times
normal_font = font.Font(
    family='Century Gothic',
    size=12,
    overstrike=False
)

crossed_font = font.Font(
    family='Century Gothic',
    size=12,
    overstrike=True
)

# Variables later used in functions
product_list = []
click_count = 0

# Classes and functions
class CrossItem:

    def __init__(self, item_entry):
        self.item_entry = item_entry

    def cross_item(self, item_entry):
        item_entry.config(font=crossed_font)


class UncrossItem(CrossItem):

    def uncross_item(self, item_entry):
        item_entry.config(font=normal_font)


class DeleteItem:

    def __init__(self, row_frame):
        self.row_frame = row_frame

    def delete_item(self, row_frame):
        global click_count
        click_count-=1
        row_frame.destroy()


def add_new_item():
    global click_count, add_item_str

    product_name = add_item_str.get()
    product_list.append(product_name)

    if len(product_name) > 30:
        return messagebox.showinfo('Info', 'Nazwa produktu za długa')
    elif len(product_name) < 3:
        return messagebox.showinfo('Info', 'Nazwa produktu za krótka')

    click_count += 1

    # Creating new row in set frame
    row_frame = tk.Frame(root)
    row_frame.grid(row=click_count+2, column=0, columnspan=5)

    counter_label = tk.Label(
        row_frame,
        text=f"{click_count}.",
        font=normal_font
    )
    counter_label.grid(row=click_count, column=0)

    product_entry = tk.Entry(
        row_frame,
        font=normal_font,
        width=30
    )
    product_entry.grid(row=click_count, column=1)
    product_entry.insert(0, product_name)
    cross_item = CrossItem(product_entry)

    bought_btn = tk.Button(
        row_frame,
        text='Kupione',
        width=10,
        bg='lightblue',
        command=lambda: cross_item.cross_item(product_entry),
        font=normal_font
    )
    bought_btn.grid(row=click_count, column=3)

    uncrossed_item = UncrossItem(product_entry)

    unbought_btn = tk.Button(
        row_frame,
        text='Odznacz',
        width=10,
        bg='lime',
        command=lambda: uncrossed_item.uncross_item(product_entry),
        font=normal_font
    )
    unbought_btn.grid(row=click_count, column=4)

    deleted_item = DeleteItem(row_frame)

    clear_btn = tk.Button(
        row_frame,
        text='Usuń',
        width=10,
        bg='orange',
        command=lambda: deleted_item.delete_item(row_frame),
        font=normal_font
    )
    clear_btn.grid(row=click_count, column=5)

    add_item_str.delete(0, tk.END)

def export_list_to_file():
    file = open('Lista-zakupow.txt', 'w')
    for product in product_list:
        file.write(f"{product_list.index(product)+1}. {product}\n")
    file.close()
    messagebox.showinfo('Informacja', 'Wyeksportowano do pliku "Lista-zakupow.txt" ')


header = tk.Label(
    text='Lista zakupów',
    font=('Century Gothic', 24)
)
header.grid(row=0, column=0, columnspan=5)

tk.Label(
    text='Podaj nazwe produktu:',
    font=normal_font
).grid(row=1, column=1)

add_item_str = tk.Entry(
    width=45,
    bd=4,
    font=('Century Gothic', 10)
)
add_item_str.grid(row=1, column=2)

add_item_btn = tk.Button(
    text='Dodaj',
    width=10,
    bg='green',
    font=normal_font,
    command=add_new_item
)
add_item_btn.grid(row=1, column=3)

export_list_btn = tk.Button(
    text='Wyeksportuj',
    width=10,
    bg='#08B2E3',
    font=normal_font,
    command=export_list_to_file
)
export_list_btn.grid(row=1, column=4)

tk.Label(
    text=''
).grid(row=2, column=0, columnspan=5)


root.mainloop()