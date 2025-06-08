import tkinter as tk
import Data.Icons as Icons
from Models.Protein import Protein
from time import time

protein_names=["tofu", "shrimp", "salmon", "meat", "egg", "chicken"]
bg_color="seashell"  # Define a background color for the tab


class Fire(tk.Frame):
    def __init__(self, parent) -> None:
        self.protein = None
        self.startTime = None


    def __str__(self) -> str:
        return f"Fire cooking {self.protein}" if self.protein is not None else "Fire is empty"
    

    def add_protein(self, protein: Protein) -> 'Fire':
        """Add protein to fire."""

        self.protein = protein
        self.startTime = time()

        return self
    

    def remove_protein(self) -> int:
        """Remove protein from fire and mark it as cooked."""

        if self.protein is None:
            return -1
        
        cookTime = time() - self.startTime
        self.protein.terminateCooking(cookTime)

        prot = self.protein
        self.protein = None
        self.startTime = None

        return prot

class ProteinBowl(tk.Frame):
    def __init__(self, parent, protein_name, controller):
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        self.protein_name = protein_name
        self.controller = controller

        label = tk.Label(self, text=protein_name.capitalize(), font=self.controller.font_label, bg=bg_color, fg="saddlebrown")
        label.pack(pady=5)

        canvas_size = self.controller.size_selection_canvas
        self.bowl_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg=bg_color)
        self.bowl_canvas.pack()
        
        icon_size = self.controller.size_selection_icon
        self.icon_manager = Icons.Icons(self.bowl_canvas, size=(icon_size, icon_size))
        self.draw_bowl_and_icon(protein_name)

    def draw_bowl_and_icon(self, protein):
        canvas_size = self.controller.size_selection_canvas
        padding = int(canvas_size * 0.08)
        self.bowl_canvas.create_oval(padding, padding, canvas_size-padding, canvas_size-padding, fill="burlywood", outline="#8B4513", width=2)
        self.icon_manager.draw_icon(protein.lower(), canvas_size/2, canvas_size/2)

class Protein_Tab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=bg_color)
        self.controller = controller
        
        label = tk.Label(self, text="Select Protein", font=self.controller.font_title, bg=bg_color)
        label.pack(pady=self.controller.padding)
        
        bowls_container = tk.Frame(self, bg=bg_color)
        bowls_container.pack(pady=self.controller.padding, padx=self.controller.padding)
        
        for protein in protein_names:
            bowl_widget = ProteinBowl(bowls_container, protein_name=protein, controller=self.controller)
            bowl_widget.pack(side=tk.LEFT, padx=self.controller.padding, pady=self.controller.padding)

if __name__=="__main__":
    root = tk.Tk()
    app = Protein_Tab(parent=root, controller=None)
    app.pack(expand=True, fill="both")
    root.mainloop()