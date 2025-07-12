import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

STRATAGEM_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/stratagems.json'))
LOADOUT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/loadouts.json'))

class StratagemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Helldivers 2 Loadout Selector")
        self.stratagems = self.load_stratagems()
        self.selected = set()
        self.create_widgets()

    def load_stratagems(self):
        with open(STRATAGEM_FILE, 'r') as f:
            data = json.load(f)
        strat_list = []
        for category in data.values():
            strat_list.extend(category.keys())
        return sorted(strat_list)

    def create_widgets(self):
        tk.Label(self.root, text="Select 4 Stratagems in Order:").pack()
        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=40, height=20)
        for strat in self.stratagems:
            self.listbox.insert(tk.END, strat)
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.save_btn = tk.Button(self.root, text="Add to Loadout", command=self.save_loadout, state=tk.DISABLED)
        self.save_btn.pack(pady=10)
        self.selection_order = []  # Track order of selection

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        i = selected_index[0]
        if i in self.selection_order:
            return  # Already selected, ignore
        self.selection_order.append(i)
        self.listbox.itemconfig(i, {'fg': 'gray', 'bg': '#d0ffd0'})
        self.listbox.selection_clear(0, tk.END)
        if len(self.selection_order) == 4:
            self.listbox.config(state=tk.DISABLED)
            self.save_btn.config(state=tk.NORMAL)

    def save_loadout(self):
        if len(self.selection_order) != 4:
            messagebox.showerror("Invalid Selection", "Please select exactly 4 stratagems.")
            return
        selected_strats = [self.listbox.get(i) for i in self.selection_order]
        name = simpledialog.askstring("Loadout Name", "Enter a name for this loadout:")
        if not name:
            return
        loadouts = self.load_loadouts()
        loadouts[name] = selected_strats
        # Ensure the data directory exists
        data_dir = os.path.dirname(LOADOUT_FILE)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(LOADOUT_FILE, 'w') as f:
            json.dump(loadouts, f, indent=2)
        messagebox.showinfo("Saved", f"Loadout '{name}' saved.")
        # Reset for next loadout
        self.listbox.config(state=tk.NORMAL)
        for i in self.selection_order:
            self.listbox.itemconfig(i, {'fg': 'black', 'bg': 'white'})
        self.selection_order = []
        self.save_btn.config(state=tk.DISABLED)

    def load_loadouts(self):
        if not os.path.exists(LOADOUT_FILE):
            return {}
        with open(LOADOUT_FILE, 'r') as f:
            return json.load(f)

def main():
    root = tk.Tk()
    # Place window in center
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 500
    window_height = 600
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    app = StratagemApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
