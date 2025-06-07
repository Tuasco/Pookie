import tkinter as tk
from Data.Icons import Icons

veggies= ["carrot", "broccoli", "beet", "tomato", "cucumber", "mushroom", "onion", "peas"]
fruits = ["dragon fruit", "melon", "watermelon", "grape", "kiwi", "avocado", "raspberry"]

class Veg_Fruit_Tab(tk.Frame):
    """
    Class representing the vegetable and fruit selection tab in the Pookie GUI.
    Allows user to drag and drop vegetables and fruits into the bowl.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Create a label for the Veggies
        label = tk.Label(self, text="Select Veggies", font=("Helvetica", 16))
        label.pack(pady=10)
        
        # Create a container frame to hold all the bowl widgets
        veg_container = tk.Frame(self)
        veg_container.pack(pady=10, padx=10)
        
        # Create a label for the Fruits
        label = tk.Label(self, text="Select Fruits", font=("Helvetica", 16))
        label.pack(pady=10)
        
        fruits_container = tk.Frame(self)
        fruits_container.pack(pady=10, padx=10)  
        
        # Step 3: Loop through the veggies and fruits and create a widget for each one
        for veggie in veggies:
            # Create an instance of our new VegFruitBowl class
            bowl_widget = VegFruitBowl(veg_container, veg_fruit_name=veggie)
            # Pack it to the left, allowing them to arrange horizontally
            bowl_widget.pack(side=tk.LEFT, padx=10, pady=5)
            continue
        for fruit in fruits:
            # Create an instance of our new VegFruitBowl class
            bowl_widget = VegFruitBowl(fruits_container, veg_fruit_name=fruit)
            # Pack it to the left, allowing them to arrange horizontally
            bowl_widget.pack(side=tk.LEFT, padx=10, pady=5)
            continue
       
       
class VegFruitBowl(tk.Frame):
    """A widget representing a single vegetable/fruit bowl with its canvas and icon."""
    def __init__(self, parent, veg_fruit_name):
        super().__init__(parent, highlightbackground="grey", highlightthickness=1, padx=5, pady=5)

        # --- Label for the vegetable/fruit ---
        label = tk.Label(self, text=veg_fruit_name.capitalize(), font=("Helvetica", 10))
        label.pack(pady=5)

        # --- Canvas Setup for this specific bowl ---
        self.bowl_canvas = tk.Canvas(self, width=120, height=120, highlightthickness=0)
        self.bowl_canvas.pack()
        
        # --- Icon Manager for this specific canvas ---
        self.icon_manager = Icons(self.bowl_canvas, size=(60, 60))
        
        # --- Draw the bowl and icon ---
        self.draw_bowl_and_icon(veg_fruit_name.replace(" ", "_"))  # Replace spaces with underscores for icon names

    def draw_bowl_and_icon(self, veg_fruit):
        """Draws the bowl shape and the vegetable/fruit icon on the canvas."""
        # Draw the bowl shape in the center of the 120x120 canvas
        self.bowl_canvas.create_oval(10, 10, 110, 110, fill="burlywood", outline="#8B4513", width=2)
        
        # Draw the icon in the center (60, 60)
        self.icon_manager.draw_icon(veg_fruit.lower(), 60, 60)