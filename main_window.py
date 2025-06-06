import tkinter as tk
from time import time
from GUI.Tabs import order_tab, base_tab, veg_fruit_tab, protein_tab, extras_sauces_tab, serve_tab
from Models.Order import Order
import pygame

import sys, os, inspect
sys.path.insert(0, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

tab_classes=[order_tab.Order_Tab, 
             base_tab.Base_Tab, 
             veg_fruit_tab.Veg_Fruit_Tab, 
             protein_tab.Protein_Tab, 
             extras_sauces_tab.Extras_Sauces_Tab, 
             serve_tab.Serve_Tab]

class PookieGUI(tk.Tk):
    """
    Principal class for the Pookie game GUI.
    Inherits from tkinter.Tk to create the main window.
    """
    def __init__(self):
        super().__init__()
        self.title("Pookie")
        self.geometry("800x600")
        self.timer = 0
        self.selected_order = None
        self.orders = []  # List to keep track of all orders
        
        # Top navigation bar
        nav_bar = tk.Frame(self, bg="lightgray")
        nav_bar.pack(side="top", fill="x")

        for page in tab_classes:
            b = tk.Button(nav_bar, text=page.__name__.replace("_"," ")[:-4], command=lambda n=page.__name__: self.show_frame(n))
            b.pack(side="left", padx=2, pady=4)

        # Main layout: left = changing frame; right = order list
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Left dynamic content area
        self.container = tk.Frame(main_frame, bg="white")
        self.container.pack(side="left", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.create_order_panel(main_frame)

        self.pages= {}
        
        for page in tab_classes:
            # Dynamically create pages and store them in the pages dictionary
            page_name = page.__name__
            frame = page(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Order_Tab")  # Show the first page by default
            
        self.sec_loop()

        
    def show_frame(self, page_name):
        """
        Show a frame for the given page name.
        """
        frame = self.pages[page_name]
        frame.tkraise()
        
    
    def select_order(self, order_id, widget):
        # Reset visuals for all
        for _, lbl in self.order_receipts:
            lbl.config(bg="white")

        # Highlight selected
        widget.config(bg="#cceeff")  # light blue

        # Save selected
        self.selected_order = order_id
        print(f"Selected: {order_id}")

    def create_order_panel(self, parent):
        # This panel holds the title and the scrollable area.
        right_panel = tk.Frame(parent, width=200, bg="lightblue")
        right_panel.pack(side="right", fill="y")
        # This crucial line prevents the panel from shrinking to fit its contents.

        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="Orders", font=("Helvetica", 14, "bold"), bg="lightblue").pack(pady=5)
        
        self.selected_order = None
        self.order_receipts = []

        # --- This frame will contain BOTH the canvas and the scrollbar ---
        scroll_container = tk.Frame(right_panel, bg="lightblue")
        scroll_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        canvas = tk.Canvas(scroll_container, borderwidth=0, bg="lightblue", highlightthickness=0)
        # The scrollbar is now correctly placed inside the scroll_container.
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        # This is the frame that will hold all your order labels.
        self.order_frame = tk.Frame(canvas, bg="lightblue")

        # This binding ensures the scrollable area resizes as you add more orders.
        self.order_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Place the order_frame inside the canvas.
        frame_id = canvas.create_window((0, 0), window=self.order_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # --- THE KEY FIX ---
        # This function is called when the canvas is first drawn or resized.
        def on_canvas_configure(event):
            # It sets the width of the frame inside the canvas to match the canvas's width.
            canvas.itemconfig(frame_id, width=event.width)

        # We bind that function to the canvas's <Configure> event.
        canvas.bind("<Configure>", on_canvas_configure)
        # --- END OF FIX ---

        # Pack the canvas and scrollbar side-by-side.
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

    

    def register_order(self, poke):
        order_id = f"Order #{1001+len(self.order_receipts)}"
        label = tk.Label(self.order_frame, text=f"{order_id}\n- base\n- topping\n- protein",
                        bg="white", font=("Courier", 10), bd=1, relief="solid", pady=5, justify="left", padx=5)
        label.pack(pady=4, fill="x", padx=5)

        # Store reference to the label
        self.order_receipts.append((order_id, label))
        self.orders.append(Order(order_id, poke, time()))

        # Add click binding
        label.bind("<Button-1>", lambda e, oid=order_id, lbl=label: self.select_order(oid, lbl))

    def sec_loop(self):
        """
        This function can be used to update the GUI or perform background tasks.
        It is called every second.
        """
        # Add new order
        self.pages["Order_Tab"].show_random_client(self.timer)

        self.timer += 1
        self.after(1000, self.sec_loop)


if __name__=="__main__":
    pygame.mixer.init()
    pygame.mixer.music.load("www/mm.mp3")
    pygame.mixer.music.play(loops=-1)  # Loop indefinitely
    app = PookieGUI()
    app.mainloop()
    