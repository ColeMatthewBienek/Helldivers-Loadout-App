import unittest
import os
import json
import sys
import tkinter as tk
from unittest import mock

sys.path.insert(0, os.path.dirname(__file__))
from loadout_ui import main, read_json, write_ahk, reload_ahk, AHK_SCRIPT, LOADOUTS_FILE, STRATAGEMS_FILE

class TestLoadoutUIWorkflow(unittest.TestCase):
    def setUp(self):
        # Minimal test data
        self.loadouts = {
            "Alpha": ["MG-43 Machine Gun", "Reinforce", "E/MG-101 HMG Emplacement", "Orbital Gatling Barrage"]
        }
        self.stratagems = {
            "Blue": {"MG-43 Machine Gun": ["down", "left", "down", "up", "right"]},
            "Yellow": {"Reinforce": ["up", "down", "right", "left", "up"]},
            "Green": {"E/MG-101 HMG Emplacement": ["down", "up", "left", "right", "right", "left"]},
            "Red": {"Orbital Gatling Barrage": ["right", "down", "left", "up", "up"]}
        }
        with open(LOADOUTS_FILE, 'w') as f:
            json.dump(self.loadouts, f)
        with open(STRATAGEMS_FILE, 'w') as f:
            json.dump(self.stratagems, f)
        if os.path.exists(AHK_SCRIPT):
            os.remove(AHK_SCRIPT)

    def tearDown(self):
        for f in [AHK_SCRIPT]:
            if os.path.exists(f):
                os.remove(f)

    @mock.patch("tkinter.messagebox.showinfo")
    @mock.patch("tkinter.messagebox.showerror")
    @mock.patch("subprocess.run")
    def test_full_workflow_select_loadout(self, mock_run, mock_showerror, mock_showinfo):
        # Simulate selecting the first loadout in the UI
        import loadout_ui
        root = tk.Tk()
        listbox = tk.Listbox(root)
        for name in sorted(self.loadouts.keys()):
            listbox.insert(tk.END, name)
        # Select the first item
        listbox.selection_set(0)
        event = mock.Mock()
        event.widget = listbox
        # Patch read_json to use our test data
        with mock.patch("loadout_ui.read_json", side_effect=[self.loadouts, self.stratagems]):
            loadout_ui.on_select(event)
        # Check that the AHK script was written
        self.assertTrue(os.path.exists(AHK_SCRIPT))
        with open(AHK_SCRIPT) as f:
            content = f.read()
        self.assertIn("^1::", content)
        self.assertIn("SendInput {L down}", content)
        # Check that reload_ahk (subprocess.run) was called
        mock_run.assert_called()
        # Check that showinfo was called for success
        mock_showinfo.assert_called()
        # No error should be shown
        mock_showerror.assert_not_called()
        root.destroy()

if __name__ == "__main__":
    unittest.main()
