from abc import ABC, abstractmethod

class MenuComponent(ABC):
    """
    Abstract base class representing a menu component.
    """

    @abstractmethod
    def calculate_price(self) -> int:
        """Calculates and returns the price of the MenuComponent """

    @abstractmethod
    def display(self, indent: int) -> None:
        """
        Displays information about MenuComponent with given indentation.
        :param indent: Indentation level (number of spaces).
        """

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        """
        Sets and validates the name of the component.
        :param value: New name as a non-empty string.
        :raises TypeError: If value is not a string.
        :raises ValueError: If value is empty.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name can not be empty")
        self.__name = value


class Dish(MenuComponent):
    """
    Represents a single dish.
    """
    def __init__(self, name: str, price: int):
        """
        Initializes a dish with a name and a positive integer price.
        :param name: Name of the dish.
        :param price: Price of the dish.
        :raises TypeError: If price is not an integer.
        :raises ValueError: If price is not positive.
        """
        self.name = name
        if not isinstance(price, int):
            raise TypeError('Price must be integer number')
        if price <= 0:
            raise ValueError('Price must be greater than 0')
        self.__price = price

    def calculate_price(self) -> int:
        """Calculates and returns the price of the Dish """
        return self.__price
    
    def display(self, indent: int = 0) -> None:
        """
        Displays name and price of the dish with indentation.
        :param indent: Number of spaces before the text.
        :raises TypeError: If indent is not an integer.
        :raises ValueError: If indent is negative.
        """
        if not isinstance(indent, int):
            raise TypeError("Indent must be an integer number")
        if indent < 0:
            raise ValueError("Indent can not be negative")
        print(f"{' ' * indent}Dish: '{self.name}', price = {self.calculate_price()}")


class Order(MenuComponent):
    """
    Represents a composite order that can contain dishes and/or sub-orders.
    """
    def __init__(self, name: str):
        """
        Initializes an order with a name and empty component list.
        :param name: Name of the order.
        """
        self.name = name
        self.__components = []

    def add(self, item: MenuComponent):
        """
        Adds a dish or sub-order to this order.
        :param item: MenuComponent.
        :raises TypeError: If item is not a MenuComponent.
        """
        if not isinstance(item, MenuComponent):
            raise TypeError("Item must be an instance of MenuComponent")
        self.__components.append(item)
    
    def remove(self, item: MenuComponent):
        """
        Removes a dish or sub-order from this order.
        :param item: MenuComponent to remove.
        :raises TypeError: If item is not a MenuComponent.
        """
        if not isinstance(item, MenuComponent):
            raise TypeError("Item must be an instance of MenuComponent")
        if item in self.__components:
            self.__components.remove(item)

    def calculate_price(self) -> int:
        """
        Calculates the total price of all components in this order.
        :return: Total price.
        """
        return sum(component.calculate_price() for component in self.__components)

    def display(self, indent: int = 0) -> None:
        """
        Displays the order and all its components with indentation.
        :param indent: Number of spaces before the text.
        :raises TypeError: If indent is not an integer.
        :raises ValueError: If indent is negative.
        """
        if not isinstance(indent, int):
            raise TypeError("Indent must be an integer number")
        if indent < 0:
            raise ValueError("Indent can not be negative")
        print(f"{' ' * indent}Order: '{self.name}'")
        for component in self.__components:
            component.display(indent+2)


def main():
    """
    Demonstration of the Composite pattern:
    Creates dishes and combines them into nested orders, then displays the structure and total price.
    """
    coffee = Dish('Coffee', 2)
    soup = Dish('Soup', 10)
    salad = Dish('Salad', 8)

    soup.display()
    print('-'*40)

    order1 = Order('Order 1')
    order1.add(coffee)
    order1.add(salad)

    order2 = Order('Order 2')
    order2.add(order1)
    order2.add(Dish('Cheesecake', 18))
    
    order2.display()
    print(f"Total = {order2.calculate_price()}")

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()