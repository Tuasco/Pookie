import tkinter as tk
import Data.Icons as Icons
from Models.Protein import Protein
from time import time
import math 

protein_names=["tofu", "shrimp", "salmon", "meat", "egg", "chicken"]
bg_color="seashell"  # Define a background color for the tab


class Fire(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        self.protein = None
        self.startTime = None
        self.controller = controller
        
        #timer constants
        RADIUS, NEEDLE_LENGTH, GRADUATION_LENGTH = controller.size_selection_icon*0.45, controller.size_selection_icon*0.4, controller.size_selection_icon*0.045
        WIDTH, HEIGHT= controller.size_selection_canvas, controller.size_selection_canvas

        # --- Functions ---

        def draw_graduations():
            """Draws 6 graduation marks on the timer face."""
            for i in range(6):
                angle = math.radians(i * 60 - 90) # Calculate angle for each of the 6 marks
                
                # Calculate the start and end points of the graduation line
                x_start = WIDTH / 2 + (RADIUS - GRADUATION_LENGTH) * math.cos(angle)
                y_start = HEIGHT / 2 + (RADIUS - GRADUATION_LENGTH) * math.sin(angle)
                x_end = WIDTH / 2 + RADIUS * math.cos(angle)
                y_end = HEIGHT / 2 + RADIUS * math.sin(angle)
                
                self.timer_canvas.create_line(x_start, y_start, x_end, y_end, fill="gray", width=2)
            
        def update_needle():
            """Updates the position of the timer needle and stops after 60 seconds."""
            global seconds_elapsed
            seconds_elapsed += 1
            
            # We use the modulo operator (%) to make the needle loop visually
            # while our counter handles the stopping.
            display_second = (seconds_elapsed) % 60
            
            angle = math.radians(display_second * 6 - 90)  # Convert second to angle
            
            x_center = WIDTH / 2
            y_center = HEIGHT / 2
            
            x_end = x_center + NEEDLE_LENGTH * math.cos(angle)
            y_end = y_center + NEEDLE_LENGTH * math.sin(angle)
            
            self.timer_canvas.coords(needle, x_center, y_center, x_end, y_end)
            
            # Only schedule the next update if the timer has not completed a full turn
            if seconds_elapsed < 60:
                controller.after(1000, update_needle)
                
        
        canvas_size = self.controller.size_selection_canvas
        self.wok_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg=bg_color)
        self.wok_canvas.pack()
        
        self.timer_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg=bg_color)
        self.timer_canvas.create_oval(canvas_size*0.25, canvas_size*0.25, canvas_size*0.75, canvas_size*0.75, outline="pink", width=4)
        draw_graduations()
        
        needle = self.timer_canvas.create_line(WIDTH / 2, HEIGHT / 2, WIDTH / 2 + NEEDLE_LENGTH, HEIGHT / 2, fill="red", width=3)
        self.timer_canvas.pack()
        
        
        icon_size = self.controller.size_selection_icon
        self.icon_manager = Icons.Icons(self.wok_canvas, size=(icon_size*2, icon_size*2))
        self.icon_manager.draw_icon("wokfire", canvas_size/2, canvas_size/2)
        
        seconds_elapsed = 0
        controller.after(1000, update_needle)  # Start the timer update loop




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
            
        fire_container = tk.Frame(self, bg=bg_color)
        fire_container.pack(pady=self.controller.padding, padx=self.controller.padding)
        for _ in range(-1, 3):
            wok_widget = Fire(fire_container, self.controller)
            wok_widget.pack(side="left", padx=self.controller.padding+20, pady=self.controller.padding)
        

if __name__=="__main__":
    root = tk.Tk()
    app = Protein_Tab(parent=root, controller=None)
    app.pack(expand=True, fill="both")
    root.mainloop()