import tkinter as tk
import Data.Icons as Icons
from Models.Protein import Protein
from time import time

protein_names=["tofu", "shrimp", "salmon", "meat", "egg", "chicken"]

class Fire(tk.Frame):
    def __init__(self, parent) -> None:
        self.protein = None
        self.startTime = None



    def __str__(self) -> str:
        return f"Fire cooking {self.protein}" if self.protein is not None else "Fire is empty"
    

    def add_protein(self, protein: Protein) -> 'Fire':
        """
        Add protein to fire
        """

        self.protein = protein
        self.startTime = time()

        return self
    

    def remove_protein(self) -> int:
        """
        Remove protein from fire and mark it as cooked
        """

        if self.protein is None:
            return -1
        
        cookTime = time() - self.startTime
        self.protein.terminateCooking(cookTime)

        prot = self.protein
        self.protein = None
        self.startTime = None

        return prot

class ProteinBowl(tk.Frame):
    """A widget representing a single protein bowl with its canvas and icon."""
    def __init__(self, parent, protein_name):
        super().__init__(parent, highlightbackground="grey", highlightthickness=1, padx=5, pady=5)

        # --- Label for the protein ---
        label = tk.Label(self, text=protein_name.capitalize(), font=("Helvetica", 10))
        label.pack(pady=5)

        # --- Canvas Setup for this specific bowl ---
        self.bowl_canvas = tk.Canvas(self, width=120, height=120, highlightthickness=0)
        self.bowl_canvas.pack()
        
        # --- Icon Manager for this specific canvas ---
        self.icon_manager = Icons.Icons(self.bowl_canvas, size=(60, 60))
        
        # --- Draw the bowl and icon ---
        self.draw_bowl_and_icon(protein_name)

    def draw_bowl_and_icon(self, protein):
        """Draws the bowl shape and the protein icon on the canvas."""
        # Draw the bowl shape in the center of the 120x120 canvas
        self.bowl_canvas.create_oval(10, 10, 110, 110, fill="burlywood", outline="#8B4513", width=2)
        
        # Draw the icon in the center (60, 60)
        self.icon_manager.draw_icon(protein.lower(), 60, 60)



class Protein_Tab(tk.Frame):
    """Class where the user can select a protein option and cook it for the desired time
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Create a label for the protein tab
        label = tk.Label(self, text="Select Protein", font=("Helvetica", 16))
        label.pack(pady=10)
        
        # Create a container frame to hold all the bowl widgets
        bowls_container = tk.Frame(self)
        bowls_container.pack(pady=10, padx=10)
        
        # Step 3: Loop through the proteins and create a widget for each one
        for protein in protein_names:
            # Create an instance of our new ProteinBowl class
            bowl_widget = ProteinBowl(bowls_container, protein_name=protein)
            # Pack it to the left, allowing them to arrange horizontally
            bowl_widget.pack(side=tk.LEFT, padx=10, pady=5)
            continue
        
    

if __name__=="__main__":
    root = tk.Tk()
    app = Protein_Tab(parent=root, controller=None)
    app.pack(expand=True, fill="both")
    root.mainloop()
            
                    
        