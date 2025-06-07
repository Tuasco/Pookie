import tkinter as tk
import random
from Models.Poke import Poke
from Customer_relation.filereader import file_reader

# Just for the demo — load from file in practice
clients = [
    {"trait": "red hat", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "biker", "order": "Base: Quinoa, Protein: Tofu, Sauce: Spicy Mayo"},
    {"trait": "happy face and hat", "order": "Base: Quinoa, Protein: Tofu, Sauce: Spicy Mayo"},
    {"trait": "sad", "order": "Base: Rice, Protein: Chicken, Sauce: Teriyaki"},
    {"trait": "stylish", "order": "Base: Rice, Protein: Chicken, Sauce: Teriyaki"},
    {"trait": "sunglasses", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "glasses", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "nerd", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "artist", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "worker", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "superhero", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "scientist", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "royalty", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    {"trait": "villain", "order": "Base: Rice, Protein: Salmon, Sauce: Soy"},
    
]



orders = file_reader('orders.csv') #list of Orders instances Order(order_id, orderedPoke, preparedPoke, orderTime)




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
            c.create_oval(85, 70, 90, 75, fill="black")   # Left eye
            c.create_oval(110, 70, 115, 75, fill="black")  # Right eye
            c.create_oval(80, 65, 95, 80)
            c.create_oval(105, 65, 120, 80)
            c.create_line(95, 72, 105, 72) 
            c.create_oval(95, 85, 105, 95)
        elif trait == "villain":
            c.create_oval(85, 65, 95, 75, fill="black")
            c.create_oval(105, 65, 115, 75, fill="black")
            c.create_line(85, 60, 95, 65)  # angry eyebrow
            c.create_line(105, 65, 115, 60)
            c.create_arc(85, 85, 115, 105, start=0, extent=180, style=tk.ARC)
        elif trait == "royalty":
            # Eyes
            c.create_oval(85, 65, 95, 75, fill="black")   # Left eye
            c.create_oval(105, 65, 115, 75, fill="black")  # Right eye
            # Smile
            c.create_arc(85, 80, 115, 100, start=0, extent=-180, style=tk.ARC)
            # Crown
            c.create_polygon(85, 50, 90, 40, 100, 50, 110, 40, 115, 50, fill="gold", outline="black")
            # Earrings (small golden dots)
            c.create_oval(70, 85, 75, 90, fill="gold")  # Left earring
            c.create_oval(125, 85, 130, 90, fill="gold")  # Right earring
        elif trait == "scientist":
            c.create_rectangle(80, 65, 95, 80, fill="lightblue")
            c.create_rectangle(105, 65, 120, 80, fill="lightblue")
            c.create_line(95, 72, 105, 72)
            c.create_rectangle(125, 130, 130, 160, fill="green")  # test tube
        elif trait == "superhero":
            c.create_oval(85, 65, 95, 75, fill="black")
            c.create_oval(105, 65, 115, 75, fill="black")
            c.create_arc(85, 80, 115, 100, start=0, extent=-180, style=tk.ARC)
            c.create_polygon(100, 110, 70, 200, 130, 200, fill="red", stipple="gray12")  # cape
        elif trait == "worker":
            c.create_rectangle(80, 65, 95, 80)
            c.create_rectangle(105, 65, 120, 80)
            c.create_line(95, 72, 105, 72)
            c.create_rectangle(60, 160, 90, 180, fill="brown")  # book
            c.create_line(90, 160, 90, 180)
            c.create_line(95, 92, 105, 92, fill="black")
            
        elif trait == "artist":
            c.create_oval(85, 65, 95, 75, fill="black")
            c.create_oval(105, 65, 115, 75, fill="black")
            c.create_line(85, 80, 115, 80)
            c.create_oval(85, 50, 115, 60, fill="purple")  # beret
        elif trait == "robot":
            # Square head
            c.create_rectangle(70, 50, 130, 110, fill="silver", outline="black")
            # Eyes
            c.create_rectangle(85, 65, 95, 75, fill="blue")
            c.create_rectangle(105, 65, 115, 75, fill="blue")
            # Antenna
            c.create_line(100, 50, 100, 30)
            c.create_oval(95, 25, 105, 35, fill="red")
            # Mouth
            c.create_rectangle(85, 90, 115, 95, fill="black")
        elif trait == "nerd":
            # Big glasses
            c.create_rectangle(80, 65, 95, 80)
            c.create_rectangle(105, 65, 120, 80)
            c.create_line(95, 72, 105, 72)
            c.create_oval(85, 67, 90, 72, fill="black")  # Left pupil
            c.create_oval(110, 67, 115, 72, fill="black")  # Right pupil
            # Teeth
            c.create_rectangle(95, 95, 105, 100, fill="white", outline="black")
            c.create_line(100, 95, 100, 100)
        elif trait == "happy face and hat":
            c.create_oval(85, 65, 95, 75, fill="black")   # Left eye
            c.create_oval(105, 65, 115, 75, fill="black")  # Right eye
            c.create_arc(85, 80, 115, 100, start=0, extent=-180, style=tk.ARC)
            c.create_polygon(70, 50, 100, 30, 130, 50, fill="red", outline="black")
        elif trait == "sunglasses":
            c.create_oval(80, 65, 95, 80, fill="black")
            c.create_oval(105, 65, 120, 80, fill="black")
            c.create_line(95, 72, 105, 72, fill="black")
            c.create_line(95, 92, 105, 92, fill="black")
        elif trait == "red hat":
             c.create_arc(70, 40, 130, 80, start=0, extent=180, fill="brown", outline="black") # hat
             c.create_arc(85, 65, 95, 75, start=0, extent=180, style=tk.ARC) # left eye
             c.create_arc(105, 65, 115, 75, start=0, extent=180, style=tk.ARC) # right eye
             c.create_arc(85, 80, 115, 100, start=0, extent=-180, style=tk.ARC)

        elif trait == "biker":
            c.create_arc(75, 85, 125, 120, start=0, extent=180, fill="black")
            c.create_polygon(75, 100, 100, 130, 125, 100, fill="black")
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
            c.create_oval(85, 70, 90, 75, fill="black")   # Left eye
            c.create_oval(110, 70, 115, 75, fill="black")  # Right eye


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
        self.controller.register_order(Poke())
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