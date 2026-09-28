""" 
Four classes:
- Item: A single food item sold by ByteBites. Holds name, price, category, and popularity rating. Read-only data holder; no behavior beyond getters.
- Menu: The full collection of items available. Supports adding and removing items and filtering the collection by category. Holds items but does not own them the same Item can appear in orders.
- Order: One transaction: the items a customer picked, grouped together. Computes its total cost on demand rather than storing it, so the total can never go stale as items are added or removed.
- Customer: A ByteBites user. Holds a name and a list of past Orders, which doubles as the check for whether they are a returning customer.
          
"""
