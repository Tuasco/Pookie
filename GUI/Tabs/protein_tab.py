import tkinter as tk

class Protein_Tab(tk.Frame):
    """Class where the user can select a protein option and cook it for the desired time
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a label for the protein tab
        label = tk.Label(self, text="Select Protein", font=("Helvetica", 16))
        label.pack(pady=10)
        
        # creates a cooking space for the protein