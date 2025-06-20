import tkinter as tk
from Data.Icons import Icons
from Services.bowl_service import add_new_bowl, add_base_to_bowl
from Services.workspace_service import draw_bowl_and_icon

base_names = ["salad", "rice", "brown rice", "quinoa", "pasta", "buckwheat"]
bg_color = "seashell"  # Define a background color for the tab
fg_color = "saddlebrown"  # Define a foreground color for the tab

class Base_Tab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=bg_color)
        self.controller = controller
        
        new_bowl_button = tk.Button(
            self, 
            text="+ New Bowl", 
            font=self.controller.font_button,
            command=lambda: add_new_bowl(self.controller),
        )
        new_bowl_button.pack(side="left", pady=self.controller.padding*2, padx=self.controller.padding)

        separator = tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=5)
        
        label = tk.Label(self, text="Select Base", font=self.controller.font_title, bg=bg_color, fg=fg_color)
        label.pack(pady=self.controller.padding)
        
        bowls_container = tk.Frame(self, bg=bg_color)
        bowls_container.pack(pady=self.controller.padding, padx=self.controller.padding)
        
        for base in base_names:
            bowl_widget = BaseBowl(bowls_container, base_name=base, controller=self.controller)
            bowl_widget.pack(side=tk.LEFT, padx=self.controller.padding, pady=self.controller.padding)


class BaseBowl(tk.Frame):
    def __init__(self, parent, base_name, controller):
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        self.base_name = base_name
        self.controller = controller

        label = tk.Label(self, text=base_name.capitalize(), font=self.controller.font_label, bg=bg_color, fg="saddlebrown")
        label.pack(pady=5)

        canvas_size = self.controller.size_selection_canvas
        self.bowl_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg=bg_color, cursor="hand2")
        self.bowl_canvas.pack()
        
        icon_size = self.controller.size_selection_icon
        self.icon_manager = Icons(self.bowl_canvas, size=(icon_size, icon_size))
        
        draw_bowl_and_icon(self, base_name)

        self.bowl_canvas.bind("<Button-1>", lambda e: add_base_to_bowl(self.controller, self.base_name))
        label.bind("<Button-1>", lambda e: add_base_to_bowl(self.controller, self.base_name))