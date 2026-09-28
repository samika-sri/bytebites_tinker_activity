"""
Manual verification scenario for the ByteBites classes.

Walks through a realistic ordering session: build a menu, inspect the
objects, filter it, place an order, total it, and file that order into a
customer's history. Every step prints what it expected alongside what it
got, so a wrong result is visible without reading the code.

Note: the spec and bytebites_design.mmd define no sorting method, so
there is nothing to sort here. Items are inspected in insertion order.

Run with:  python3 demo.py
"""

from models import Item, Menu, Order, Customer


def check(label: str, actual, expected) -> None:
    """Print one comparison line and flag it if the values disagree."""
    mark = "ok  " if actual == expected else "FAIL"
    print(f"  [{mark}] {label}: got {actual!r}, expected {expected!r}")


# --- 1. Create sample items and inspect their stored attributes --------

print("\n1. Sample items")

burger = Item("Spicy Burger", 8.50, "Entrees", 4.7)
soda = Item("Large Soda", 2.25, "Drinks", 4.1)
coffee = Item("Iced Coffee", 3.75, "Drinks", 4.8)
cake = Item("Lava Cake", 5.00, "Desserts", 4.9)

for item in (burger, soda, coffee, cake):
    print(f"  {item.get_name():<14} ${item.get_price():>5.2f}  "
          f"{item.get_category():<9} rating {item.get_popularity_rating()}")

check("burger name", burger.get_name(), "Spicy Burger")
check("burger price", burger.get_price(), 8.50)
check("soda category", soda.get_category(), "Drinks")
check("cake rating", cake.get_popularity_rating(), 4.9)


# --- 2. Build the menu -------------------------------------------------

print("\n2. Adding items to the menu")

menu = Menu()
check("new menu is empty", menu.get_items(), [])

for item in (burger, soda, coffee, cake):
    menu.add_item(item)

check("menu size after 4 adds", len(menu.get_items()), 4)
print("  menu:", [i.get_name() for i in menu.get_items()])


# --- 3. Filter by category --------------------------------------------

print("\n3. Filtering by category")

drinks = menu.filter_by_category("Drinks")
check("drinks found", [i.get_name() for i in drinks],
      ["Large Soda", "Iced Coffee"])

check("filtering is case-insensitive",
      [i.get_name() for i in menu.filter_by_category("dRiNkS")],
      ["Large Soda", "Iced Coffee"])

check("desserts found", [i.get_name() for i in menu.filter_by_category("Desserts")],
      ["Lava Cake"])

check("unknown category returns empty list",
      menu.filter_by_category("Sides"), [])

check("filtering does not shrink the menu", len(menu.get_items()), 4)


# --- 4. Removing from the menu ----------------------------------------

print("\n4. Removing menu items")

ghost = Item("Not On Menu", 1.00, "Sides", 3.0)
menu.remove_item(ghost)
check("removing an absent item is a no-op", len(menu.get_items()), 4)

menu.remove_item(cake)
check("menu size after removing Lava Cake", len(menu.get_items()), 3)
check("Lava Cake is gone", menu.filter_by_category("Desserts"), [])

menu.add_item(cake)  # put it back for the rest of the scenario

stolen = menu.get_items()
stolen.append(ghost)
check("mutating the returned list cannot change the menu",
      len(menu.get_items()), 4)


# --- 5. Place an order and total it ------------------------------------

print("\n5. Building an order")

order = Order()
check("new order totals zero", order.calculate_total(), 0.0)

order.add_item(burger)
order.add_item(soda)
order.add_item(soda)   # two sodas: the same Item appears twice
order.add_item(cake)

print("  ordered:", [i.get_name() for i in order.get_items()])
check("item count counts duplicates", len(order.get_items()), 4)

# 8.50 + 2.25 + 2.25 + 5.00
check("order total", round(order.calculate_total(), 2), 18.00)

order.remove_item(soda)
check("removing one soda drops exactly one",
      len(order.get_items()), 3)
check("total recomputes after removal",
      round(order.calculate_total(), 2), 15.75)


# --- 6. Customer and purchase history ----------------------------------

print("\n6. Customer history")

sam = Customer("Sam")
check("customer name", sam.get_name(), "Sam")
check("new customer has no history", sam.get_purchase_history(), [])
check("new customer is not returning", sam.is_returning_customer(), False)

sam.add_order(order)
check("history holds one order", len(sam.get_purchase_history()), 1)
check("customer is now returning", sam.is_returning_customer(), True)

second = Order()
second.add_item(coffee)
sam.add_order(second)
check("history holds two orders", len(sam.get_purchase_history()), 2)
check("second order total", round(second.calculate_total(), 2), 3.75)

check("history totals",
      [round(o.calculate_total(), 2) for o in sam.get_purchase_history()],
      [15.75, 3.75])

print("\nScenario complete.\n")
