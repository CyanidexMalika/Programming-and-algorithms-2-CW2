import unittest
from unittest.mock import patch
import tkinter as tk
import main

class TestMainMenu(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = main.MainMenu(self.root)

    @patch('main.subprocess.Popen')
    def test_open_ssh_tool(self, mock_popen):
        self.app.open_ssh_tool()
        mock_popen.assert_called_once()

    @patch('main.subprocess.Popen')
    def test_open_directory_tool(self, mock_popen):
        self.app.open_directory_tool()
        mock_popen.assert_called_once()

    def test_exit_application(self):
        with self.assertRaises(tk.TclError):  # Expecting a TclError when accessing destroyed window
            self.app.exit_application()
            self.root.winfo_exists()  # Attempting to access destroyed root window

if __name__ == '__main__':
    unittest.main()
