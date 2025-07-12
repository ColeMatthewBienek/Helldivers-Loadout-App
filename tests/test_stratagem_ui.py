
import unittest
import os
import json
import sys
import shutil
import tkinter as tk
from stratagem_ui import StratagemApp, LOADOUT_FILE, STRATAGEM_FILE


class TestStratagemApp(unittest.TestCase):
    def setUp(self):
        # Remove loadout file before each test
        if os.path.exists(LOADOUT_FILE):
            os.remove(LOADOUT_FILE)
        self.root = tk.Tk()
        self.app = StratagemApp(self.root)

    def tearDown(self):
        self.root.destroy()
        if os.path.exists(LOADOUT_FILE):
            os.remove(LOADOUT_FILE)

    def test_stratagem_count(self):
        # Should load more than 0 stratagems
        self.assertGreater(len(self.app.stratagems), 0)

    def test_select_and_save_loadout(self):
        # Simulate selecting 4 stratagems
        for i in range(4):
            self.app.listbox.selection_set(i)
        # Patch dialog
        self.app.root.withdraw()
        import tkinter.simpledialog
        tkinter.simpledialog.askstring = lambda *a, **k: "TestLoadout"
        self.app.save_loadout()
        # Check file
        with open(LOADOUT_FILE) as f:
            data = json.load(f)
        self.assertIn("TestLoadout", data)
        self.assertEqual(len(data["TestLoadout"]), 4)

    def test_invalid_selection(self):
        # Select 3 stratagems
        for i in range(3):
            self.app.listbox.selection_set(i)
        # Patch dialog
        self.app.root.withdraw()
        import tkinter.messagebox
        tkinter.messagebox.showerror = lambda *a, **k: None
        self.app.save_loadout()
        self.assertFalse(os.path.exists(LOADOUT_FILE))

if __name__ == "__main__":
    unittest.main()
