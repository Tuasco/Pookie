import tkinter as tk

from Data.Icons import Icons
from Services.bowl_service import set_ingredient_for_placement, set_sauce_for_drawing
from Services.workspace_service import draw_bowl_and_icon

extra_names = ["edamame", "mint", "lemon", "corn", "sesame"]
sauce_names = ["soy sauce", "sriracha", "sour cream", "wasabi"]
bg_color = "seashell"


class Extras_Sauces_Tab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=bg_color)
        self.controller = controller
        
        label = tk.Label(self, text="Select Extras", font=self.controller.font_title, bg=bg_color)
        label.pack(pady=self.controller.padding)
        
        extras_container = tk.Frame(self, bg=bg_color)
        extras_container.pack(pady=self.controller.padding, padx=self.controller.padding)
        
        label = tk.Label(self, text="Select Sauces", font=self.controller.font_title, bg=bg_color)
        label.pack(pady=self.controller.padding)
        
        sauces_container = tk.Frame(self, bg=bg_color)
        sauces_container.pack(pady=self.controller.padding, padx=self.controller.padding)
        
        for extra in extra_names:
            bowl_widget = ExtrasSaucesBowl(extras_container, item_name=extra, controller=self.controller)
            bowl_widget.pack(side=tk.LEFT, padx=self.controller.padding, pady=self.controller.padding)
            
        for sauce in sauce_names:
            bowl_widget = ExtrasSaucesBowl(sauces_container, item_name=sauce, controller=self.controller)
            bowl_widget.pack(side=tk.LEFT, padx=self.controller.padding, pady=self.controller.padding)
            

class ExtrasSaucesBowl(tk.Frame):
    def __init__(self, parent, item_name, controller):
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        self.item_name = item_name
        self.controller = controller

        label = tk.Label(self, text=item_name.capitalize(), font=self.controller.font_label, bg=bg_color, fg="saddlebrown")
        label.pack(pady=5)

        canvas_size = self.controller.size_selection_canvas
        self.bowl_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg=bg_color)
        self.bowl_canvas.pack()

        icon_size = self.controller.size_selection_icon
        self.icon_manager = Icons(self.bowl_canvas, size=(icon_size, icon_size))

        if self.item_name in extra_names:
            draw_bowl_and_icon(self, self.item_name)
            self.bowl_canvas.config(cursor="hand2")
            self.bowl_canvas.bind("<Button-1>", lambda e: set_ingredient_for_placement(self.controller, self.item_name))
            label.bind("<Button-1>", lambda e: set_ingredient_for_placement(self.controller, self.item_name))
        else:
            self.draw_icon(self.item_name.replace(" ", "_").lower())
            self.bowl_canvas.config(cursor="hand2")
            self.bowl_canvas.bind("<Button-1>", lambda e: set_sauce_for_drawing(self.controller, self.item_name))
            label.bind("<Button-1>", lambda e: set_sauce_for_drawing(self.controller, self.item_name))


    def draw_icon(self, sauce):
        canvas_size = self.controller.size_selection_canvas
        self.icon_manager.draw_icon(sauce, canvas_size/2, canvas_size/2)