import tkinter as tk
import random
from time import sleep

# Just for the demo — load from file in practice
clients = [
    {"trait": "glasses", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "hat", "order": "Base: Quinoa, Protein: Tofu, Sauce: Spicy Mayo"},
]

class Order_Tab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.pending_clients = []
        self.taking_order = False

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)

        self.stickman_canvas = tk.Canvas(self, width=200, height=300, bg="white")
        self.stickman_canvas.grid(row=0, column=0, padx=20, pady=20)
        
        self.speech = tk.Label(self, text="", font=("Helvetica", 14), wraplength=300,
                               bg="#f0f0f0", relief="solid", bd=1, justify="left", padx=10, pady=10)
        self.speech.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        self.take_order_button = tk.Button(self, text="Take Order", command=self.take_order)
        self.take_order_button.grid(row=1, column=0, columnspan=2, pady=10)


    def show_random_client(self, timer):
        if timer % 60 != 0:
            return

        client = random.choice(clients)
        self.pending_clients.append(client)

        if len(self.pending_clients) == 1:
            self.draw_stickman(trait=client["trait"])

        self.speech.config(text=f"Line : {len(self.pending_clients)}")
        print("Order added")


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


    def take_order(self):
        """
        Simulate taking an order.
        In practice, this would involve more complex logic.
        """
        if self.taking_order:
            return

        client = self.pending_clients.pop(0) if self.pending_clients else None
        if client is None:
            return
        
        self.taking_order = True
        self.speech.config(text=client["order"])
        self.draw_stickman(trait=client["trait"])

        # Add order to orders list
        self.controller.add_order_to_panel()
        self.after(3000, self.finish_taking_order)


    def finish_taking_order(self):
        """
        This function is called after the order is taken.
        It can be used to update the GUI or perform background tasks.
        """
        if self.pending_clients:
            self.draw_stickman(trait=self.pending_clients[0]["trait"])
            self.speech.config(text=f"Line : {len(self.pending_clients)}")
        else:
            self.stickman_canvas.delete("all")
            self.speech.config(text="No more clients in line.")

        self.taking_order = False
         


if __name__=="__main__":
    root = tk.Tk()
    app = Order_Tab(parent=root, controller=None)
    app.pack(expand=True, fill="both")
    root.mainloop()