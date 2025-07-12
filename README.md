# 🚀 HELLDIVERS 2 STRATAGEM MASTER 🚀

![Helldivers 2 Banner](https://cdn.akamai.steamstatic.com/steam/apps/553850/header.jpg)

**FOR DEMOCRACY! FOR SUPER EARTH!** A lightning-fast stratagem automation tool for the elite Helldivers who don't have time for pesky manual key entries in the heat of battle!

## ⚡ Overview

Stratagem Master is a powerful WSL-based automation tool that lets you execute complex Helldivers 2 stratagems with a single keypress. This tool allows you to:

- Create custom loadouts with your favorite stratagems
- Trigger complex stratagem sequences with a single hotkey (Ctrl+1 through Ctrl+9)
- Run both primary loadouts and utility stratagems simultaneously
- Customize key timing for optimal game performance

## 🛠️ Installation Requirements

- Windows 10/11 with WSL (Windows Subsystem for Linux)
- Python 3.6+
- AutoHotkey v1.1.37.02+ installed on Windows
- Helldivers 2 (obviously)

## 🔥 Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/helldivers_strats.git
   cd helldivers_strats
   ```

2. **Install Python requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure AutoHotkey is installed**
   - Download and install from [AutoHotkey Website](https://www.autohotkey.com/) if you don't have it
   - Default path should be: `C:\Program Files\AutoHotkey\v1.1.37.02\AutoHotkeyU32.exe`

## 💥 Usage

1. **Launch the application**
   ```bash
   cd data
   python loadout_ui.py
   ```

2. **Select your loadout** from the UI window

3. **RAIN HELL ON THE ENEMIES OF SUPER EARTH!**
   - Use `Ctrl+1` through `Ctrl+9` for your main loadout stratagems
   - Use `Alt+1` through `Alt+7` for utility stratagems (defined in basic_strats.ahk)

## ⚙️ Configuration

### Customize Loadouts

Edit the `data/loadouts.json` file to create custom stratagem loadouts:

```json
{
  "Anti-Tank": [
    "EAT-17 Expendable Anti-tank",
    "GR-8 Recoilless Rifle",
    "RS-422 Railgun",
    "Orbital 380MM HE Barrage"
  ],
  "Bug Smasher": [
    "Orbital Gatling Barrage",
    "Eagle Cluster Bomb",
    "Orbital Napalm Barrage",
    "A/MG-43 Machine Gun Sentry"
  ]
}
```

### Customize Basic Stratagems

The `basic_strats.ahk` file contains utility stratagems bound to Alt keys:

- `Alt+1`: SSSD Delivery
- `Alt+2`: Seismic Probe
- `Alt+3`: Upload Data
- `Alt+4`: NUX-223 Hellbomb
- `Alt+5`: SEAF Artillery
- `Alt+6`: Prospecting Drill
- `Alt+7`: Tectonic Drill

## ⚠️ Important Notes

- The application writes scripts to Windows temp directory for execution
- Ensure you're running the game in windowed or borderless mode for hotkeys to work
- If hotkeys don't respond, check the debug.txt file for troubleshooting
- Timing settings are tuned for optimal stratagem execution speed

## 🔄 Advanced Configuration

### Key Timing Adjustment

Fine-tune key timing in both scripts:
- `SetKeyDelay, 50` sets the global delay
- `Sleep, 50` determines pause between key presses

Lower values = faster execution but may cause missed inputs in-game.

## 🛡️ License

MIT License - See LICENSE file for details

## 🌟 Contributions

Contributions welcome! Submit PRs or open issues to enhance this tool for all Helldivers!

---

*"Managed democracy is the best democracy!" - Helldivers 2*
