from Models.Order import Order
import tkinter as tk

def select_order(self, order_id, widget):
    """ Selects an order and displays its details in a pop-up window. """
    for _, lbl in self.order_receipts:
        lbl.config(bg="white")

    widget.config(bg="#e3f5eb", relief="groove")
    self.selected_order = next((order for order in self.orders if order.order_id == order_id), None)


def register_order(self, poke, time_waited):
    order_id = f"Order #{1001+len(self.order_receipts)}"
    vft_names = [item.name for item in poke.vft] if (poke.vft and not isinstance(poke.vft[0], str)) else poke.vft
    sauce_name = poke.sauce.name if hasattr(poke.sauce, 'name') else poke.sauce
    poke_text = f"- {poke.base.capitalize()}\n* {str(vft_names)[1:-2].replace(',', '\n*').replace('\'', '')}\n- {sauce_name}\n- {poke.protein}"
    label = tk.Label(self.order_frame, text=f"{order_id}\n{poke_text}", bg="white", font=self.font_receipt, bd=1, borderwidth=0, pady=self.padding, justify="left", padx=self.padding)
    label.pack(pady=self.padding, fill="x", padx=self.padding)
    self.order_receipts.append((order_id, label))
    self.orders.append(Order(order_id, poke, time_waited))
    label.bind("<Button-1>", lambda e, oid=order_id, lbl=label: select_order(self, oid, lbl))
    return order_id


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
        label.bind("<Button-1>", lambda e, oid=order.order_id, lbl=label: select_order(self, oid, lbl))
            
        # Add the new receipt to the tracker list
        self.order_receipts.append((order.order_id, label))