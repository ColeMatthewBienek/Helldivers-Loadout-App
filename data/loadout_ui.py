"""
Helldivers 2 Loadout UI
This app lets you select a loadout and generates an AutoHotkey script to send the correct keystrokes.
"""
import json
import subprocess
import os
import tkinter as tk
from tkinter import messagebox

# --- Constants ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOADOUTS_FILE = os.path.join(BASE_DIR, 'loadouts.json')
STRATAGEMS_FILE = os.path.join(BASE_DIR, 'stratagems.json')
AHK_SCRIPT = os.path.join(BASE_DIR, 'generated_loadout.ahk')
AHK_EXE = '/mnt/c/Program Files/AutoHotkey/v1.1.37.02/AutoHotkeyU32.exe'

# --- Read loadouts.json and stratagems.json ---
def read_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read {path}: {e}")
        return None

# --- Write the AHK script for the selected loadout ---
def write_ahk(loadout):
    stratagems = read_json(STRATAGEMS_FILE)
    if stratagems is None:
        return
    ahk_lines = [
        '#SingleInstance force',
        'SetKeyDelay, 70',
        '',
    ]
    # For each stratagem in the loadout, generate a hotkey ^1::, ^2::, ...
    for idx, strat_name in enumerate(loadout, 1):
        found = False
        for color, group in stratagems.items():
            if strat_name in group:
                keys = group[strat_name]
                found = True
                break
        if not found:
            ahk_lines.append(f'; ERROR: Stratagem not found: {strat_name}')
            continue
        ahk_lines.append(f'^%d::' % idx)
        ahk_lines.append('    SendInput {L down}')
        for dir in keys:
            key = direction_to_key(dir)
            if not key:
                ahk_lines.append(f'    ; ERROR: Unknown direction: {dir}')
                continue
            ahk_lines.append(f'    SendInput {key}')
            ahk_lines.append('    Sleep 70')
        ahk_lines.append('    SendInput {L up}')
        ahk_lines.append('    Return')
        ahk_lines.append('')
    # Write the script
    with open(AHK_SCRIPT, 'w') as f:
        f.write('\n'.join(ahk_lines))

# --- Helper: Map direction to AHK key ---
def direction_to_key(dir):
    return {
        'up': '{Up}',
        'down': '{Down}',
        'left': '{Left}',
        'right': '{Right}'
    }.get(dir, '')

# --- Reload the AHK script ---
def reload_ahk():
    try:
        subprocess.run([AHK_EXE, AHK_SCRIPT], check=True)
    except Exception as e:
        messagebox.showerror("AHK Error", f"Could not reload AHK script: {e}")

# --- On Listbox selection ---
def on_select(event):
    selection = event.widget.curselection()
    if not selection:
        return
    idx = selection[0]
    loadout_name = event.widget.get(idx)
    loadouts = read_json(LOADOUTS_FILE)
    if loadouts is None:
        return
    if loadout_name not in loadouts:
        messagebox.showerror("Loadout Error", f"Loadout '{loadout_name}' not found in loadouts.json.")
        return
    loadout = loadouts[loadout_name]
    write_ahk(loadout)
    reload_ahk()
    messagebox.showinfo("Success", f"AHK script generated and reloaded for loadout '{loadout_name}'.")

# --- Build the Tkinter UI ---
def main():
    root = tk.Tk()
    root.title("Helldivers 2 Loadout UI")
    tk.Label(root, text="Select Loadout:").pack(pady=5)
    listbox = tk.Listbox(root, width=40, height=15)
    listbox.pack()
    # Populate listbox with loadout names
    loadouts = read_json(LOADOUTS_FILE)
    if loadouts:
        for name in sorted(loadouts.keys()):
            listbox.insert(tk.END, name)
    listbox.bind('<<ListboxSelect>>', on_select)
    tk.Button(root, text="Quit", command=root.quit).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
