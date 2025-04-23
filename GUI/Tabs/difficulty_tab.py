import tkinter as tk

class Game_difficulty_Tab(tk.Frame):
    """
    Class representing the game difficulty tab in the Pookie GUI.
    Inherits from tkinter.Tk to create the main window.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Create a label for the game difficulty tab
        label = tk.Label(self, text="Select Game Difficulty", font=("Helvetica", 16))
        label.pack(pady=10)
        
        # Create buttons for different difficulty levels
        button1 = tk.Button(self, text="Easy", command=lambda: self.set_difficulty("Easy"))
        button1.pack(pady=5)
        
        button2 = tk.Button(self, text="Medium", command=lambda: self.set_difficulty("Medium"))
        button2.pack(pady=5)
        
        button3 = tk.Button(self, text="Hard", command=lambda: self.set_difficulty("Hard"))
        button3.pack(pady=5)
        
if __name__=="__main__":
    root = tk.Tk()
    app = Game_difficulty_Tab(parent=root, controller=None)
    app.pack(expand=True, fill="both")
    root.mainloop()