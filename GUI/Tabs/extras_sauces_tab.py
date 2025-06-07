import tkinter as tk
from Data.Icons import Icons

extra_names = ["edamame", "mint", "lemon", "corn"]
sauce_names = ["soy sauce", "sriracha", "lemon sauce", "spicy mayo", "wasabi"]

class Extras_Sauces_Tab(tk.Frame):
    """
    Class representing the extras and sauces tab in the Pookie GUI.
    Inherits from tkinter.Frame to create a frame for the extras and sauces tab.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a label for the extras and sauces tab
        label = tk.Label(self, text="Select Extras", font=("Helvetica", 16))
        label.pack(pady=10)
        
        # Create a container frame to hold all the bowl widgets
        extras_container = tk.Frame(self)
        extras_container.pack(pady=10, padx=10)
        
        label = tk.Label(self, text="Select Sauces", font=("Helvetica", 16))
        label.pack(pady=10)
        
        sauces_container = tk.Frame(self)
        sauces_container.pack(pady=10, padx=10)
        
        # Create a widget for each extra and sauce
        for extra in extra_names:
            bowl_widget = ExtrasSaucesBowl(extras_container, extra_name=extra)
            bowl_widget.pack(side=tk.LEFT, padx=10, pady=5)
            
        for sauce in sauce_names:
            bowl_widget = ExtrasSaucesBowl(sauces_container, extra_name=sauce)
            bowl_widget.pack(side=tk.LEFT, padx=10, pady=5)
            
        
        
        
class ExtrasSaucesBowl(tk.Frame):
    """A widget representing a single extra/sauce bowl with its canvas and icon."""
    def __init__(self, parent, extra_name):
        super().__init__(parent, highlightbackground="grey", highlightthickness=1, padx=5, pady=5)

        # --- Label for the extra/sauce ---
        label = tk.Label(self, text=extra_name.capitalize(), font=("Helvetica", 10))
        label.pack(pady=5)

        # --- Canvas Setup for this specific bowl ---
        self.bowl_canvas = tk.Canvas(self, width=120, height=120, highlightthickness=0)
        self.bowl_canvas.pack()

        self.icon_manager = Icons(self.bowl_canvas, size=(60, 60))
        self.draw_bowl_and_icon(extra_name)

    def draw_bowl_and_icon(self, extra):
        """Draws the bowl shape and the extra/sauce icon on the canvas."""

        self.bowl_canvas.create_oval(10, 10, 110, 110, fill="burlywood", outline="#8B4513", width=2)
        self.icon_manager.draw_icon(extra.lower(), 60, 60)