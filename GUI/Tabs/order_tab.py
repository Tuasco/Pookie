import tkinter as tk
import random

# Just for the demo — load from file in practice
clients = [
    {"trait": "glasses", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "hat", "order": "Base: Quinoa, Protein: Tofu, Sauce: Spicy Mayo"},
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

    
    def add_order(self, timer):
        # This function would add an order to the list of orders
        # For now, just print it
        if timer % 30 != 0:
            return

        print(f"Order added")


if __name__=="__main__":
    root = tk.Tk()
    app = Order_Tab(parent=root, controller=None)
    app.pack(expand=True, fill="both")
    root.mainloop()