import tkinter as tk
from tkinter import messagebox
from time import time
from functools import partial
import random
import math

from Models.Poke import Poke
from Models.Order import Order
from Models.VFT import VFT
from Models.Sauce import Sauce
from Data.Icons import Icons

from GUI.Tabs import order_tab, base_tab, veg_fruit_tab, protein_tab, extras_sauces_tab, serve_tab
import pygame

import sys, os, inspect
sys.path.insert(0, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

tab_classes=[order_tab.Order_Tab, base_tab.Base_Tab, veg_fruit_tab.Veg_Fruit_Tab, protein_tab.Protein_Tab, extras_sauces_tab.Extras_Sauces_Tab, serve_tab.Serve_Tab]
NavBarFont=("Helvetica", 18, "bold")
bg_color = "seashell"  # Background color for the bowl management panel

class PookieGUI(tk.Tk):
    """
    Principal class for the Pookie game GUI.
    Inherits from tkinter.Tk to create the main window.
    """
    def __init__(self):
        super().__init__()
        self.title("Pookie")
        self.attributes("-fullscreen", True)
        self.configure(bg="lightpink")
        self.timer = 0
        self.selected_order = None
        self.orders = []

        # --- Music State ---
        self.music_on = True

        # --- Bowl Management Data Initialization ---
        self.bowls = {}
        self.active_bowl_id = None
        self.next_bowl_id = 1
        self.current_page = ""
        
        # --- Placement & Drawing Mode State ---
        self.ingredient_to_place = None
        self.sauce_to_draw = None
        self.is_drawing_sauce = False
        self.sauce_path_points = []
        self.sauce_colors = {
            "soy sauce": "#5C4033", "sriracha": "#FF4500",
            "sour cream": "#FAF0E6", "wasabi": "#7CFC00"
        }
        
        # --- Bowl Geometry ---
        self.bowl_center_x = 0
        self.bowl_center_y = 0
        self.bowl_radius = 0

        # Get screen dimensions for responsive sizing ---
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Define responsive sizes ---
        self.responsive_right_panel_width = int(screen_width * 0.15) 
        self.responsive_workspace_height = int(screen_height * 0.30)
            
        pygame.mixer.music.stop()
        
        # UI Initialization ---
        nav_bar = tk.Frame(self, bg="lightpink")

        for page in tab_classes:
            cmd = partial(self.show_frame, page.__name__)
            b = tk.Button(nav_bar, text=page.__name__.replace("_"," ")[:-4], font=NavBarFont, command=cmd, bg="palevioletred", fg="white", borderwidth=0, highlightthickness=0, cursor="hand2")
            b.pack(side="left", padx=10, pady=4)

        close_button = tk.Button(nav_bar, text="X", font=NavBarFont, command=self.destroy, borderwidth=0, bg="mediumvioletred", fg="white", highlightthickness=0, cursor="hand2")
        close_button.pack(side="right", padx=10, pady=4)

        # --- Music Button Setup ---
        self.music_canvas = tk.Canvas(nav_bar, width=24, height=24, bg="lightpink", highlightthickness=0, cursor="hand2")
        self.music_canvas.pack(side="right", padx=10, pady=4)
        
        self.music_icon_loader = Icons(self.music_canvas, size=(24, 24))
        self.music_icon_loader.draw_icon("sound_on", 12, 12) 
        
        self.music_canvas.bind("<Button-1>", self.toggle_music) 

        nav_bar.pack(side="top", fill="x")
        
        # --- Main Frame for Content ---
        main_frame = tk.Frame(self)
        main_frame.pack(side="top", fill="both", expand=True)

        # Create the Order Panel first and pack it to the right
        self.create_order_panel(main_frame)

        # Create the Bowl Management Panel 
        self.bowl_management_panel = tk.Frame(main_frame)
        bowl_selection_frame = tk.Frame(self.bowl_management_panel, bg=bg_color) 
        bowl_selection_frame.pack(side="top", fill="x", padx=5, pady=(5,0))
        self.bowl_buttons_frame = tk.Frame(bowl_selection_frame, bg=bg_color, highlightthickness=0)
        self.bowl_buttons_frame.pack(side="left", fill="x", expand=True)
        self.workspace_canvas = tk.Canvas(self.bowl_management_panel, height=self.responsive_workspace_height, bg=bg_color, highlightthickness=0)
        self.workspace_canvas.pack(side="bottom", fill="x", padx=5, pady=5)
        
        # Bind all mouse events for the workspace
        self.workspace_canvas.bind("<ButtonPress-1>", self.on_workspace_press)
        self.workspace_canvas.bind("<B1-Motion>", self.on_workspace_drag)
        self.workspace_canvas.bind("<ButtonRelease-1>", self.on_workspace_release)

        # Create icon managers for the workspace canvas
        self.workspace_icon_manager = Icons(self.workspace_canvas, size=(200, 200))
        self.toppings_icon_manager = Icons(self.workspace_canvas, size=(45, 45))

        # Create the main container for tabs last.
        self.container = tk.Frame(main_frame, bg=bg_color)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # --- Page and Tab Initialization ---
        self.pages= {}
        for page in tab_classes:
            page_name = page.__name__
            frame = page(parent=self.container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Order_Tab")
        self.sec_loop()

    
    def toggle_music(self, event=None):
        self.music_canvas.delete("all")
        if self.music_on:
            pygame.mixer.music.stop()
            self.music_icon_loader.draw_icon("sound_off", 12, 12)
            self.music_on = False
        else:
            pygame.mixer.music.play(loops=-1)
            self.music_icon_loader.draw_icon("sound_on", 12, 12)
            self.music_on = True


    def show_frame(self, page_name):
        self.current_page = page_name
        frame = self.pages[page_name]
        frame.tkraise()

        if page_name == "Order_Tab":
            self.bowl_management_panel.pack_forget()
        elif self.bowls:
             self.bowl_management_panel.pack(side="bottom")


    def select_order(self, order_id, widget):
        for _, lbl in self.order_receipts:
            lbl.config(bg="white")
        widget.config(bg="#e3f5eb", relief="groove")
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
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        frame_id = canvas.create_window((0, 0), window=self.order_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        def on_canvas_configure(event):
            canvas.itemconfig(frame_id, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)


    def register_order(self, poke):
        order_id = f"Order #{1001+len(self.order_receipts)}"
        vft_names = [item['name'] for item in poke.vft] if (poke.vft and isinstance(poke.vft[0], dict)) else poke.vft
        sauce_name = poke.sauce.name if hasattr(poke.sauce, 'name') else poke.sauce
        poke_text= f"- {poke.base.capitalize()}\n* {str(vft_names)[1:-2].replace('\'', '').replace(',', '\n*')}\n- {sauce_name}\n- {poke.protein.name}"
        label = tk.Label(self.order_frame, text=f"{order_id}\n{poke_text}", bg="white", font=("Courier", 15), bd=1, borderwidth=0, pady=5, justify="left", padx=5)
        label.pack(pady=4, fill="x", padx=5)
        self.order_receipts.append((order_id, label))
        self.orders.append(Order(order_id, poke, time()))
        label.bind("<Button-1>", lambda e, oid=order_id, lbl=label: self.select_order(oid, lbl))


    def add_new_bowl(self):
        if not self.order_receipts:
            messagebox.showinfo("No Orders", "You must take an order before you can create a bowl.")
            self.show_frame("Order_Tab")
            return
        was_first_bowl = not self.bowls
        if was_first_bowl and self.current_page != "Order_Tab":
            self.bowl_management_panel.pack(side="bottom", fill="x")
        new_id = self.next_bowl_id
        self.bowls[new_id] = Poke()
        self.next_bowl_id += 1
        self.set_active_bowl(new_id)

    def set_active_bowl(self, bowl_id):
        self.active_bowl_id = bowl_id
        print(f"Active bowl set to: {bowl_id}")
        self.update_bowl_selection_bar()
        self.redraw_workspace()

    def update_bowl_selection_bar(self):
        for widget in self.bowl_buttons_frame.winfo_children():
            widget.destroy()
        for bowl_id, poke in sorted(self.bowls.items()):
            cmd = partial(self.set_active_bowl, bowl_id)
            btn_text = f"Bowl {bowl_id}"
            btn = tk.Button(self.bowl_buttons_frame, text=btn_text, command=cmd, relief="raised")
            if bowl_id == self.active_bowl_id:
                btn.config(relief="groove", bg="salmon", fg="white")
            btn.pack(side="left", padx=2, pady=2)

    def add_base_to_bowl(self, base):
        if self.active_bowl_id is None: return
        poke = self.bowls[self.active_bowl_id]
        poke.base = base
        self.redraw_workspace()

    def set_ingredient_for_placement(self, ingredient_name):
        """Puts the game into 'placement mode' for a given ingredient."""
        if self.active_bowl_id is None:
            messagebox.showwarning("No Active Bowl", "Please select a bowl before adding ingredients.")
            return
        self.sauce_to_draw = None # Exit sauce mode if active
        self.ingredient_to_place = ingredient_name
        self.workspace_canvas.config(cursor="crosshair")

    def set_sauce_for_drawing(self, sauce_name):
        """Puts the game into 'sauce drawing mode'."""
        if self.active_bowl_id is None:
            messagebox.showwarning("No Active Bowl", "Please select a bowl before adding sauce.")
            return
        self.ingredient_to_place = None # Exit placement mode
        self.sauce_to_draw = sauce_name
        self.workspace_canvas.config(cursor="spraycan")

    def on_workspace_press(self, event):
        """Handles the start of a click or drag on the workspace."""
        if self.sauce_to_draw:
            self.is_drawing_sauce = True
            self.sauce_path_points = [(event.x, event.y)]
        
    def on_workspace_drag(self, event):
        """Draws the sauce trail as the user drags the mouse."""
        if not self.is_drawing_sauce:
            return
        
        self.sauce_path_points.append((event.x, event.y))
        if len(self.sauce_path_points) > 1:
            p1 = self.sauce_path_points[-2]
            p2 = self.sauce_path_points[-1]
            color = self.sauce_colors.get(self.sauce_to_draw, "black")
            self.workspace_canvas.create_line(p1, p2, fill=color, width=5, capstyle=tk.ROUND, smooth=True)

    def on_workspace_release(self, event):
        """Finalizes the placement of an ingredient or the drawing of a sauce."""
        # --- Handle Ingredient Placement ---
        if self.ingredient_to_place:
            distance_sq = (event.x - self.bowl_center_x)**2 + (event.y - self.bowl_center_y)**2
            if distance_sq > self.bowl_radius**2:
                messagebox.showwarning("Missed!", "You must click inside the bowl to place an ingredient.")
            else:
                poke = self.bowls[self.active_bowl_id]
                new_vft = VFT(name=self.ingredient_to_place, position=(event.x, event.y))
                poke.vft.append(new_vft)
            self.ingredient_to_place = None # Exit placement mode
        
        # --- Handle Sauce Drawing ---
        if self.is_drawing_sauce:
            self.is_drawing_sauce = False
            if len(self.sauce_path_points) > 1:
                poke = self.bowls[self.active_bowl_id]
                poke.sauce = Sauce(name=self.sauce_to_draw, path=self.sauce_path_points)
            self.sauce_to_draw = None # Exit drawing mode

        self.workspace_canvas.config(cursor="")
        self.redraw_workspace()

    def redraw_workspace(self):
        """Clears the workspace and draws the currently active bowl and all its contents."""
        self.workspace_canvas.delete("all")
        if self.active_bowl_id is None: return
        
        self.update_idletasks()
        canvas_w = self.workspace_canvas.winfo_width()
        canvas_h = self.workspace_canvas.winfo_height()

        self.bowl_center_x = canvas_w / 2
        self.bowl_center_y = canvas_h / 2
        diameter = min(canvas_w, canvas_h) * 0.85
        self.bowl_radius = diameter / 2
        
        x1, y1 = self.bowl_center_x - self.bowl_radius, self.bowl_center_y - self.bowl_radius
        x2, y2 = self.bowl_center_x + self.bowl_radius, self.bowl_center_y + self.bowl_radius
        
        active_poke = self.bowls[self.active_bowl_id]
        self.workspace_canvas.create_oval(x1, y1, x2, y2, fill="peru", outline="saddlebrown", width=3)
        
        if active_poke.base:
            icon_name = active_poke.base.replace(" ", "_").lower()
            self.workspace_icon_manager.draw_icon(icon_name, self.bowl_center_x, self.bowl_center_y)

        if active_poke.sauce and active_poke.sauce.path:
            color = self.sauce_colors.get(active_poke.sauce.name, "black")
            self.workspace_canvas.create_line(active_poke.sauce.path, fill=color, width=5, capstyle=tk.ROUND, smooth=True)

        if active_poke.vft:
            for vft_item in active_poke.vft:
                icon_name = vft_item.name.replace(" ", "_").lower()
                pos_x, pos_y = vft_item.position
                self.toppings_icon_manager.draw_icon(icon_name, pos_x, pos_y)

    def sec_loop(self):
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