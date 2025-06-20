from tkinter import messagebox
from Services.bowl_service import remove_bowl
from Services.order_service import redraw_order_panel
from Services.score_service import score


def serve_poke(self):
    if self.active_bowl_id is None:
        messagebox.showwarning("No Active Bowl", "Please select a bowl to serve.")
        return
        
    if self.selected_order is None:
        messagebox.showwarning("No Order Selected", "Please select an order to serve the bowl.")
        return
        
    tip, grade_w, grade_a, grade_c, grade_d = score(self.selected_order, self.bowls[self.active_bowl_id], extract_poke_layout_data(self))
    self.wallet += tip

    self.tip_label.configure(text=f"Wallet: ${self.wallet:.2f}")
    self.pages["Serve_Tab"].display_serving_feedback(tip, grade_w, grade_a, grade_c, grade_d) # Show feedback animation in the Serve tab
    self.pages["Order_Tab"].remove_client_from_waiting_area(self.selected_order.order_id) # Remove client from waiting area
    self.orders.remove(self.selected_order) # Remove order from orders list
    redraw_order_panel(self) # Redraw order panel with new order list
    remove_bowl(self) # Remove the bowl from the working aread
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