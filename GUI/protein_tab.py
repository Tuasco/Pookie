import tkinter as tk
import math

import Data.Icons as Icons
from Models.Protein import Protein
from Services.bowl_service import set_ingredient_for_placement
from Services.workspace_service import draw_bowl_and_icon

protein_names=["tofu", "shrimp", "salmon", "meat", "egg", "chicken"]
bg_color="seashell"  # Define a background color for the tab


class Fire(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        self.protein_name = None
        self.controller = controller
        self.seconds_elapsed = 0
        
        #timer constants
        RADIUS, NEEDLE_LENGTH, GRADUATION_LENGTH = controller.size_selection_icon*0.45, controller.size_selection_icon*0.4, controller.size_selection_icon*0.045
        WIDTH, HEIGHT= controller.size_selection_canvas, controller.size_selection_canvas

        # --- Functions ---
        def draw_graduations():
            """Draws 6 graduation marks on the timer face."""
            for i in range(6):
                angle = math.radians(i * 60 - 90)
                x_start = WIDTH / 2 + (RADIUS - GRADUATION_LENGTH) * math.cos(angle)
                y_start = HEIGHT / 2 + (RADIUS - GRADUATION_LENGTH) * math.sin(angle)
                x_end = WIDTH / 2 + RADIUS * math.cos(angle)
                y_end = HEIGHT / 2 + RADIUS * math.sin(angle)
                self.timer_canvas.create_line(x_start, y_start, x_end, y_end, fill="gray", width=2)
            
        def update_needle():
            """Updates the position of the timer needle and stops after 60 seconds."""
            if self.protein_name is None:
                self.seconds_elapsed = 0
            elif self.seconds_elapsed < 60:
                self.seconds_elapsed += 1

            display_second = (self.seconds_elapsed) % 60
            angle = math.radians(display_second * 6 - 90)
            x_center = WIDTH / 2
            y_center = HEIGHT / 2
            x_end = x_center + NEEDLE_LENGTH * math.cos(angle)
            y_end = y_center + NEEDLE_LENGTH * math.sin(angle)
            self.timer_canvas.coords(needle, x_center, y_center, x_end, y_end)
            
            controller.after(1000, update_needle)
                
        
        canvas_size = self.controller.size_selection_canvas
        self.wok_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg=bg_color)
        self.wok_canvas.pack()
        self.wok_canvas.bind("<Button-1>", self.on_select)
        
        self.timer_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg=bg_color)
        self.timer_canvas.create_oval(canvas_size*0.25, canvas_size*0.25, canvas_size*0.75, canvas_size*0.75, outline="pink", width=4)
        draw_graduations()
        
        needle = self.timer_canvas.create_line(WIDTH / 2, HEIGHT / 2, WIDTH / 2, HEIGHT / 2 - NEEDLE_LENGTH, fill="red", width=3)
        self.timer_canvas.pack()
        
        icon_size = self.controller.size_selection_icon
        
        # A large one for the background fire effect
        self.wok_icon_manager = Icons.Icons(self.wok_canvas, size=(icon_size*2, icon_size*2))
        # A smaller one for the protein, to fit inside the wok
        self.protein_icon_manager = Icons.Icons(self.wok_canvas, size=(icon_size, icon_size))
        
        self.set_display("wokfire")
        
        controller.after(1000, update_needle)


    def set_display(self, icon_name: str):
        """Clears the canvas and draws the wok, with a protein on top if specified."""
        canvas_size = self.controller.size_selection_canvas
        self.wok_canvas.delete("all") # Always start with a clean slate

        # Layer 1: Always draw the background wok/fire icon
        self.wok_icon_manager.draw_icon("wokfire", canvas_size/2, canvas_size/2)
        
        # Layer 2: If the icon is a protein, draw it on top
        if icon_name.lower() != "wokfire":
            self.protein_icon_manager.draw_icon(icon_name.lower(), canvas_size/2, canvas_size/2)


    def __str__(self) -> str:
        return f"Fire cooking {self.protein_name}" if self.protein_name is not None else "Fire is empty"
    

    def add_protein(self, protein_name: str) -> bool:
        """Add protein to fire."""
        if self.protein_name is not None:
            return False

        self.protein_name = protein_name
        self.seconds_elapsed = 0
        
        self.set_display(protein_name)
        

        return True
    
    def remove_protein(self) -> Protein:
        """Remove protein from fire and mark it as cooked."""
        if self.protein_name is None:
            return None
        
        protein = Protein(self.protein_name, (0, 0), math.floor(self.seconds_elapsed / 10))

        self.protein_name = None
        self.seconds_elapsed = 0
        
        self.set_display("wokfire")

        return protein
    

    def on_select(self, event):
        if self.protein_name is None:
            return
        
        set_ingredient_for_placement(self. controller, self.remove_protein())
    

class ProteinBowl(tk.Frame):
    def __init__(self, parent, protein_name, controller, tab):
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        self.protein_name = protein_name
        self.controller = controller
        self.parent = tab

        label = tk.Label(self, text=protein_name.capitalize(), font=self.controller.font_label, bg=bg_color, fg="saddlebrown")
        label.pack(pady=5)

        canvas_size = self.controller.size_selection_canvas
        self.bowl_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg=bg_color)
        self.bowl_canvas.pack()
        
        icon_size = self.controller.size_selection_icon
        self.icon_manager = Icons.Icons(self.bowl_canvas, size=(icon_size, icon_size))
        draw_bowl_and_icon(self, protein_name)
        self.bowl_canvas.config(cursor="hand2")
        self.bowl_canvas.bind("<Button-1>", self.on_select_protein)
        label.bind("<Button-1>", self.on_select_protein)


    def on_select_protein(self, event):
        print(f"Selected protein: {self.protein_name}")
        self.parent.assign_wok(self.protein_name)


class Protein_Tab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=bg_color)
        self.controller = controller
        
        label = tk.Label(self, text="Select Protein", font=self.controller.font_title, bg=bg_color)
        label.pack(pady=self.controller.padding)
        
        self.bowls_container = tk.Frame(self, bg=bg_color)
        self.bowls_container.pack(pady=self.controller.padding, padx=self.controller.padding)
        
        for protein in protein_names:
            bowl_widget = ProteinBowl(self.bowls_container, protein_name=protein, controller=self.controller, tab=self)
            bowl_widget.pack(side=tk.LEFT, padx=self.controller.padding, pady=self.controller.padding)
            
        self.fire_container = tk.Frame(self, bg=bg_color)
        self.fire_container.pack(pady=self.controller.padding, padx=self.controller.padding)
        for _ in range(-1, 3):
            wok_widget = Fire(self.fire_container, self.controller)
            wok_widget.pack(side="left", padx=self.controller.padding+20, pady=self.controller.padding)


    def assign_wok(self, protein_name: str) -> bool:
        """Assign a protein to the first available wok."""
        for child in self.fire_container.winfo_children():
            if isinstance(child, Fire) and child.protein_name is None:
                if child.add_protein(protein_name):
                    print(f"Assigned {protein_name} to wok.")
                    return True
        print(f"No available woks for {protein_name}.")
        return False