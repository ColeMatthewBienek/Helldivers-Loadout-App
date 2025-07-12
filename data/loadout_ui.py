"""
Helldivers 2 Loadout UI
This app lets you select a loadout and generates an AutoHotkey script to send the correct keystrokes.
"""
import json
import subprocess
import os
import tkinter as tk
from tkinter import messagebox
import logging
import datetime

# --- Constants ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOADOUTS_FILE = os.path.join(BASE_DIR, 'loadouts.json')
STRATAGEMS_FILE = os.path.join(BASE_DIR, 'stratagems.json')
AHK_SCRIPT = os.path.join(BASE_DIR, 'generated_loadout.ahk')

# Convert Unix paths to Windows paths for AHK
def unix_to_windows_path(unix_path):
    # First handle direct /mnt/c/ paths (standard WSL mapping)
    if unix_path.startswith('/mnt/c/'):
        return 'C:' + unix_path[6:].replace('/', '\\')
    # Handle other WSL paths that need to be mapped to Windows paths
    elif unix_path.startswith('/home/'):
        # Map /home/username/... to appropriate Windows path via WSL path
        return f'\\\\wsl$\\Ubuntu{unix_path}'.replace('/', '\\')

AHK_EXE = '/mnt/c/Program Files/AutoHotkey/v1.1.37.02/AutoHotkeyU32.exe'
AHK_EXE_WIN = unix_to_windows_path(AHK_EXE)

