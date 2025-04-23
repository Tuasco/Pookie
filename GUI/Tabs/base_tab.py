import tkinter as tk

class Base_tab(tk.Frame):
    """ Class generating the base tab of the GUI.
    Allowing user to pick the base of the pokebowl.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a label for the base tab
        label = tk.Label(self, text="Select Base", font=("Helvetica", 16))
        label.pack(pady=10)
        
        # Create buttons for different base options
        #uses list, or file of base options to create buttons

