import unittest
import subprocess
import os
from unittest.mock import patch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AHK_SCRIPT = os.path.join(BASE_DIR, 'generated_loadout.ahk')
AHK_EXE = '/mnt/c/Program Files/AutoHotkey/v1.1.37.02/AutoHotkeyU32.exe'

def reload_ahk():
    try:
        subprocess.run([AHK_EXE, AHK_SCRIPT], check=True)
    except Exception as e:
        raise RuntimeError(f"Could not reload AHK script: {e}")

class TestReloadAHK(unittest.TestCase):
    @patch('subprocess.run')
    def test_reload_ahk_success(self, mock_run):
        mock_run.return_value = None
        try:
            reload_ahk()
        except RuntimeError:
            self.fail("reload_ahk() raised RuntimeError unexpectedly!")

    @patch('subprocess.run', side_effect=Exception("Test Exception"))
    def test_reload_ahk_failure(self, mock_run):
        with self.assertRaises(RuntimeError):
            reload_ahk()

if __name__ == "__main__":
    unittest.main()
