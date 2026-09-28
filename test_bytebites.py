

import pytest

from models import Item, Menu, Order, Customer


@pytest.fixture
def burger():
    return Item("Spicy Burger", 10.00, "Entrees", 4.7)


@pytest.fixture
def soda():
    return Item("Large Soda", 5.00, "Drinks", 4.1)


@pytest.fixture
def coffee():
    return Item("Iced Coffee", 3.75, "Drinks", 4.8)


@pytest.fixture
def cake():
    return Item("Lava Cake", 5.00, "Desserts", 4.9)


@pytest.fixture
def menu(burger, soda, coffee, cake):
    """A menu holding one entree, two drinks, and one dessert."""
    filled = Menu()
    for item in (burger, soda, coffee, cake):
        filled.add_item(item)
    return filled


@pytest.fixture
def order():
    return Order()


@pytest.fixture
def customer():
    return Customer("Sam")



class TestItem:
    """An Item holds the four facts it was built with."""

    def test_item_reports_the_values_it_was_created_with(self):
        burger = Item("Spicy Burger", 8.50, "Entrees", 4.7)
        assert burger.get_name() == "Spicy Burger"
        assert burger.get_price() == pytest.approx(8.50)
        assert burger.get_category() == "Entrees"
        assert burger.get_popularity_rating() == pytest.approx(4.7)




class TestMenuContents:
    """Adding to and removing from the menu."""

    def test_new_menu_has_no_items(self):
        assert Menu().get_items() == []

    def test_add_item_puts_the_item_on_the_menu(self, burger):
        blank = Menu()
        blank.add_item(burger)
        assert blank.get_items() == [burger]

    def test_remove_item_takes_the_item_off_the_menu(self, menu, burger):
        menu.remove_item(burger)
        assert burger not in menu.get_items()
        assert len(menu.get_items()) == 3

    def test_removing_an_item_that_is_not_on_the_menu_changes_nothing(self, menu):
       
        never_added = Item("Not On Menu", 1.00, "Sides", 3.0)
        menu.remove_item(never_added)
        assert len(menu.get_items()) == 4

    def test_removing_from_an_empty_menu_changes_nothing(self, burger):
        blank = Menu()
        blank.remove_item(burger)
        assert blank.get_items() == []

    def test_changing_the_returned_list_does_not_change_the_menu(self, menu, cake):
        
        menu.get_items().append(cake)
        assert len(menu.get_items()) == 4




class TestMenuFiltering:
    """Filtering a menu down to one category."""

    def test_filter_by_category_returns_only_items_in_that_category(
            self, menu, soda, coffee):
        assert menu.filter_by_category("Drinks") == [soda, coffee]

    def test_filter_by_category_returns_a_single_match(self, menu, cake):
        assert menu.filter_by_category("Desserts") == [cake]

    @pytest.mark.parametrize("written_as", ["Drinks", "drinks", "DRINKS", "dRiNkS"])
    def test_filter_by_category_ignores_capitalization(
            self, menu, soda, coffee, written_as):
        assert menu.filter_by_category(written_as) == [soda, coffee]

    @pytest.mark.parametrize("written_as", ["  Drinks", "Drinks  ", "  Drinks  "])
    def test_filter_by_category_ignores_surrounding_spaces(
            self, menu, soda, coffee, written_as):
        assert menu.filter_by_category(written_as) == [soda, coffee]

    def test_filter_by_unknown_category_returns_an_empty_list(self, menu):
        
        assert menu.filter_by_category("Sides") == []

    def test_filter_on_an_empty_menu_returns_an_empty_list(self):
        assert Menu().filter_by_category("Drinks") == []

    def test_filtering_does_not_remove_anything_from_the_menu(self, menu):
        menu.filter_by_category("Drinks")
        assert len(menu.get_items()) == 4


