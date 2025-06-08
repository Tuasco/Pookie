import tkinter as tk
from Data.Icons import Icons

base_names = ["salad", "rice", "brown rice", "quinoa", "pasta", "buckwheat"]

class Base_Tab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="seashell")
        self.controller = controller
        
        new_bowl_button = tk.Button(
            self, 
            text="+ New Bowl", 
            font=self.controller.font_button,
            command=self.controller.add_new_bowl
        )
        new_bowl_button.pack(side="left", pady=self.controller.padding*2, padx=self.controller.padding)

        separator = tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=5)
        
        label = tk.Label(self, text="Select Base", font=self.controller.font_title, bg="seashell")
        label.pack(pady=self.controller.padding)
        
        bowls_container = tk.Frame(self, bg="seashell")
        bowls_container.pack(pady=self.controller.padding, padx=self.controller.padding)
        
        for base in base_names:
            bowl_widget = BaseBowl(bowls_container, base_name=base, controller=self.controller)
            bowl_widget.pack(side=tk.LEFT, padx=self.controller.padding, pady=self.controller.padding)

class BaseBowl(tk.Frame):
    def __init__(self, parent, base_name, controller):
        super().__init__(parent, bg="seashell", padx=5, pady=5)
        self.base_name = base_name
        self.controller = controller

        label = tk.Label(self, text=base_name.capitalize(), font=self.controller.font_label, bg="seashell", fg="saddlebrown")
        label.pack(pady=5)

        canvas_size = self.controller.size_selection_canvas
        self.bowl_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg="seashell", cursor="hand2")
        self.bowl_canvas.pack()
        
        icon_size = self.controller.size_selection_icon
        self.icon_manager = Icons(self.bowl_canvas, size=(icon_size, icon_size))
        
        self.draw_bowl_and_icon(base_name.replace(" ", "_"))

        self.bowl_canvas.bind("<Button-1>", self.on_select_base)
        label.bind("<Button-1>", self.on_select_base)

    def draw_bowl_and_icon(self, base):
        canvas_size = self.controller.size_selection_canvas
        padding = int(canvas_size * 0.08)
        self.bowl_canvas.create_oval(padding, padding, canvas_size-padding, canvas_size-padding, fill="burlywood", outline="saddlebrown", width=2)
        self.icon_manager.draw_icon(base.lower(), canvas_size/2, canvas_size/2)

    def on_select_base(self, event):
        self.controller.add_base_to_bowl(self.base_name)