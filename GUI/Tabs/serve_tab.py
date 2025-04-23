import tkinter as tk

class Serve_Tab(tk.Frame):
    """
    Class representing the serve tab in the Pookie GUI.
    Takes the selected reciept and serves the dish to the affiliated client.
    Inherits from tkinter.Frame to create a frame for the serve tab.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a label for the serve tab
        label = tk.Label(self, text="Serve Your Dish", font=("Helvetica", 16))
        label.pack(pady=10)
    
        
        # Create a button to serve the dish
        self.serve_button = tk.Button(self, text="Serve", command=self.serve_dish)
        self.serve_button.pack(pady=10)