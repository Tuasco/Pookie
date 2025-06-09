import tkinter as tk
import random
from time import time
from tkinter import scrolledtext
from Models.Poke import Poke
from GUI.Tabs.order_detail_window import OrderDetailWindow
from Customer_simulation.filereader import file_reader_dico

orders = file_reader_dico("Customer_simulation/orders.csv")
bg_color = "seashell"


class Order_Tab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=bg_color)
        self.controller = controller

        self.pending_orders = []
        self.pending_orders_time = []
        self.waiting_clients = []
        self.waiting_clients_frames = {} # Store frames for waiting clients to remove them on serve (by order id)
        self.taking_order = False

        # --- Main Layout Frames ---
        self.counter_frame = tk.Frame(self, bg=bg_color)
        self.counter_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.waiting_area_frame = tk.Frame(self, bg="lightgoldenrodyellow")
        self.waiting_area_frame.pack(side="right", fill="y", padx=20, pady=20)
        tk.Label(self.waiting_area_frame, text="Waiting", font=self.controller.font_title, bg="lightgoldenrodyellow").pack(pady=10)

        # --- Counter Display (Center) ---
        self.stickman_canvas = tk.Canvas(self.counter_frame, width=200, height=300, bg=bg_color, highlightthickness=0)
        self.stickman_canvas.pack(pady=20)

        self.queue_label = tk.Label(self.counter_frame, text="No clients in line.", font=self.controller.font_label, wraplength=400,
                                bg="#f0f0f0", relief="solid", bd=1, justify="left", padx=10, pady=10)
        self.queue_label.pack(pady=10, fill="x")

        self.take_order_button = tk.Button(self.counter_frame, text="Take Order", font=self.controller.font_button, command=self.take_order)
        self.take_order_button.pack(pady=10)

        self.display_current_client()


    def show_random_client(self, timer):
        if timer % 30 != 0: return
        if len(self.pending_orders) >= 5: return

        order = random.choice(orders)
        self.pending_orders.append(order)
        self.pending_orders_time.append(time())
        
        if len(self.pending_orders) == 1 and not self.taking_order:
            self.display_current_client()
        else:
            self.queue_label.config(text=f"A new client has arrived! ({len(self.pending_orders)} in line)")


    def display_current_client(self):
        if not self.pending_orders:
            self.stickman_canvas.delete("all")
            self.queue_label.config(text="No clients in line.")
            return

        client = self.pending_orders[0]
        self.draw_stickman(trait=client.get("trait", ""))
        self.queue_label.config(text=f"A new client has arrived! ({len(self.pending_orders)} in line)")


    def take_order(self):
        if self.taking_order or not self.pending_orders: return

        self.taking_order = True
        client = self.pending_orders[0]
        time_waited = self.pending_orders_time[0]
        order_id = self.controller.register_order(client["poke"], time_waited)
        
        # Create an instance of our new pop-up window
        OrderDetailWindow(self.controller, client["poke"])
        
        # Finish the order process immediately after the pop-up closes
        self.finish_taking_order(order_id)


    def finish_taking_order(self, order_id):
        if not self.pending_orders:
             self.taking_order = False
             return

        client_that_ordered = self.pending_orders.pop(0)
        self.pending_orders_time.pop(0)
        self.waiting_clients.append(client_that_ordered)
        self.add_client_to_waiting_area(client_that_ordered, order_id)
        self.taking_order = False

        if self.pending_orders:
            self.display_current_client()
        else:
            self.stickman_canvas.delete("all")
            self.queue_label.config(text="No clients in line.")


    def add_client_to_waiting_area(self, client_data, order_id):
        client_frame = tk.Frame(self.waiting_area_frame, bg="lightgoldenrodyellow")
        client_canvas = tk.Canvas(client_frame, width=50, height=75, bg="lightgoldenrodyellow", highlightthickness=0)
        self.draw_stickman(canvas=client_canvas, scale=0.25, trait=client_data.get("trait", ""))
        client_canvas.pack()
        client_frame.pack(pady=5)
        self.waiting_clients_frames[order_id] = client_frame


    def remove_client_from_waiting_area(self, order_id):
        self.waiting_clients_frames[order_id].destroy()
        del self.waiting_clients_frames[order_id]

        
    def draw_stickman(self, canvas=None, scale=1.0, trait=""):
        """
        Draws a stickman on a given canvas with a specified scale and trait.
        If no canvas is provided, it uses the main stickman canvas.
        """
        # Use the provided canvas, or default to the main one
        c = canvas if canvas else self.stickman_canvas
        c.delete("all")

        # Scaling function to make drawings smaller or larger
        def s(value):
            return int(value * scale)

        # --- Base Stickman Drawing ---
        # Each coordinate is passed through the scaling function s()
        c.create_oval(s(70), s(50), s(130), s(110), fill="white")  # head
        c.create_line(s(100), s(110), s(100), s(200))              # body
        c.create_line(s(100), s(130), s(70), s(160))               # left arm
        c.create_line(s(100), s(130), s(130), s(160))              # right arm
        c.create_line(s(100), s(200), s(80), s(250))               # left leg
        c.create_line(s(100), s(200), s(120), s(250))              # right leg

        # --- Trait Drawing ---
        # Each trait's coordinates are also scaled
        if trait == "glasses":
            c.create_oval(s(85), s(70), s(90), s(75), fill="black")   # Left eye
            c.create_oval(s(110), s(70), s(115), s(75), fill="black")  # Right eye
            c.create_oval(s(80), s(65), s(95), s(80))
            c.create_oval(s(105), s(65), s(120), s(80))
            c.create_line(s(95), s(72), s(105), s(72))
            c.create_oval(s(95), s(85), s(105), s(95))
        elif trait == "villain":
            c.create_oval(s(85), s(65), s(95), s(75), fill="black")
            c.create_oval(s(105), s(65), s(115), s(75), fill="black")
            c.create_line(s(85), s(60), s(95), s(65))  # angry eyebrow
            c.create_line(s(105), s(65), s(115), s(60))
            c.create_arc(s(85), s(85), s(115), s(105), start=0, extent=180, style=tk.ARC)
        elif trait == "royalty":
            # Eyes
            c.create_oval(s(85), s(65), s(95), s(75), fill="black")   # Left eye
            c.create_oval(s(105), s(65), s(115), s(75), fill="black")  # Right eye
            # Smile
            c.create_arc(s(85), s(80), s(115), s(100), start=0, extent=-180, style=tk.ARC)
            # Crown
            c.create_polygon(s(85), s(50), s(90), s(40), s(100), s(50), s(110), s(40), s(115), s(50), fill="gold", outline="black")
            # Earrings (small golden dots)
            c.create_oval(s(70), s(85), s(75), s(90), fill="gold")  # Left earring
            c.create_oval(s(125), s(85), s(130), s(90), fill="gold")  # Right earring
        elif trait == "scientist":
            c.create_rectangle(s(80), s(65), s(95), s(80), fill="lightblue")
            c.create_rectangle(s(105), s(65), s(120), s(80), fill="lightblue")
            c.create_line(s(95), s(72), s(105), s(72))
            c.create_rectangle(s(125), s(130), s(130), s(160), fill="green")  # test tube
        elif trait == "superhero":
            c.create_oval(s(85), s(65), s(95), s(75), fill="black")
            c.create_oval(s(105), s(65), s(115), s(75), fill="black")
            c.create_arc(s(85), s(80), s(115), s(100), start=0, extent=-180, style=tk.ARC)
            c.create_polygon(s(100), s(110), s(70), s(200), s(130), s(200), fill="red", stipple="gray12")  # cape
        elif trait == "worker":
            c.create_rectangle(s(80), s(65), s(95), s(80))
            c.create_rectangle(s(105), s(65), s(120), s(80))
            c.create_line(s(95), s(72), s(105), s(72))
            c.create_rectangle(s(60), s(160), s(90), s(180), fill="brown")  # book
            c.create_line(s(90), s(160), s(90), s(180))
            c.create_line(s(95), s(92), s(105), s(92), fill="black")
        elif trait == "artist":
            c.create_oval(s(85), s(65), s(95), s(75), fill="black")
            c.create_oval(s(105), s(65), s(115), s(75), fill="black")
            c.create_line(s(85), s(80), s(115), s(80))
            c.create_oval(s(85), s(50), s(115), s(60), fill="purple")  # beret
        elif trait == "robot":
            # Square head
            c.create_rectangle(s(70), s(50), s(130), s(110), fill="silver", outline="black")
            # Eyes
            c.create_rectangle(s(85), s(65), s(95), s(75), fill="blue")
            c.create_rectangle(s(105), s(65), s(115), s(75), fill="blue")
            # Antenna
            c.create_line(s(100), s(50), s(100), s(30))
            c.create_oval(s(95), s(25), s(105), s(35), fill="red")
            # Mouth
            c.create_rectangle(s(85), s(90), s(115), s(95), fill="black")
        elif trait == "nerd":
            # Big glasses
            c.create_rectangle(s(80), s(65), s(95), s(80))
            c.create_rectangle(s(105), s(65), s(120), s(80))
            c.create_line(s(95), s(72), s(105), s(72))
            c.create_oval(s(85), s(67), s(90), s(72), fill="black")  # Left pupil
            c.create_oval(s(110), s(67), s(115), s(72), fill="black")  # Right pupil
            # Teeth
            c.create_rectangle(s(95), s(95), s(105), s(100), fill="white", outline="black")
            c.create_line(s(100), s(95), s(100), s(100))
        elif trait == "happy face and hat":
            c.create_oval(s(85), s(65), s(95), s(75), fill="black")   # Left eye
            c.create_oval(s(105), s(65), s(115), s(75), fill="black")  # Right eye
            c.create_arc(s(85), s(80), s(115), s(100), start=0, extent=-180, style=tk.ARC)
            c.create_polygon(s(70), s(50), s(100), s(30), s(130), s(50), fill="red", outline="black")
        elif trait == "sunglasses":
            c.create_oval(s(80), s(65), s(95), s(80), fill="black")
            c.create_oval(s(105), s(65), s(120), s(80), fill="black")
            c.create_line(s(95), s(72), s(105), s(72), fill="black")
            c.create_line(s(95), s(92), s(105), s(92), fill="black")
        elif trait == "red hat":
             c.create_arc(s(70), s(40), s(130), s(80), start=0, extent=180, fill="brown", outline="black") # hat
             c.create_arc(s(85), s(65), s(95), s(75), start=0, extent=180, style=tk.ARC) # left eye
             c.create_arc(s(105), s(65), s(115), s(75), start=0, extent=180, style=tk.ARC) # right eye
             c.create_arc(s(85), s(80), s(115), s(100), start=0, extent=-180, style=tk.ARC)
        elif trait == "biker":
            c.create_arc(s(75), s(85), s(125), s(120), start=0, extent=180, fill="black")
            c.create_polygon(s(75), s(100), s(100), s(130), s(125), s(100), fill="black")
            c.create_rectangle(s(80), s(65), s(95), s(80), fill="black")
            c.create_rectangle(s(105), s(65), s(120), s(80), fill="black")
            c.create_line(s(95), s(72), s(105), s(72))
        elif trait == "sad":
            c.create_oval(s(85), s(65), s(95), s(75), fill="black")   # Left eye
            c.create_oval(s(105), s(65), s(115), s(75), fill="black")  # Right eye
            c.create_line(s(85), s(65), s(95), s(60))  # left eyebrow
            c.create_line(s(105), s(60), s(115), s(65))  # right eyebrow
            c.create_arc(s(85), s(80), s(115), s(100), start=0, extent=180, style=tk.ARC)
        elif trait == "stylish":
            c.create_rectangle(s(80), s(20), s(120), s(50), fill="black")
            c.create_rectangle(s(70), s(50), s(130), s(55), fill="black")
            c.create_polygon(s(90), s(115), s(100), s(125), s(90), s(135), fill="red")  # left triangle
            c.create_polygon(s(110), s(115), s(100), s(125), s(110), s(135), fill="red")  # right triangle
            c.create_oval(s(97), s(122), s(103), s(128), fill="black")
            c.create_oval(s(105), s(65), s(120), s(80))  # monocle
            c.create_line(s(120), s(70), s(130), s(70))  # string
            c.create_oval(s(85), s(70), s(90), s(75), fill="black")   # Left eye
            c.create_oval(s(110), s(70), s(115), s(75), fill="black")  # Right eye