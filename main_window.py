import tkinter as tk
from functools import partial

from GUI import order_tab, base_tab, veg_fruit_tab, protein_tab, extras_sauces_tab, serve_tab
from Data.Icons import Icons
from Services.music_service import init_music, toggle_music
from Services.bowl_service import remove_bowl
from Services.workspace_service import on_workspace_drag, on_workspace_press, on_workspace_release

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

        # --- Initialise music ---
        init_music(self, "www/mm.mp3")

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
        
        self.music_canvas.bind("<Button-1>", lambda e: toggle_music(self, e))

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
        self.bowl_remove_button = tk.Button(bowl_selection_frame, text="Throw Bowl", command=lambda: remove_bowl(self), font=self.font_button, bg="lightcoral", fg="white", borderwidth=0, highlightthickness=0, cursor="hand2")
        self.bowl_remove_button.pack(side="right", padx=self.padding, pady=self.padding)
        self.workspace_canvas = tk.Canvas(self.bowl_management_panel, height=self.responsive_workspace_height, bg="seashell", highlightthickness=0)
        self.workspace_canvas.pack(side="bottom", fill="x", padx=self.padding, pady=self.padding)
        
        self.workspace_canvas.bind("<ButtonPress-1>", lambda e: on_workspace_press(self, e))
        self.workspace_canvas.bind("<B1-Motion>", lambda e: on_workspace_drag(self, e))
        self.workspace_canvas.bind("<ButtonRelease-1>", lambda e: on_workspace_release(self, e))

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


    def show_frame(self, page_name):
        self.current_page = page_name
        frame = self.pages[page_name]
        frame.tkraise()
        if page_name == "Order_Tab":
            self.bowl_management_panel.pack_forget()
        elif self.bowls:
             self.bowl_management_panel.pack(side="bottom", fill="x")
        

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


    def sec_loop(self):
        if "Order_Tab" in self.pages:
            self.pages["Order_Tab"].show_random_client(self.timer)
        self.timer += 1
        self.after(1000, self.sec_loop)


if __name__=="__main__":
    app = PookieGUI()
    app.mainloop()