import tkinter as tk

class Veg_Fruit_Tab(tk.Frame):
    """
    Class representing the vegetable and fruit selection tab in the Pookie GUI.
    Allows user to drag and drop vegetables and fruits into the bowl.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
       