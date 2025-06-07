import tkinter as tk
from time import time
from functools import partial

from Models.Poke import Poke
from Models.Order import Order

from GUI.Tabs import order_tab, base_tab, veg_fruit_tab, protein_tab, extras_sauces_tab, serve_tab
import pygame

import sys, os, inspect
sys.path.insert(0, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

tab_classes=[order_tab.Order_Tab, 
             base_tab.Base_Tab, 
             veg_fruit_tab.Veg_Fruit_Tab, 
             protein_tab.Protein_Tab, 
             extras_sauces_tab.Extras_Sauces_Tab, 
             serve_tab.Serve_Tab]

NavBarFont=("Helvetica", 18, "bold")

class PookieGUI(tk.Tk):
    """
    Principal class for the Pookie game GUI.
    Inherits from tkinter.Tk to create the main window.
    """
    def __init__(self):
        super().__init__()
        self.title("Pookie")
        self.attributes("-fullscreen", True)
        self.timer = 0
        self.selected_order = None
        self.orders = []  # List to keep track of all orders
        
        
        # --- NEW: Main Panel for Bowl Management ---
        self.bowl_management_panel = tk.Frame(self)

        # Part 1: The selection bar
        bowl_selection_frame = tk.Frame(self.bowl_management_panel, bg="#e0e0e0")
        bowl_selection_frame.pack(side="top", fill="x", padx=5, pady=(5,0))
        
        self.bowl_buttons_frame = tk.Frame(bowl_selection_frame, bg="#e0e0e0")
        self.bowl_buttons_frame.pack(side="left", fill="x", expand=True)

        # Part 2: The workspace where the active bowl is drawn
        self.workspace_canvas = tk.Canvas(self.bowl_management_panel, height=150, bg="lightyellow", highlightthickness=0)
        self.workspace_canvas.pack(side="bottom", fill="x", padx=5, pady=5)
                
        # Top navigation bar
        nav_bar = tk.Frame(self, bg="lightgray")
        nav_bar.pack(side="top", fill="x")

        for page in tab_classes:
            b = tk.Button(nav_bar, text=page.__name__.replace("_"," ")[:-4], font=NavBarFont, command=lambda n=page.__name__: self.show_frame(n))
            b.pack(side="left", padx=10, pady=4)

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
        widget.config(bg="#e3f5eb")  

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
    
    def add_new_bowl(self):
            """Creates a new bowl, adds it to the list, and makes it active."""
            new_id = self.next_bowl_id
            self.bowls[new_id] = Poke() # Create a new empty Poke object
            self.next_bowl_id += 1
            self.set_active_bowl(new_id)
            
            # Ensure the panel is visible if we're not on the order tab
            self.show_frame(self.current_page)
    
    def set_active_bowl(self, bowl_id):
        """Sets the specified bowl as active and refreshes the UI."""
        self.active_bowl_id = bowl_id
        print(f"Active bowl set to: {bowl_id}")
        self.update_bowl_selection_bar()
        self.redraw_workspace()
    
    def update_bowl_selection_bar(self):
        """Clears and redraws the buttons for all created bowls."""
        for widget in self.bowl_buttons_frame.winfo_children():
            widget.destroy()

        for bowl_id, poke in sorted(self.bowls.items()):
            cmd = partial(self.set_active_bowl, bowl_id)
            btn_text = f"Bowl {bowl_id}"
            btn = tk.Button(self.bowl_buttons_frame, text=btn_text, command=cmd, relief="raised")
            
            if bowl_id == self.active_bowl_id:
                btn.config(relief="sunken", bg="#cceeff") # Highlight active bowl
            
            btn.pack(side="left", padx=2, pady=2)
    
    def redraw_workspace(self):
        """Clears the workspace and draws the currently active bowl."""
        self.workspace_canvas.delete("all")
        if self.active_bowl_id is None or self.active_bowl_id not in self.bowls:
            return

        # Get the data for the active bowl
        active_poke = self.bowls[self.active_bowl_id]
        
        # Draw the bowl shape
        self.workspace_canvas.create_oval(150, 20, 450, 140, fill="white", outline="grey", width=2)
        
        # Draw the ingredients as text
        y_pos = 40
        if active_poke.base:
            self.workspace_canvas.create_text(300, 110, text=f"Base: {active_poke.base.capitalize()}", font=("Helvetica", 12, "italic"))
        # Future logic will draw proteins, veggies etc. here

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
    