import tkinter as tk

import tkinter as tk
import json, random

# Just for the demo — load from file in practice
clients = [
    #{"trait": "glasses", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    #{"trait": "hat", "order": "Base: Quinoa, Protein: Tofu, Sauce: Spicy Mayo"},
    #{"trait": "sunglasses and beard", "order": "Base: Quinoa, Protein: Tofu, Sauce: Spicy Mayo"},
    #{"trait": "earrings", "order": "Base: Rice, Protein: Chicken, Sauce: Teriyaki"},
    {"trait": "stylish", "order": "Base: Rice, Protein: Chicken, Sauce: Teriyaki"},
    
]

class Order_Tab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self.stickman_canvas = tk.Canvas(self, width=200, height=300, bg="white")
        self.stickman_canvas.grid(row=0, column=0, padx=20, pady=20)
        
        self.speech = tk.Label(self, text="", font=("Helvetica", 14), wraplength=300,
                               bg="#f0f0f0", relief="solid", bd=1, justify="left", padx=10, pady=10)
        self.speech.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        self.show_random_client()

    def show_random_client(self):
        client = random.choice(clients)
        self.draw_stickman(trait=client["trait"])
        self.speech.config(text=client["order"])

    def draw_stickman(self, trait=""):
        c = self.stickman_canvas
        c.delete("all")
        # Draw stickman base
        c.create_oval(70, 50, 130, 110)  # head
        c.create_line(100, 110, 100, 200)  # body
        c.create_line(100, 130, 70, 160)  # left arm
        c.create_line(100, 130, 130, 160)  # right arm
        c.create_line(100, 200, 80, 250)  # left leg
        c.create_line(100, 200, 120, 250)  # right leg
  
 
        if trait == "glasses":
            c.create_oval(80, 65, 95, 80)
            c.create_oval(105, 65, 120, 80)
            c.create_line(95, 72, 105, 72)
        elif trait == "hat":
            c.create_rectangle(65, 40, 135, 55, fill="black")
        elif trait == "happy face and hat":
            c.create_oval(85, 65, 95, 75, fill="black")   # Left eye
            c.create_oval(105, 65, 115, 75, fill="black")  # Right eye
            c.create_arc(85, 80, 115, 100, start=0, extent=-180, style=tk.ARC)
            c.create_polygon(70, 50, 100, 10, 130, 50, fill="red", outline="black")
        elif trait == "sunglasses":
            c.create_oval(80, 65, 95, 80, fill="black")
            c.create_oval(105, 65, 120, 80, fill="black")
            c.create_line(95, 72, 105, 72, fill="black")
        
        elif trait == "earrings":
            c.create_oval(60, 80, 70, 90, fill="gold")
            c.create_oval(130, 80, 140, 90, fill="gold")
        elif trait == "short hair":
             c.create_arc(70, 40, 130, 80, start=0, extent=180, fill="brown", outline="black")  
        elif trait == "biker":
            c.create_arc(75, 85, 125, 120, start=0, extent=180, fill="brown")
            c.create_polygon(75, 100, 100, 130, 125, 100, fill="brown")
            c.create_rectangle(80, 65, 95, 80, fill="black")
            c.create_rectangle(105, 65, 120, 80, fill="black")
            c.create_line(95, 72, 105, 72)
        elif trait == "sad":
            c.create_oval(85, 65, 95, 75, fill="black")   # Left eye
            c.create_oval(105, 65, 115, 75, fill="black")  # Right eye
            c.create_line(85, 65, 95, 60)  # left eyebrow
            c.create_line(105, 60, 115, 65)  # right eyebrow
            c.create_arc(85, 80, 115, 100, start=0, extent=180, style=tk.ARC)
        elif trait == "stylish":
            c.create_rectangle(80, 20, 120, 50, fill="black")
            c.create_rectangle(70, 50, 130, 55, fill="black")
            c.create_polygon(90, 115, 100, 125, 90, 135, fill="red")  # left triangle
            c.create_polygon(110, 115, 100, 125, 110, 135, fill="red")  # right triangle
            c.create_oval(97, 122, 103, 128, fill="black")
            c.create_oval(105, 65, 120, 80)  # monocle
            c.create_line(120, 70, 130, 70)  # string

        
if __name__=="__main__":
    root = tk.Tk()
    app = Order_Tab(parent=root, controller=None)
    app.pack(expand=True, fill="both")
    root.mainloop()