"""
main.py - Starting point of the AI Voice Assistant.
Run this file:  python main.py
"""

import tkinter as tk

from gui import VoiceAssistantApp


def main():
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()


if __name__ == "__main__":
    main()
