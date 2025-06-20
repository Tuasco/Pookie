import tkinter as tk
from tkinter import messagebox

from Models.Poke import Poke
from Services.workspace_service import redraw_workspace


def set_active_bowl(self, bowl_id):
    self.active_bowl_id = bowl_id
    update_bowl_selection_bar(self)
    redraw_workspace(self)


def add_new_bowl(self):
    """ Adds a new bowl to the bowl management panel. """
    was_first_bowl = not self.bowls

    if was_first_bowl and self.current_page != "Order_Tab":
        self.bowl_management_panel.pack(side="bottom", fill="x")

    new_id = self.next_bowl_id
    self.bowls[new_id] = Poke()
    self.next_bowl_id += 1
    set_active_bowl(self, new_id)


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
    redraw_workspace(self)


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


def remove_bowl(self):
    """ Removes a bowl from the bowl management panel. """
    if self.active_bowl_id in self.bowls:
        del self.bowls[self.active_bowl_id]
        if self.active_bowl_id == self.active_bowl_id:
            self.active_bowl_id = None
            redraw_workspace(self)
        update_bowl_selection_bar(self)
        if not self.bowls:
            self.bowl_management_panel.pack_forget()


def update_bowl_selection_bar(self):
    for widget in self.bowl_buttons_frame.winfo_children():
        widget.destroy()
    for bowl_id, poke in sorted(self.bowls.items()):
        btn = tk.Button(self.bowl_buttons_frame, text=f"Bowl {bowl_id}", command=lambda: set_active_bowl(self, bowl_id), relief="raised", font=self.font_button)
        if bowl_id == self.active_bowl_id:
            btn.config(relief="groove", bg="salmon", fg="white")
        btn.pack(side="left", padx=2, pady=2)