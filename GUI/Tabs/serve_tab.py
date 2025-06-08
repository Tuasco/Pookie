import tkinter as tk

bg_color = "seashell"  # Background color for the tab

class Serve_Tab(tk.Frame):
    """Class representing the serve tab in the Pookie GUI.
    Takes the selected reciept and serves the dish to the affiliated client.
    Inherits from tkinter.Frame to create a frame for the serve tab."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=bg_color)
        self.controller = controller
        
        label = tk.Label(self, text="Serve Your Dish", font=self.controller.font_title, bg=bg_color)
        label.pack(pady=self.controller.padding)
    
        self.serve_button = tk.Button(self, text="Serve", font=self.controller.font_button, command=self.controller.serve_poke, bg="lightgreen", fg="white", borderwidth=0, highlightthickness=0, cursor="hand2")
        self.serve_button.pack(pady=self.controller.padding)