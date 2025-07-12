import unittest
import os
import json
import sys
import tkinter as tk
from unittest import mock

sys.path.insert(0, os.path.dirname(__file__))
from loadout_ui import read_json, write_ahk, direction_to_key, LOADOUTS_FILE, STRATAGEMS_FILE, AHK_SCRIPT

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

    def tearDown(self):
        for f in [LOADOUTS_FILE, STRATAGEMS_FILE, AHK_SCRIPT]:
            if os.path.exists(f):
                os.remove(f)

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

if __name__ == "__main__":
    unittest.main()
