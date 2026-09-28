""" 
Four classes:
- Item: A single food item sold by ByteBites. Holds name, price, category, and popularity rating. Read-only data holder; no behavior beyond getters.
- Menu: The full collection of items available. Supports adding and removing items and filtering the collection by category. Holds items but does not own them the same Item can appear in orders.
- Order: One transaction: the items a customer picked, grouped together. Computes its total cost on demand rather than storing it, so the total can never go stale as items are added or removed.
- Customer: A ByteBites user. Holds a name and a list of past Orders, which doubles as the check for whether they are a returning customer.
          
"""

class Item:
    def __init__(self, name: str, price: float, category: str,
                 popularity_rating: float):
        self._name = name
        self._price = price
        self._category = category
        self._popularity_rating = popularity_rating

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        return self._price

    def get_category(self) -> str:
        return self._category

    def get_popularity_rating(self) -> float:
        return self._popularity_rating


class Menu:
    def __init__(self):
        self._items: list[Item] = []


class Order:
    def __init__(self):
        self._items: list[Item] = []


class Customer:
    def __init__(self, name: str):
        self._name = name
        self._purchase_history: list[Order] = []
