import tkinter as tk
from tkinter import messagebox
from functools import partial
from copy import deepcopy

from Models.Poke import Poke
from Models.Order import Order
from Models.Protein import Protein
from Models.VFT import VFT
from Models.Sauce import Sauce
from Data.Icons import Icons
from Customer_simulation.order_grading import score

from GUI.Tabs import order_tab, base_tab, veg_fruit_tab, protein_tab, extras_sauces_tab, serve_tab
import pygame

import sys, os, inspect
sys.path.insert(0, os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

tab_classes=[order_tab.Order_Tab, base_tab.Base_Tab, veg_fruit_tab.Veg_Fruit_Tab, protein_tab.Protein_Tab, extras_sauces_tab.Extras_Sauces_Tab, serve_tab.Serve_Tab]

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
        self.wallet = 0.00

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

        # --- Define Responsive Sizes & Fonts ---
        self.responsive_right_panel_width = int(screen_width * 0.15) 
        self.responsive_workspace_height = int(screen_height * 0.30)

        # Fonts
        base_font_size = max(10, int(screen_height / 60))
        self.font_nav = ("Helvetica", base_font_size, "bold")
        self.font_title = ("Helvetica", int(base_font_size * 1.1), "bold")
        self.font_button = ("Helvetica", int(base_font_size * 0.8), "bold")
        self.font_receipt = ("Courier", int(base_font_size * 0.9))
        self.font_label = ("Helvetica", int(base_font_size * 0.75))

        # Sizes for Icons and Canvases
        self.size_workspace_base_icon = int(self.responsive_workspace_height * 0.6)
        self.size_workspace_topping_icon = int(self.responsive_workspace_height * 0.3)
        self.size_selection_canvas = int(screen_height * 0.11)
        self.size_selection_icon = int(self.size_selection_canvas * 0.5)
        self.padding = int(screen_height / 120)
            
        pygame.mixer.music.stop()
        
        # --- UI Initialization ---
        nav_bar = tk.Frame(self, bg="lightpink")

        for page in tab_classes:
            cmd = partial(self.show_frame, page.__name__)
            b = tk.Button(nav_bar, text=page.__name__.replace("_"," ")[:-4], font=self.font_nav, command=cmd, bg="palevioletred", fg="white", borderwidth=0, highlightthickness=0, cursor="hand2")
            b.pack(side="left", padx=self.padding, pady=self.padding)

        close_button = tk.Button(nav_bar, text="X", font=self.font_nav, command=self.destroy, borderwidth=0, bg="mediumvioletred", fg="white", highlightthickness=0, cursor="hand2")
        close_button.pack(side="right", padx=self.padding, pady=self.padding)

        # --- Music Button Setup ---
        music_canvas_size = int(base_font_size * 1.3)
        self.music_canvas = tk.Canvas(nav_bar, width=music_canvas_size, height=music_canvas_size, bg="lightpink", highlightthickness=0, cursor="hand2")
        self.music_canvas.pack(side="right", padx=self.padding, pady=self.padding)
        
        self.music_icon_loader = Icons(self.music_canvas, size=(music_canvas_size, music_canvas_size))
        self.music_icon_loader.draw_icon("sound_on", music_canvas_size/2, music_canvas_size/2) 
        
        self.music_canvas.bind("<Button-1>", self.toggle_music) 

        self.tip_label = tk.Label(nav_bar, text=f"Wallet: $0", font=self.font_title, fg="green", bg="lightpink")
        self.tip_label.pack(side="right", padx=self.padding, pady=self.padding)

        nav_bar.pack(side="top", fill="x")
        
        # --- Main Frame for Content ---
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.create_order_panel(self.main_frame)

        # Create the Bowl Management Panel 
        self.bowl_management_panel = tk.Frame(self.main_frame)
        bowl_selection_frame = tk.Frame(self.bowl_management_panel, bg="seashell") 
        bowl_selection_frame.pack(side="top", fill="x", padx=self.padding, pady=(self.padding,0))
        self.bowl_buttons_frame = tk.Frame(bowl_selection_frame, bg="seashell", highlightthickness=0)
        self.bowl_buttons_frame.pack(side="left", fill="x", expand=True)
        self.bowl_remove_button = tk.Button(bowl_selection_frame, text="Throw Bowl", command=self.remove_bowl, font=self.font_button, bg="lightcoral", fg="white", borderwidth=0, highlightthickness=0, cursor="hand2")
        self.bowl_remove_button.pack(side="right", padx=self.padding, pady=self.padding)
        self.workspace_canvas = tk.Canvas(self.bowl_management_panel, height=self.responsive_workspace_height, bg="seashell", highlightthickness=0)
        self.workspace_canvas.pack(side="bottom", fill="x", padx=self.padding, pady=self.padding)
        
        self.workspace_canvas.bind("<ButtonPress-1>", self.on_workspace_press)
        self.workspace_canvas.bind("<B1-Motion>", self.on_workspace_drag)
        self.workspace_canvas.bind("<ButtonRelease-1>", self.on_workspace_release)

        # Create icon managers for the workspace canvas
        self.workspace_icon_manager = Icons(self.workspace_canvas, size=(self.size_workspace_base_icon, self.size_workspace_base_icon))
        self.toppings_icon_manager = Icons(self.workspace_canvas, size=(self.size_workspace_topping_icon, self.size_workspace_topping_icon))

        self.container = tk.Frame(self.main_frame, bg="seashell")
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
            self.music_icon_loader.draw_icon("sound_off", self.music_canvas.winfo_height()/2, self.music_canvas.winfo_height()/2)
            self.music_on = False
        else:
            pygame.mixer.music.play(loops=-1)
            self.music_icon_loader.draw_icon("sound_on", self.music_canvas.winfo_height()/2, self.music_canvas.winfo_height()/2)
            self.music_on = True


    def show_frame(self, page_name):
        self.current_page = page_name
        frame = self.pages[page_name]
        frame.tkraise()
        if page_name == "Order_Tab":
            self.bowl_management_panel.pack_forget()
        elif self.bowls:
             self.bowl_management_panel.pack(side="bottom", fill="x")


    def select_order(self, order_id, widget):
        """ Selects an order and displays its details in a pop-up window. """
        # --- Highlighting Logic ---
        for _, lbl in self.order_receipts:
            lbl.config(bg="white")
        widget.config(bg="#e3f5eb", relief="groove")
        self.selected_order = next((order for order in self.orders if order.order_id == order_id), None)
        

    def create_order_panel(self, parent):
        right_panel = tk.Frame(parent, width=self.responsive_right_panel_width, bg="lightblue")
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="Orders", font=self.font_title, bg="lightblue").pack(pady=self.padding)
        self.order_receipts = []
        scroll_container = tk.Frame(right_panel, bg="lightblue")
        scroll_container.pack(fill="both", expand=True, padx=self.padding, pady=self.padding)
        canvas = tk.Canvas(scroll_container, borderwidth=0, bg="lightblue", highlightthickness=0)
        scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        self.order_frame = tk.Frame(canvas, bg="lightblue")
        self.order_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame_id = canvas.create_window((0, 0), window=self.order_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        def on_canvas_configure(event):
            canvas.itemconfig(frame_id, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)


    def redraw_order_panel(self):
        """Clears and redraws all order receipts to match the self.orders list."""
        # Destroy all existing receipt widgets to clear the panel
        for widget in self.order_frame.winfo_children():
            widget.destroy()

        # Clear the list that tracks receipt widgets
        self.order_receipts.clear()

        # Re-create all receipts from the current self.orders list
        for order in self.orders:
            poke = order.orderedPoke
            
            # Recreate the text for the receipt label (logic from your register_order)
            vft_names = [item.name for item in poke.vft] if (poke.vft and not isinstance(poke.vft[0], str)) else poke.vft
            sauce_name = poke.sauce.name if hasattr(poke.sauce, 'name') else poke.sauce
            poke_text = f"- {poke.base.capitalize()}\n* {str(vft_names)[1:-2].replace(',', '\n*').replace('\'', '')}\n- {sauce_name}\n- {poke.protein.name}"
            
            label = tk.Label(self.order_frame, text=f"{order.order_id}\n{poke_text}", bg="white", font=self.font_receipt, bd=1, borderwidth=0, pady=self.padding, justify="left", padx=self.padding)
            label.pack(pady=self.padding, fill="x", padx=self.padding)
            
            # Re-bind the click event, capturing the current order_id and label
            label.bind("<Button-1>", lambda e, oid=order.order_id, lbl=label: self.select_order(oid, lbl))
            
            # Add the new receipt to the tracker list
            self.order_receipts.append((order.order_id, label))


    def register_order(self, poke, time_waited):
        order_id = f"Order #{1001+len(self.order_receipts)}"
        vft_names = [item.name for item in poke.vft] if (poke.vft and not isinstance(poke.vft[0], str)) else poke.vft
        sauce_name = poke.sauce.name if hasattr(poke.sauce, 'name') else poke.sauce
        poke_text = f"- {poke.base.capitalize()}\n* {str(vft_names)[1:-2].replace(',', '\n*').replace('\'', '')}\n- {sauce_name}\n- {poke.protein}"
        label = tk.Label(self.order_frame, text=f"{order_id}\n{poke_text}", bg="white", font=self.font_receipt, bd=1, borderwidth=0, pady=self.padding, justify="left", padx=self.padding)
        label.pack(pady=self.padding, fill="x", padx=self.padding)
        self.order_receipts.append((order_id, label))
        self.orders.append(Order(order_id, poke, time_waited))
        label.bind("<Button-1>", lambda e, oid=order_id, lbl=label: self.select_order(oid, lbl))
        return order_id


    def add_new_bowl(self):
        """ Adds a new bowl to the bowl management panel. """
        was_first_bowl = not self.bowls
        if was_first_bowl and self.current_page != "Order_Tab":
            self.bowl_management_panel.pack(side="bottom", fill="x")
        new_id = self.next_bowl_id
        self.bowls[new_id] = Poke()
        self.next_bowl_id += 1
        self.set_active_bowl(new_id)


    def remove_bowl(self):
        """ Removes a bowl from the bowl management panel. """
        if self.active_bowl_id in self.bowls:
            del self.bowls[self.active_bowl_id]
            if self.active_bowl_id == self.active_bowl_id:
                self.active_bowl_id = None
                self.redraw_workspace()
            self.update_bowl_selection_bar()
            if not self.bowls:
                self.bowl_management_panel.pack_forget()


    def set_active_bowl(self, bowl_id):
        self.active_bowl_id = bowl_id
        self.update_bowl_selection_bar()
        self.redraw_workspace()


    def update_bowl_selection_bar(self):
        for widget in self.bowl_buttons_frame.winfo_children():
            widget.destroy()
        for bowl_id, poke in sorted(self.bowls.items()):
            cmd = partial(self.set_active_bowl, bowl_id)
            btn = tk.Button(self.bowl_buttons_frame, text=f"Bowl {bowl_id}", command=cmd, relief="raised", font=self.font_button)
            if bowl_id == self.active_bowl_id:
                btn.config(relief="groove", bg="salmon", fg="white")
            btn.pack(side="left", padx=2, pady=2)


    def add_base_to_bowl(self, base):
        if self.active_bowl_id is None: return
        poke = self.bowls[self.active_bowl_id]
        if poke.base is not None:
            messagebox.showwarning("Base Already Set", "You can only set one base per bowl.")
            return
        poke.base = base
        poke.protein = None  # Reset protein when a new base is added
        poke.vft.clear()  # Clear toppings when a new base is added
        poke.sauce = None  # Clear sauce when a new base is added
        self.redraw_workspace()


    def set_ingredient_for_placement(self, ingredient_name):
        if self.active_bowl_id is None:
            messagebox.showwarning("No Active Bowl", "Please select a bowl before adding ingredients.")
            return
        self.sauce_to_draw = None 
        self.ingredient_to_place = ingredient_name
        self.workspace_canvas.config(cursor="crosshair")


    def set_sauce_for_drawing(self, sauce_name):
        if self.active_bowl_id is None:
            messagebox.showwarning("No Active Bowl", "Please select a bowl before adding sauce.")
            return
        self.ingredient_to_place = None 
        self.sauce_to_draw = sauce_name
        self.workspace_canvas.config(cursor="spraycan")


    def on_workspace_press(self, event):
        if self.sauce_to_draw:
            self.is_drawing_sauce = True
            self.sauce_path_points = [(event.x, event.y)]

        
    def on_workspace_drag(self, event):
        if not self.is_drawing_sauce: return
        self.sauce_path_points.append((event.x, event.y))
        if len(self.sauce_path_points) > 1:
            p1, p2 = self.sauce_path_points[-2], self.sauce_path_points[-1]
            color = self.sauce_colors.get(self.sauce_to_draw, "black")
            self.workspace_canvas.create_line(p1, p2, fill=color, width=5, capstyle=tk.ROUND, smooth=True)


    def on_workspace_release(self, event):
        if self.ingredient_to_place:
            distance_sq = (event.x - self.bowl_center_x)**2 + (event.y - self.bowl_center_y)**2
            if distance_sq <= self.bowl_radius**2:
                if type(self.ingredient_to_place) is str:
                    self.bowls[self.active_bowl_id].vft.append(VFT(name=self.ingredient_to_place, position=(event.x, event.y)))
                elif type(self.ingredient_to_place) is Protein: 
                    self.bowls[self.active_bowl_id].protein = deepcopy(self.ingredient_to_place)
                    self.bowls[self.active_bowl_id].protein.position = (event.x, event.y)
            self.ingredient_to_place = None 
        
        if self.is_drawing_sauce:
            self.is_drawing_sauce = False
            if len(self.sauce_path_points) > 1:
                self.bowls[self.active_bowl_id].sauce = Sauce(name=self.sauce_to_draw, path=self.sauce_path_points)
            self.sauce_to_draw = None 

        self.workspace_canvas.config(cursor="")
        self.redraw_workspace()


    def redraw_workspace(self):
        self.workspace_canvas.delete("all")
        if self.active_bowl_id is None: return
        
        self.update_idletasks()
        canvas_w, canvas_h = self.workspace_canvas.winfo_width(), self.workspace_canvas.winfo_height()

        self.bowl_center_x, self.bowl_center_y = canvas_w / 2, canvas_h / 2
        diameter = min(canvas_w, canvas_h) * 0.85
        self.bowl_radius = diameter / 2
        
        x1, y1 = self.bowl_center_x - self.bowl_radius, self.bowl_center_y - self.bowl_radius
        x2, y2 = self.bowl_center_x + self.bowl_radius, self.bowl_center_y + self.bowl_radius
        
        active_poke = self.bowls[self.active_bowl_id]
        self.workspace_canvas.create_oval(x1, y1, x2, y2, fill="peru", outline="saddlebrown", width=3)
        
        if active_poke.base:
            self.workspace_icon_manager.draw_icon(active_poke.base.replace(" ", "_").lower(), self.bowl_center_x, self.bowl_center_y)

        if active_poke.sauce and active_poke.sauce.path:
            color = self.sauce_colors.get(active_poke.sauce.name, "black")
            self.workspace_canvas.create_line(active_poke.sauce.path, fill=color, width=5, capstyle=tk.ROUND, smooth=True)

        if active_poke.vft:
            for vft_item in active_poke.vft:
                self.toppings_icon_manager.draw_icon(vft_item.name.replace(" ", "_").lower(), vft_item.position[0], vft_item.position[1])

        if active_poke.protein:
            self.toppings_icon_manager.draw_icon(active_poke.protein.name.replace(" ", "_").lower(), active_poke.protein.position[0], active_poke.protein.position[1])


    def serve_poke(self):
        if self.active_bowl_id is None:
            messagebox.showwarning("No Active Bowl", "Please select a bowl to serve.")
            return
        
        if self.selected_order is None:
            messagebox.showwarning("No Order Selected", "Please select an order to serve the bowl.")
            return
        
        tip, grade_w, grade_a, grade_c, grade_d = score(self.selected_order, self.bowls[self.active_bowl_id], self.extract_poke_layout_data())
        self.wallet += tip

        self.tip_label.configure(text=f"Wallet: ${self.wallet:.2f}")
        self.pages["Serve_Tab"].display_serving_feedback(tip, grade_w, grade_a, grade_c, grade_d) # Show feedback animation in the Serve tab
        self.pages["Order_Tab"].remove_client_from_waiting_area(self.selected_order.order_id) # Remove client from waiting area
        self.orders.remove(self.selected_order) # Remove order from orders list
        self.redraw_order_panel() # Redraw order panel with new order list
        self.remove_bowl() # Remove the bowl from the working aread
        self.selected_order = None # Set selected order to None (no order selected)


    def extract_poke_layout_data(self):
        """
        The "Inspector": Gathers all positional data for the active poke bowl.
        Returns a dictionary with ingredient positions, sauce path, and bowl geometry.
        """
        if self.active_bowl_id is None:
            return None

        active_poke = self.bowls[self.active_bowl_id]
        
        # Collect positions of all toppings (VFTs)
        ingredient_positions = [vft.position for vft in active_poke.vft] + [active_poke.protein.position] if active_poke.protein else []
        
        # Collect all points from the sauce path, if it exists
        sauce_path = active_poke.sauce.path if active_poke.sauce else []
        
        # Package all the "inspector's notes" together
        layout_data = {
            "ingredient_positions": ingredient_positions,
            "sauce_path": sauce_path,
            "bowl_center": (self.bowl_center_x, self.bowl_center_y),
            "bowl_radius": self.bowl_radius
        }

        return layout_data


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