import tkinter as tk
from tkinterweb import HtmlFrame
import os

# Create the main application window
root = tk.Tk()
root.title("Portfolio Viewer")
root.geometry("850x550")
root.resizable(False, False)

# Create an instance of HtmlFrame
frame = HtmlFrame(root, horizontal_scrollbar="auto")
frame.pack(fill="both", expand=True)

# Get the absolute path to the HTML file
html_file_path = os.path.join(os.path.dirname(__file__), "webFile", "working.html")

# Load the HTML file
frame.load_file(html_file_path)

# Start the Tkinter main loop
root.mainloop()
