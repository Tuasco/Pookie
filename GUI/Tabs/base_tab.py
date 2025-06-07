import tkinter as tk
from Data.Icons import Icons

base_names = ["salad"] #, "rice", "quinoa", "pasta"]

class Base_Tab(tk.Frame):
    """Class generating the base tab of the GUI. Allowing user to pick the base of the pokebowl."""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Add the "+ New Bowl" button here ---
        new_bowl_button = tk.Button(
            self, 
            text="+ New Bowl", 
            font=("Helvetica", 12, "bold"),
            command=self.controller.add_new_bowl  # This calls the method in main_window.py
        )
        new_bowl_button.pack(side="left" ,pady=20, padx=10)

        # --- Separator for clarity ---
        separator = tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=5)
        
        # Title label
        label = tk.Label(self, text="Select Base", font=("Helvetica", 16))
        label.pack(pady=10)
        
        # Create a container frame to hold all the bowl widgets
        bowls_container = tk.Frame(self)
        bowls_container.pack(pady=10, padx=10)
        
        # Step 3: Loop through the base and create a widget for each one
        for base in base_names:
            # Create an instance of our new BaseBowl class
            bowl_widget = BaseBowl(bowls_container, base_name=base)
            # Pack it to the left, allowing them to arrange horizontally
            bowl_widget.pack(side=tk.LEFT, padx=10, pady=5)
            continue

class BaseBowl(tk.Frame):
    """A widget representing a single Base Bowl with its canvas and icon."""
    def __init__(self, parent, base_name):
        super().__init__(parent, highlightbackground="grey", highlightthickness=1, padx=5, pady=5)

        # --- Label for the base ---
        label = tk.Label(self, text=base_name.capitalize(), font=("Helvetica", 10))
        label.pack(pady=5)

        # --- Canvas Setup for this specific bowl ---
        self.bowl_canvas = tk.Canvas(self, width=120, height=120, highlightthickness=0)
        self.bowl_canvas.pack()
        
        # --- Icon Manager for this specific canvas ---
        self.icon_manager = Icons(self.bowl_canvas, size=(60, 60))
        
        # --- Draw the bowl and icon ---
        self.draw_bowl_and_icon(base_name)

    def draw_bowl_and_icon(self, base):
        """Draws the bowl shape and the base icon on the canvas."""
        # Draw the bowl shape in the center of the 120x120 canvas
        self.bowl_canvas.create_oval(10, 10, 110, 110, fill="burlywood", outline="#8B4513", width=2)
        
        # Draw the icon in the center (60, 60)
        self.icon_manager.draw_icon(base.lower(), 60, 60)
