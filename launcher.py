import tkinter as tk
import subprocess
import os
import sys

# Paths to your scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STRATAGEM_UI = os.path.join(BASE_DIR, "stratagem_ui.py")
LOADOUT_UI = os.path.join(BASE_DIR, "data", "loadout_ui.py")

def launch_stratagem_ui():
    subprocess.Popen([sys.executable, STRATAGEM_UI])

def launch_loadout_ui():
    subprocess.Popen([sys.executable, LOADOUT_UI])

root = tk.Tk()
root.title("Helldivers 2 Tools Launcher")
# Place window in upper right
root.update_idletasks()
screen_width = root.winfo_screenwidth()
window_width = 300
window_height = 150
x = screen_width - window_width - 20  # 20px from right edge
root.geometry(f"{window_width}x{window_height}+{x}+20")

tk.Label(root, text="Helldivers 2 Desktop Launcher", font=("Arial", 14, "bold")).pack(pady=10)
tk.Button(root, text="Stratagem UI", command=launch_stratagem_ui, width=20, height=2).pack(pady=5)
tk.Button(root, text="Loadout UI", command=launch_loadout_ui, width=20, height=2).pack(pady=5)
tk.Button(root, text="Quit", command=root.quit, width=20).pack(pady=5)

root.mainloop()