# --- Configure logging ---
# Create a log file in the same directory
LOG_FILE = os.path.join(BASE_DIR, 'helldivers_debug.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Function to log both to file and console
def debug_log(message):
    print(message)
    logging.debug(message)
    # Also write to a simple debug file
    with open(os.path.join(BASE_DIR, 'debug.txt'), 'a') as f:
        f.write(f"{message}\n")
        f.flush()  # Ensure it's written immediately

# --- Read loadouts.json and stratagems.json ---
def read_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read {path}: {e}")
        return None

# --- Write the AHK script for the selected loadout ---
def write_ahk(loadout, loadout_name="Unknown"):
    stratagems = read_json(STRATAGEMS_FILE)
    if stratagems is None:
        return
    ahk_lines = [
        '; Helldivers 2 Loadout: ' + loadout_name,
        '; Generated: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        '',
        '#SingleInstance Ignore',
        'SetKeyDelay, 50',
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
        
        # Add hotkey with stratagem name as comment if available
        ahk_lines.append(f'^{idx}:: ; {strat_name}')
        ahk_lines.append('Send, {l down}')
        ahk_lines.append('Sleep, 50')
        
        # Each direction key needs down/up events with sleep timings
        for dir in keys:
            key = direction_to_key_improved(dir)
            if not key:
                ahk_lines.append(f'; ERROR: Unknown direction: {dir}')
                continue
                
            # Key down event
            ahk_lines.append(f'Send, {{{key} down}}')
            ahk_lines.append('Sleep, 50')
            
            # Key up event
            ahk_lines.append(f'Send, {{{key} up}}')
            ahk_lines.append('Sleep, 50')
            
        ahk_lines.append('Send, {l up}')
        ahk_lines.append('Return')
        ahk_lines.append('')
        
    # Write the script
    with open(AHK_SCRIPT, 'w') as f:
        f.write('\n'.join(ahk_lines))

# --- Helper: Map direction to AHK key with improved format ---
def direction_to_key_improved(dir):
    return {
        'up': 'Up',
        'down': 'Down',
        'left': 'Left',
        'right': 'Right'
    }.get(dir, '')

# --- Reload the AHK script ---
def reload_ahk():
    debug_log("===== RELOAD AHK FUNCTION CALLED =====")
    debug_log(f"Current working directory: {os.getcwd()}")
    debug_log(f"BASE_DIR: {BASE_DIR}")
    debug_log(f"Generated Loadout Script Path: {AHK_SCRIPT}")
    debug_log(f"AHK Executable: {AHK_EXE}")
    debug_log(f"AHK Executable (Windows path): {AHK_EXE_WIN}")
    
    try:
        # Check if the files exist
        if not os.path.exists(AHK_SCRIPT):
            debug_log(f"ERROR: Script file not found: {AHK_SCRIPT}")
            raise FileNotFoundError(f"Script file not found: {AHK_SCRIPT}")
        else:
            debug_log(f"Script file exists: {AHK_SCRIPT}")
            
        if not os.path.exists(AHK_EXE):
            debug_log(f"ERROR: AutoHotkey executable not found: {AHK_EXE}")
            raise FileNotFoundError(f"AutoHotkey executable not found: {AHK_EXE}")
        else:
            debug_log(f"AHK executable exists: {AHK_EXE}")
        
        # Copy the AHK script to a Windows-accessible temp directory
        win_temp_dir = "/mnt/c/Windows/Temp"
        win_script_path = os.path.join(win_temp_dir, "generated_loadout.ahk")
        
        # Read the original script
        with open(AHK_SCRIPT, 'r') as src_file:
            script_content = src_file.read()
            
        # Write to Windows temp directory
        with open(win_script_path, 'w') as dst_file:
            dst_file.write(script_content)
            
        debug_log(f"Copied script to Windows temp directory: {win_script_path}")
        
        # Create a VBS script to launch AutoHotkey (handles paths with spaces better)
        vbs_content = f'''
Set WshShell = CreateObject("WScript.Shell")
' Launch the generated loadout script
WshShell.Run """C:\\Program Files\\AutoHotkey\\v1.1.37.02\\AutoHotkeyU32.exe"" ""C:\\Windows\\Temp\\generated_loadout.ahk""", 0, False
' Also launch the basic_strats script
WshShell.Run """C:\\Program Files\\AutoHotkey\\v1.1.37.02\\AutoHotkeyU32.exe"" ""C:\\Windows\\Temp\\basic_strats.ahk""", 0, False
'''

        # Also copy the basic_strats.ahk script to Windows temp if it exists
        basic_strats_path = os.path.join(BASE_DIR, 'basic_strats.ahk')
        if os.path.exists(basic_strats_path):
            debug_log(f"Basic strats script found: {basic_strats_path}")
            
            # Copy basic_strats.ahk to Windows temp directory
            win_basic_strats_path = os.path.join(win_temp_dir, "basic_strats.ahk")
            with open(basic_strats_path, 'r') as src_file:
                basic_strats_content = src_file.read()
                
            with open(win_basic_strats_path, 'w') as dst_file:
                dst_file.write(basic_strats_content)
                
            debug_log(f"Copied basic_strats script to Windows temp: {win_basic_strats_path}")
        else:
            debug_log(f"Basic strats script not found at {basic_strats_path}, will only run the generated script")
            # Update VBS to only run the generated script
            vbs_content = f'''
Set WshShell = CreateObject("WScript.Shell")
' Launch the generated loadout script only
WshShell.Run """C:\\Program Files\\AutoHotkey\\v1.1.37.02\\AutoHotkeyU32.exe"" ""C:\\Windows\\Temp\\generated_loadout.ahk""", 0, False
'''
        
        vbs_path = os.path.join(win_temp_dir, "launch_ahk.vbs")
        with open(vbs_path, 'w') as vbs_file:
            vbs_file.write(vbs_content)
        
        debug_log(f"Created VBS launcher: {vbs_path}")
        debug_log(f"VBS content: {vbs_content}")
        
        # Execute the VBS script
        cmd = f'cmd.exe /c "cscript //Nologo C:\\Windows\\Temp\\launch_ahk.vbs"'
        debug_log(f"Executing command: {cmd}")
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        debug_log(f"Subprocess result: {result}")
        
        # Try to get immediate output
        try:
            stdout, stderr = result.communicate(timeout=2)
            if stdout:
                debug_log(f"Process stdout: {stdout.decode('utf-8', errors='ignore')}")
            if stderr:
                debug_log(f"Process stderr: {stderr.decode('utf-8', errors='ignore')}")
        except subprocess.TimeoutExpired:
            debug_log("Process is still running (timeout expired)")
            pass
        
        status_label.config(text="AHK script running in the background.")
        debug_log("AHK script execution initiated successfully")
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        debug_log(f"ERROR DETAILS: {error_details}")
        messagebox.showerror("AHK Error", f"Could not reload AHK scripts: {e}\n\nDetails: {error_details}")

# --- On Listbox selection ---
def on_select(event):
    logging.debug("on_select triggered")
    selection = event.widget.curselection()
    logging.debug(f"Selection: {selection}")
    if not selection:
        messagebox.showerror("Selection Error", "No loadout selected.")
        return
    idx = selection[0]
    loadout_name = event.widget.get(idx)
    logging.debug(f"Selected loadout name: {loadout_name}")
    selected_label.config(text=f"Selected Loadout: {loadout_name}")
    loadouts = read_json(LOADOUTS_FILE)
    if loadouts is None:
        return
    if loadout_name not in loadouts:
        messagebox.showerror("Loadout Error", f"Loadout '{loadout_name}' not found in loadouts.json.")
        return
    loadout = loadouts[loadout_name]
    write_ahk(loadout, loadout_name)  # Pass the loadout name to write_ahk
    reload_ahk()
    status_label.config(text=f"Script generated and reloaded for loadout: {loadout_name}")
    logging.debug(f"Loadout selected: {loadout_name}, Loadout details: {loadout}")

# --- Build the Tkinter UI ---
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
    root.title("Helldivers 2 Loadout UI")
    tk.Label(root, text="Select Loadout:", font=("Arial", 12, "bold")).pack(pady=5)
    listbox = tk.Listbox(root, width=40, height=15, font=("Arial", 10))
    listbox.pack()
    # Populate listbox with loadout names
    loadouts = read_json(LOADOUTS_FILE)
    logging.debug(f"Loadouts loaded: {loadouts}")
    if loadouts:
        for name in sorted(loadouts.keys()):
            listbox.insert(tk.END, name)
    listbox.bind('<<ListboxSelect>>', on_select)
    global selected_label, status_label
    selected_label = tk.Label(root, text="Selected Loadout: None", font=("Arial", 12, "italic"), fg="blue")
    selected_label.pack(pady=10)
    status_label = tk.Label(root, text="Status: Waiting for selection", font=("Arial", 10), fg="green")
    status_label.pack(pady=5)
    tk.Button(root, text="Quit", command=root.quit, font=("Arial", 10)).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
