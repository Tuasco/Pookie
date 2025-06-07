import tkinter as tk
from time import time
from functools import partial

from Models.Poke import Poke
from Models.Order import Order
from Data.Icons import Icons

from GUI.Tabs import order_tab, base_tab, veg_fruit_tab, protein_tab, extras_sauces_tab, serve_tab
import pygame

import sys, os, inspect
sys.path.insert(0, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

tab_classes=[order_tab.Order_Tab, base_tab.Base_Tab, veg_fruit_tab.Veg_Fruit_Tab, protein_tab.Protein_Tab, extras_sauces_tab.Extras_Sauces_Tab, serve_tab.Serve_Tab]
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
        self.orders = []

        # --- Bowl Management Data Initialization ---
        self.bowls = {}
        self.active_bowl_id = None
        self.next_bowl_id = 1
        self.current_page = ""
        
        # Get screen dimensions for responsive sizing ---
        self.update_idletasks() # Ensure window info is up-to-date
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Define responsive sizes ---
        self.responsive_right_panel_width = int(screen_width * 0.15) 
        self.responsive_workspace_height = int(screen_height * 0.20)

        # UI Initialization ---
        nav_bar = tk.Frame(self, bg="lightgray")

        for page in tab_classes:
            cmd = partial(self.show_frame, page.__name__)
            b = tk.Button(nav_bar, text=page.__name__.replace("_"," ")[:-4], font=NavBarFont, command=cmd)
            b.pack(side="left", padx=10, pady=4)

        close_button = tk.Button(nav_bar, text="X", font=NavBarFont, command=self.destroy)
        close_button.pack(side="right", padx=10, pady=4)

        music_canvas = tk.Canvas(nav_bar, width=24, height=24, bg="lightgray", highlightthickness=0, cursor="hand2")
        music_canvas.pack(side="right", padx=10, pady=4)
        
        # Create an icon loader and draw the icon
        try:
            music_icon_loader = Icons(music_canvas, size=(24, 24))
            music_icon_loader.draw_icon("music_on", 12, 12)
        except Exception as e:
            print(f"Could not load music_on icon: {e}")
            music_canvas.create_text(12, 12, text="M", font=NavBarFont) # Fallback text
        
        music_canvas.bind("<Button-1>", lambda e: pygame.mixer.music.pause() if pygame.mixer.music.get_busy() else pygame.mixer.music.unpause())

        nav_bar.pack(side="top", fill="x")


        # Bowl Management Panel ---
        self.bowl_management_panel = tk.Frame(self)
        bowl_selection_frame = tk.Frame(self.bowl_management_panel, bg="#e0e0e0") 
        bowl_selection_frame.pack(side="top", fill="x", padx=5, pady=(5,0))
        self.bowl_buttons_frame = tk.Frame(bowl_selection_frame, bg="#e0e0e0")
        self.bowl_buttons_frame.pack(side="left", fill="x", expand=True)
        self.workspace_canvas = tk.Canvas(self.bowl_management_panel, height=self.responsive_workspace_height, bg="lightyellow", highlightthickness=0)
        self.workspace_canvas.pack(side="bottom", fill="x", padx=5, pady=5)
        # This panel is packed/unpacked later in show_frame.

        # Main Container Frame ---
        main_frame = tk.Frame(self)
        main_frame.pack(side="top", fill="both", expand=True)


        # Setup Main Content Area (which is inside main_frame) ---
        self.container = tk.Frame(main_frame, bg="white")
        self.container.pack(side="left", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.create_order_panel(main_frame)

        self.pages= {}
        for page in tab_classes:
            page_name = page.__name__
            frame = page(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Order_Tab")
        self.sec_loop()


    def show_frame(self, page_name):
        """
        Show a frame for the given page name and manage bowl panel visibility.
        """
        self.current_page = page_name
        frame = self.pages[page_name]
        frame.tkraise()

        if page_name == "Order_Tab":
            self.bowl_management_panel.pack_forget()
        elif self.bowls:
             self.bowl_management_panel.pack(side="top", fill="x")


    def select_order(self, order_id, widget):
        """ Selects an order by changing its background color and updating the selected_order attribute."""

        for _, lbl in self.order_receipts:
            lbl.config(bg="white")

        widget.config(bg="#e3f5eb")
        self.selected_order = order_id
        print(f"Selected: {order_id}")

    def create_order_panel(self, parent):
        right_panel = tk.Frame(parent, width=self.responsive_right_panel_width, bg="lightblue")
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="Orders", font=("Helvetica", 20, "bold"), bg="lightblue").pack(pady=5)
        self.order_receipts = []
        scroll_container = tk.Frame(right_panel, bg="lightblue")
        scroll_container.pack(fill="both", expand=True, padx=5, pady=5)
        canvas = tk.Canvas(scroll_container, borderwidth=0, bg="lightblue", highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        self.order_frame = tk.Frame(canvas, bg="lightblue")
        self.order_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        frame_id = canvas.create_window((0, 0), window=self.order_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_canvas_configure(event):
            canvas.itemconfig(frame_id, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)


    def register_order(self, poke):
        """ Registers a new order by creating a label in the order panel and storing it in the orders list."""

        order_id = f"Order #{1001+len(self.order_receipts)}"
        poke_text= f"- {poke.base.capitalize()}\n* {str(poke.vft)[1:-2].replace('\'', '').replace(',', '\n*')}\n- {poke.sauce}\n- {poke.protein.name}"
        label = tk.Label(self.order_frame, text=f"{order_id}\n{poke_text}", bg="white", font=("Courier", 15), bd=1, relief="solid", pady=5, justify="left", padx=5)
        label.pack(pady=4, fill="x", padx=5)
        self.order_receipts.append((order_id, label))
        self.orders.append(Order(order_id, poke, time()))
        label.bind("<Button-1>", lambda e, oid=order_id, lbl=label: self.select_order(oid, lbl))

    def add_new_bowl(self):
        """Creates a new bowl, adds it to the list, and makes it active."""

        was_first_bowl = not self.bowls
        
        if was_first_bowl and self.current_page != "Order_Tab":
            self.bowl_management_panel.pack(side="top", fill="x")
        
        new_id = self.next_bowl_id
        self.bowls[new_id] = Poke()
        self.next_bowl_id += 1
        self.set_active_bowl(new_id)

        

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
                btn.config(relief="sunken", bg="#cceeff")
            btn.pack(side="left", padx=2, pady=2)


    def redraw_workspace(self):
        """Clears the workspace and draws the currently active bowl."""

        self.workspace_canvas.delete("all")
        if self.active_bowl_id is None or self.active_bowl_id not in self.bowls:
            return
        
        # Draw the circle
        self.update_idletasks()
        canvas_w = self.workspace_canvas.winfo_width()
        canvas_h = self.workspace_canvas.winfo_height()

        # Center the circle on the canvas
        center_x = canvas_w / 2
        center_y = canvas_h / 2
        
        # Make the diameter 85% of the canvas's smaller dimension
        diameter = min(canvas_w, canvas_h) * 0.85
        radius = diameter / 2
        
        # Calculate the bounding box for the circle
        x1 = center_x - radius
        y1 = center_y - radius
        x2 = center_x + radius
        y2 = center_y + radius
        
        active_poke = self.bowls[self.active_bowl_id]
        self.workspace_canvas.create_oval(x1, y1, x2, y2, fill="white", outline="grey", width=3)
        
        # Draw the base text in the center of the circle
        if hasattr(active_poke, 'base') and active_poke.base:
            text_x = center_x
            text_y = center_y + (radius * 0.5) # Position text in the lower part of the bowl
            self.workspace_canvas.create_text(text_x, text_y, text=f"Base: {active_poke.base.capitalize()}", font=("Helvetica", 14, "italic"))


    def add_base_to_active_bowl(self, base_name):
        """Called by Base_Tab to add a base to the current bowl."""

        if self.active_bowl_id is not None and self.active_bowl_id in self.bowls:
            self.bowls[self.active_bowl_id].base = base_name
            print(f"Added base '{base_name}' to Bowl {self.active_bowl_id}")
            self.redraw_workspace()
        else:
            print("No active bowl to add a base to!")


    def sec_loop(self):
        """
        This function can be used to update the GUI or perform background tasks.
        It is called every second.
        """
        if "Order_Tab" in self.pages:
            self.pages["Order_Tab"].show_random_client(self.timer)

        self.timer += 1
        self.after(1000, self.sec_loop)


if __name__=="__main__":
    pygame.mixer.init()
    pygame.mixer.music.load("www/mm.mp3")
    pygame.mixer.music.play(loops=-1)
    app = PookieGUI()
    app.mainloop()