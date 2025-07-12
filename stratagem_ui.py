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
        tk.Label(self.root, text="Select 4 Stratagems:").pack()
        self.listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=40, height=20)
        for strat in self.stratagems:
            self.listbox.insert(tk.END, strat)
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.save_btn = tk.Button(self.root, text="Add to Loadout", command=self.save_loadout)
        self.save_btn.pack(pady=10)

    def on_select(self, event):
        selected_indices = self.listbox.curselection()
        if len(selected_indices) > 4:
            # Deselect the last selected
            self.listbox.selection_clear(selected_indices[-1])
            messagebox.showwarning("Limit Exceeded", "You can only select 4 stratagems.")

    def save_loadout(self):
        selected_indices = self.listbox.curselection()
        if len(selected_indices) != 4:
            messagebox.showerror("Invalid Selection", "Please select exactly 4 stratagems.")
            return
        selected_strats = [self.listbox.get(i) for i in selected_indices]
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

    def load_loadouts(self):
        if not os.path.exists(LOADOUT_FILE):
            return {}
        with open(LOADOUT_FILE, 'r') as f:
            return json.load(f)

def main():
    root = tk.Tk()
    app = StratagemApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
