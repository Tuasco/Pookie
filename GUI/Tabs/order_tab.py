import tkinter as tk

class Order_Tab(tk.Frame):
    """
    Class representing the order tab in the Pookie GUI.
    Inherits from tkinter.Frame to create a frame for the order tab.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        