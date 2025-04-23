import tkinter as tk 
from Tabs import difficulty_tab, order_tab, base_tab, veg_fruit_tab, protein_tab, extras_sauces_tab, serve_tab

tab_classes=[difficulty_tab.Game_difficulty_Tab, 
             order_tab.Order_Tab, 
             base_tab.Base_Tab, 
             veg_fruit_tab.Veg_Fruit_Tab, 
             protein_tab.Protein_Tab, 
             extras_sauces_tab.Extras_Sauces_Tab, 
             serve_tab.Serve_Tab]

class Pookie(tk.Tk):
    """
    Principal class for the Pookie game GUI.
    Inherits from tkinter.Tk to create the main window.
    """
    def __init__(self):
        super().__init__()
        self.title("Pookie Game")
        self.geometry("800x600")   
        
        self.container = tk.Frame(self)
        
        self.pages= {}
        
        for page in tab_classes:
            # Dynamically create pages and store them in the pages dictionary
            page_name = page.__name__
            frame = page(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("Game_difficulty_Tab")
        
    def show_frame(self, page_name):
        """
        Show a frame for the given page name.
        """
        frame = self.pages[page_name]
        frame.tkraise()
        
    
