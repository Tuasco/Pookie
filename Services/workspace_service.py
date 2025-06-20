import tkinter as tk
from copy import deepcopy

from Models.VFT import VFT
from Models.Protein import Protein
from Models.Sauce import Sauce


def draw_bowl_and_icon(self, base):
    canvas_size = self.controller.size_selection_canvas
    padding = int(canvas_size * 0.08)
    self.bowl_canvas.create_oval(padding, padding, canvas_size-padding, canvas_size-padding, fill="burlywood", outline="saddlebrown", width=2)
    self.icon_manager.draw_icon(base.replace(' ', '_').lower(), canvas_size/2, canvas_size/2)


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
    redraw_workspace(self)


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