import tkinter as tk

class Game_difficulty_Tab(tk.Frame):
    """
    Class representing the game difficulty tab in the Pookie GUI.
    Inherits from tkinter.Tk to create the main window.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
         # Title
        title = tk.Label(self, text="Choose\ndifficulty", font=("Helvetica", 24), justify="center")
        title.pack(pady=40)
        
        # Difficulty selection
        self.difficulty = tk.StringVar(value="easy")  # default

        options = [("easy", "easy"), ("medium", "medium"), ("hard", "hard")]
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        # Button to confirm selection
        
        def confirm_difficulty():
            # Store the selected difficulty in the controller
            selected = self.difficulty.get()
            self.controller.game_difficulty = selected  # <— store it globally
            self.controller.show_frame("Order_Tab")     # go to next tab

        confirm_button = tk.Button(self, text="Confirm", command=confirm_difficulty, font=("Helvetica", 16))
        confirm_button.pack(pady=20)

        for text, value in options:
            rb = tk.Radiobutton(button_frame, text=text, variable=self.difficulty, value=value, font=("Helvetica", 16))
            rb.pack(side="left", padx=20)
    

        
if __name__=="__main__":
    root = tk.Tk()
    app = Game_difficulty_Tab(parent=root, controller=None)
    app.pack(expand=True, fill="both")
    root.mainloop()