import tkinter as tk

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
        
        # Create a listbox for extras and sauces selection
        self.extras_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.extras_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        
        