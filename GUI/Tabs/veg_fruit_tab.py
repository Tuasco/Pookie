import tkinter as tk
from Data.Icons import Icons

veggies= ["carrot", "broccoli", "beet", "tomato", "cucumber", "mushroom", "onion", "peas"]
fruits = ["dragon fruit", "melon", "watermelon", "grapes", "kiwi", "avocado", "raspberry"]
bg_color = "seashell"

class Veg_Fruit_Tab(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=bg_color)
        self.controller = controller

        label = tk.Label(self, text="Select Veggies", font=self.controller.font_title, bg=bg_color)
        label.pack(pady=self.controller.padding)
        
        veg_container = tk.Frame(self, bg=bg_color)
        veg_container.pack(pady=self.controller.padding, padx=self.controller.padding)
        
        label = tk.Label(self, text="Select Fruits", font=self.controller.font_title, bg=bg_color)
        label.pack(pady=self.controller.padding)
        
        fruits_container = tk.Frame(self, bg=bg_color)
        fruits_container.pack(pady=self.controller.padding, padx=self.controller.padding)  
        
        for veggie in veggies:
            bowl_widget = VegFruitBowl(veg_container, veg_fruit_name=veggie, controller=self.controller)
            bowl_widget.pack(side=tk.LEFT, padx=self.controller.padding, pady=self.controller.padding)

        for fruit in fruits:
            bowl_widget = VegFruitBowl(fruits_container, veg_fruit_name=fruit, controller=self.controller)
            bowl_widget.pack(side=tk.LEFT, padx=self.controller.padding, pady=self.controller.padding)
       
class VegFruitBowl(tk.Frame):
    def __init__(self, parent, veg_fruit_name, controller):
        super().__init__(parent, bg=bg_color, padx=5, pady=5)
        self.veg_fruit_name = veg_fruit_name
        self.controller = controller

        label = tk.Label(self, text=veg_fruit_name.capitalize(), font=self.controller.font_label, bg=bg_color, fg="saddlebrown")
        label.pack(pady=5)

        canvas_size = self.controller.size_selection_canvas
        self.bowl_canvas = tk.Canvas(self, width=canvas_size, height=canvas_size, highlightthickness=0, bg=bg_color, cursor="hand2")
        self.bowl_canvas.pack()
        
        icon_size = self.controller.size_selection_icon
        self.icon_manager = Icons(self.bowl_canvas, size=(icon_size, icon_size))
        
        self.draw_bowl_and_icon(veg_fruit_name.replace(" ", "_"))

        self.bowl_canvas.bind("<Button-1>", self.on_select)
        label.bind("<Button-1>", self.on_select)


    def draw_bowl_and_icon(self, veg_fruit):
        canvas_size = self.controller.size_selection_canvas
        padding = int(canvas_size * 0.08)
        self.bowl_canvas.create_oval(padding, padding, canvas_size-padding, canvas_size-padding, fill="burlywood", outline="saddlebrown", width=2)
        self.icon_manager.draw_icon(veg_fruit.lower(), canvas_size/2, canvas_size/2)

    def on_select(self, event):
        self.controller.set_ingredient_for_placement(self.veg_fruit_name)