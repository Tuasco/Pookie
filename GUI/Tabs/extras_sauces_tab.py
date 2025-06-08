import tkinter as tk
from Data.Icons import Icons

extra_names = ["edamame", "mint", "lemon", "corn", "sesame"]
sauce_names = ["soy sauce", "sriracha", "sour cream", "wasabi"]

bg_color = "seashell"  # Background color for the tab

class Extras_Sauces_Tab(tk.Frame):
    """
    Class representing the extras and sauces tab in the Pookie GUI.
    Inherits from tkinter.Frame to create a frame for the extras and sauces tab.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=bg_color)
        self.controller = controller
        
        # Create a label for the extras and sauces tab
        label = tk.Label(self, text="Select Extras", font=("Helvetica", 16), bg=bg_color)
        label.pack(pady=10)
        
        # Create a container frame to hold all the bowl widgets
        extras_container = tk.Frame(self, bg=bg_color)
        extras_container.pack(pady=10, padx=10)
        
        label = tk.Label(self, text="Select Sauces", font=("Helvetica", 16), bg=bg_color)
        label.pack(pady=10)
        
        sauces_container = tk.Frame(self, bg=bg_color)
        sauces_container.pack(pady=10, padx=10)
        
        # Create a widget for each extra and sauce
        for extra in extra_names:
            bowl_widget = ExtrasSaucesBowl(extras_container, item_name=extra, controller=self.controller)
            bowl_widget.pack(side=tk.LEFT, padx=10, pady=5)
            
        for sauce in sauce_names:
            bowl_widget = ExtrasSaucesBowl(sauces_container, item_name=sauce, controller=self.controller)
            bowl_widget.pack(side=tk.LEFT, padx=10, pady=5)
            
        
class ExtrasSaucesBowl(tk.Frame):
    """A widget representing a single extra/sauce bowl with its canvas and icon."""
    def __init__(self, parent, item_name, controller):
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        self.item_name = item_name
        self.controller = controller

        # --- Label for the extra/sauce ---
        label = tk.Label(self, text=item_name.capitalize(), font=("Helvetica", 12), bg=bg_color, fg="saddlebrown")
        label.pack(pady=5)

        # --- Canvas Setup for this specific bowl ---
        self.bowl_canvas = tk.Canvas(self, width=120, height=120, highlightthickness=0, bg=bg_color)
        self.bowl_canvas.pack()

        self.icon_manager = Icons(self.bowl_canvas, size=(60, 60))

        # Conditionally bind events and draw icons
        if self.item_name in extra_names:
            self.draw_bowl_and_icon(self.item_name.replace(" ", "_"))
            # Make the widget clickable if it's an extra
            self.bowl_canvas.config(cursor="hand2")
            self.bowl_canvas.bind("<Button-1>", self.on_select_extra)
            label.bind("<Button-1>", self.on_select_extra)
        else: # It's a sauce
            self.draw_icon(self.item_name.replace(" ", "_").lower())
            # Make the widget clickable if it's a sauce
            self.bowl_canvas.config(cursor="hand2")
            self.bowl_canvas.bind("<Button-1>", self.on_select_sauce)
            label.bind("<Button-1>", self.on_select_sauce)
            
    def draw_bowl_and_icon(self, extra):
        """Draws the bowl shape and the extra/sauce icon on the canvas."""
        self.bowl_canvas.create_oval(10, 10, 110, 110, fill="burlywood", outline="saddlebrown", width=2)
        self.icon_manager.draw_icon(extra.lower(), 60, 60)

    def draw_icon(self, sauce):
        """Draws the sauce icon on the canvas."""
        self.icon_manager.draw_icon(sauce, 60, 60)

    def on_select_extra(self, event):
        """When this extra is clicked, set it up for placement."""
        self.controller.set_ingredient_for_placement(self.item_name)

    def on_select_sauce(self, event):
        """When this sauce is clicked, set it up for drawing."""
        self.controller.set_sauce_for_drawing(self.item_name)