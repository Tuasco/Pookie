import tkinter as tk

extra_names = ["edamame", "mint", "lemon", "corn"]
class Extras_Sauces_Tab(tk.Frame):
    """
    Class representing the extras and sauces tab in the Pookie GUI.
    Inherits from tkinter.Frame to create a frame for the extras and sauces tab.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a label for the extras and sauces tab
        label = tk.Label(self, text="Select Extras and Sauces", font=("Helvetica", 16))
        label.pack(pady=10)
        
        # Create a container frame to hold all the bowl widgets
        extras_container = tk.Frame(self)
        extras_container.pack(pady=10, padx=10)
        sauces_container = tk.Frame(self)
        sauces_container.pack(pady=10, padx=10)
        # Step 3: Loop through the extras and sauces and create a widget for each one
        
        
        
        