import unittest
import os
import json
import sys
import tkinter as tk
from unittest import mock
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.dirname(__file__))
from loadout_ui import read_json, write_ahk, direction_to_key, LOADOUTS_FILE, STRATAGEMS_FILE, AHK_SCRIPT, on_select

class TestLoadoutUI(unittest.TestCase):
    def setUp(self):
        # Create minimal test data
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

        # Mock data for loadouts in UI tests
        with patch("loadout_ui.read_json", return_value=self.loadouts):
            self.root = tk.Tk()
            self.listbox = tk.Listbox(self.root)
            for name in sorted(self.loadouts.keys()):
                self.listbox.insert(tk.END, name)

    def tearDown(self):
        for f in [LOADOUTS_FILE, STRATAGEMS_FILE, AHK_SCRIPT]:
            if os.path.exists(f):
                os.remove(f)
        self.root.destroy()

    def test_read_json_loadouts(self):
        data = read_json(LOADOUTS_FILE)
        self.assertIn("Alpha", data)
        self.assertEqual(len(data["Alpha"]), 4)

    def test_direction_to_key(self):
        self.assertEqual(direction_to_key("up"), "{Up}")
        self.assertEqual(direction_to_key("down"), "{Down}")
        self.assertEqual(direction_to_key("left"), "{Left}")
        self.assertEqual(direction_to_key("right"), "{Right}")
        self.assertEqual(direction_to_key("foo"), "")

    def test_write_ahk_creates_script(self):
        loadout = self.loadouts["Alpha"]
        write_ahk(loadout)
        self.assertTrue(os.path.exists(AHK_SCRIPT))
        with open(AHK_SCRIPT) as f:
            content = f.read()
        self.assertIn("^1::", content)
        self.assertIn("SendInput {L down}", content)
        self.assertIn("SendInput {Up}", content)

    @mock.patch("subprocess.run")
    def test_reload_ahk_called(self, mock_run):
        # Import reload_ahk here to avoid circular import
        from loadout_ui import reload_ahk
        with open(AHK_SCRIPT, 'w') as f:
            f.write("dummy")
        reload_ahk()
        mock_run.assert_called()

    @patch("loadout_ui.write_ahk")
    @patch("loadout_ui.reload_ahk")
    @patch("tkinter.messagebox.showinfo")
    @patch("tkinter.messagebox.showerror")
    def test_on_select_success(self, mock_showerror, mock_showinfo, mock_reload_ahk, mock_write_ahk):
        # Simulate selecting the first loadout
        self.listbox.selection_set(0)
        event = Mock()
        event.widget = self.listbox
        on_select(event)

        # Verify that write_ahk and reload_ahk were called
        mock_write_ahk.assert_called_once()
        mock_reload_ahk.assert_called_once()

        # Verify that showinfo was called
        mock_showinfo.assert_called_once()

        # Verify that showerror was not called
        mock_showerror.assert_not_called()

    @patch("tkinter.messagebox.showerror")
    def test_on_select_no_selection(self, mock_showerror):
        # Simulate no selection
        event = Mock()
        event.widget = self.listbox
        with patch.object(event.widget, 'curselection', return_value=[]):
            on_select(event)

        # Verify that showerror was called with the correct arguments
        mock_showerror.assert_called_once_with("Selection Error", "No loadout selected.")

if __name__ == "__main__":
    unittest.main()
