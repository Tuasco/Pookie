import tkinter as tk
import sys
sys.path.append("../../Data")  # Adjust the path to import Icons from the parent directory
from ...Data.Icons import Icons

class Base_Tab(tk.Frame):
    """Class generating the base tab of the GUI. Allowing user to pick the base of the pokebowl."""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Title label
        label = tk.Label(self, text="Select Base", font=("Helvetica", 16))
        label.pack(pady=10)
        
        # Create a canvas to draw icons
        self.canvas = tk.Canvas(self, width=400, height=300, bg="white")
        self.canvas.pack(pady=20)

        # Load icons using the Icons class
        self.icons = Icons(self.canvas)

        # Draw an example icon, e.g. "salad"
        self.icons.draw_icon("salad", 200, 150)  # Adjust position as needed

