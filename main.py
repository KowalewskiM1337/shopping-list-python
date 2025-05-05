import tkinter as tk
from tkinter import font, messagebox
from typing import List, Dict

class ShoppingListApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Lista zakupów')
        self.root.geometry('800x600')
        
        # Configure grid layout
        for i in range(3):
            self.root.columnconfigure(i, weight=0)
            
        # Initialize fonts
        self.normal_font = font.Font(
            family='Century Gothic',
            size=12,
            overstrike=False
        )
        self.crossed_font = font.Font(
            family='Century Gothic',
            size=12,
            overstrike=True
        )
        
        # Initialize variables
        self.product_list: List[str] = []
        self.click_count = 0
        self.row_frames: Dict[int, tk.Frame] = {}  # Store row frames with their positions
        
        self._setup_ui()
        
    def _setup_ui(self):
        # Header
        header = tk.Label(
            text='Lista zakupów',
            font=('Century Gothic', 24)
        )
        header.grid(row=0, column=0, columnspan=5)
        
        # Input section
        tk.Label(
            text='Podaj nazwe produktu:',
            font=self.normal_font
        ).grid(row=1, column=1)
        
        self.add_item_str = tk.Entry(
            width=45,
            bd=4,
            font=('Century Gothic', 10)
        )
        self.add_item_str.grid(row=1, column=2)
        
        add_item_btn = tk.Button(
            text='Dodaj',
            width=10,
            bg='green',
            font=self.normal_font,
            command=self.add_new_item
        )
        add_item_btn.grid(row=1, column=3)
        
        export_list_btn = tk.Button(
            text='Wyeksportuj',
            width=10,
            bg='#08B2E3',
            font=self.normal_font,
            command=self.export_list_to_file
        )
        export_list_btn.grid(row=1, column=4)
        
        tk.Label(text='').grid(row=2, column=0, columnspan=5)
        
    def add_new_item(self):
        product_name = self.add_item_str.get()
        
        if len(product_name) > 30:
            messagebox.showinfo('Info', 'Nazwa produktu za długa')
            return
        elif len(product_name) < 3:
            messagebox.showinfo('Info', 'Nazwa produktu za krótka')
            return
            
        self.product_list.append(product_name)
        self.click_count += 1
        
        # Create new row
        row_frame = tk.Frame(self.root)
        row_frame.grid(row=self.click_count+2, column=0, columnspan=5)
        self.row_frames[self.click_count] = row_frame
        
        # Counter label
        counter_label = tk.Label(
            row_frame,
            text=f"{self.click_count}.",
            font=self.normal_font
        )
        counter_label.grid(row=self.click_count, column=0)
        
        # Product entry
        product_entry = tk.Entry(
            row_frame,
            font=self.normal_font,
            width=30
        )
        product_entry.grid(row=self.click_count, column=1)
        product_entry.insert(0, product_name)
        
        # Buttons
        bought_btn = tk.Button(
            row_frame,
            text='Kupione',
            width=10,
            bg='lightblue',
            command=lambda: self._cross_item(product_entry),
            font=self.normal_font
        )
        bought_btn.grid(row=self.click_count, column=3)
        
        unbought_btn = tk.Button(
            row_frame,
            text='Odznacz',
            width=10,
            bg='lime',
            command=lambda: self._uncross_item(product_entry),
            font=self.normal_font
        )
        unbought_btn.grid(row=self.click_count, column=4)
        
        clear_btn = tk.Button(
            row_frame,
            text='Usuń',
            width=10,
            bg='orange',
            command=lambda: self._delete_item(row_frame, product_name),
            font=self.normal_font
        )
        clear_btn.grid(row=self.click_count, column=5)
        
        self.add_item_str.delete(0, tk.END)
        
    def _cross_item(self, item_entry):
        item_entry.config(font=self.crossed_font)
        
    def _uncross_item(self, item_entry):
        item_entry.config(font=self.normal_font)
        
    def _delete_item(self, row_frame, product_name):
        # Find the position of the deleted item
        deleted_position = None
        for pos, frame in self.row_frames.items():
            if frame == row_frame:
                deleted_position = pos
                break
                
        if deleted_position is not None:
            # Remove the frame from our tracking dictionary
            del self.row_frames[deleted_position]
            
            # Update positions of all frames after the deleted one
            for pos in range(deleted_position + 1, self.click_count + 1):
                if pos in self.row_frames:
                    frame = self.row_frames[pos]
                    frame.grid(row=pos, column=0, columnspan=5)
                    # Update counter label
                    counter_label = frame.winfo_children()[0]
                    counter_label.config(text=f"{pos-1}.")
                    # Update row number in grid
                    for widget in frame.winfo_children():
                        widget.grid_configure(row=pos-1)
            
            # Remove the frame from the UI
            row_frame.destroy()
            
            # Update product list and click count
            self.product_list.remove(product_name)
            self.click_count -= 1
            
            # Update the row_frames dictionary with new positions
            new_row_frames = {}
            for pos in range(1, self.click_count + 1):
                if pos in self.row_frames:
                    new_row_frames[pos-1] = self.row_frames[pos]
            self.row_frames = new_row_frames
        
    def export_list_to_file(self):
        with open('Lista-zakupow.txt', 'w', encoding='utf-8') as file:
            for i, product in enumerate(self.product_list, 1):
                file.write(f"{i}. {product}\n")
        messagebox.showinfo('Informacja', 'Wyeksportowano do pliku "Lista-zakupow.txt"')
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = ShoppingListApp()
    app.run() 