class TestOrderTotal:
    """Adding items to a transaction and totalling it."""

    def test_calculate_total_with_multiple_items(self, order, burger, soda):
       
        order.add_item(burger)
        order.add_item(soda)
        assert order.calculate_total() == pytest.approx(15.00)

    def test_calculate_total_with_one_item_is_that_items_price(self, order, burger):
        order.add_item(burger)
        assert order.calculate_total() == pytest.approx(10.00)

    def test_order_total_is_zero_when_empty(self, order):
        
        assert order.calculate_total() == pytest.approx(0.00)

    def test_empty_order_total_is_a_float(self, order):
        
        assert isinstance(order.calculate_total(), float)

    def test_calculate_total_counts_the_same_item_twice(self, order, soda):
        
        order.add_item(soda)
        order.add_item(soda)
        assert order.calculate_total() == pytest.approx(10.00)

    def test_total_goes_back_down_after_an_item_is_removed(
            self, order, burger, soda):
        
        order.add_item(burger)
        order.add_item(soda)
        order.remove_item(soda)
        assert order.calculate_total() == pytest.approx(10.00)

    def test_total_returns_to_zero_when_every_item_is_removed(self, order, burger):
        order.add_item(burger)
        order.remove_item(burger)
        assert order.calculate_total() == pytest.approx(0.00)

    def test_total_rises_when_an_item_is_added_after_an_earlier_total(
            self, order, burger, soda):
       
        order.add_item(burger)
        assert order.calculate_total() == pytest.approx(10.00)
        order.add_item(soda)
        assert order.calculate_total() == pytest.approx(15.00)

    def test_total_falls_when_an_item_is_removed_after_an_earlier_total(
            self, order, burger, soda):
        order.add_item(burger)
        order.add_item(soda)
        assert order.calculate_total() == pytest.approx(15.00)
        order.remove_item(soda)
        assert order.calculate_total() == pytest.approx(10.00)

    def test_totals_handle_prices_that_do_not_divide_evenly(self, order, coffee):
        
        order.add_item(coffee)
        order.add_item(coffee)
        assert order.calculate_total() == pytest.approx(7.50)



class TestOrderContents:
    """The list of items inside a transaction."""

    def test_new_order_has_no_items(self, order):
        assert order.get_items() == []

    def test_add_item_puts_the_item_in_the_order(self, order, burger):
        order.add_item(burger)
        assert order.get_items() == [burger]

    def test_the_same_item_can_be_added_twice(self, order, soda):
        order.add_item(soda)
        order.add_item(soda)
        assert order.get_items() == [soda, soda]

    def test_remove_item_takes_away_only_one_copy(self, order, soda):
       
        order.add_item(soda)
        order.add_item(soda)
        order.remove_item(soda)
        assert order.get_items() == [soda]

    def test_removing_an_item_not_in_the_order_changes_nothing(
            self, order, burger, soda):
        order.add_item(burger)
        order.remove_item(soda)
        assert order.get_items() == [burger]

    def test_changing_the_returned_list_does_not_change_the_order(
            self, order, burger, soda):
        order.add_item(burger)
        order.get_items().append(soda)
        assert order.get_items() == [burger]



class TestCustomer:
    """A customer's name and purchase history."""

    def test_customer_reports_its_name(self, customer):
        assert customer.get_name() == "Sam"

    def test_new_customer_has_an_empty_purchase_history(self, customer):
        assert customer.get_purchase_history() == []

    def test_new_customer_is_not_a_returning_customer(self, customer):
       
        assert customer.is_returning_customer() is False

    def test_customer_is_returning_after_one_order(self, customer, order):
        customer.add_order(order)
        assert customer.is_returning_customer() is True

    def test_add_order_puts_the_order_in_the_history(self, customer, order):
        customer.add_order(order)
        assert customer.get_purchase_history() == [order]

    def test_history_keeps_orders_in_the_order_they_were_added(
            self, customer, order):
        second = Order()
        customer.add_order(order)
        customer.add_order(second)
        assert customer.get_purchase_history() == [order, second]

    def test_orders_in_history_can_still_be_totalled(
            self, customer, order, burger):
        order.add_item(burger)
        customer.add_order(order)
        stored = customer.get_purchase_history()[0]
        assert stored.calculate_total() == pytest.approx(10.00)

    def test_changing_the_returned_history_does_not_change_the_customer(
            self, customer, order):
        customer.get_purchase_history().append(order)
        assert customer.get_purchase_history() == []
