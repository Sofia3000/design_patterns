from abc import ABC, abstractmethod
from typing import Any

PRECISION = 2

class SimpleTextField:
    """
    Descriptor class for validating non-empty string fields.
    Ensures the value is a non-empty string.

    :raises TypeError: If value is not a string.
    :raises ValueError: If value is an empty string.
    """

    def __set_name__(self, owner, name):
        self.name = name
        self.attr_name = '__' + self.name.lstrip('_')

    def __get__(self, instance, owner):
        return getattr(instance, self.attr_name, None)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"'{self.name}' must be an instance of string.")
        if not value.strip():
            raise ValueError(f"'{self.name}' must not be empty.")
        setattr(instance, self.attr_name, value)


class Product(ABC):
    """
    Abstract base class representing a product.

    :param price: Product price.
    :param name: Product name.
    :param producer: Product producer or manufacturer.
    """

    name = SimpleTextField()
    producer = SimpleTextField()

    def __init__(self, price: float, name: str, producer: str):
        self.price = price
        self.name = name
        self.producer = producer

    @property
    def price(self) -> str:
        """
        Get the product price.

        :return: Product price.
        """
        return self.__price

    @price.setter
    def price(self, price: float):
        """
        Set and validate the product price.

        :param price: Price to set.
        :raises TypeError: If price is not numeric.
        :raises ValueError: If price is not positive.
        """
        if not isinstance(price, (int, float)):
            raise TypeError("Parameter 'price' must be an instance of float")
        if price <= 0:
            raise ValueError("Parameter 'price' must be positive number")
        self.__price = round(float(price), PRECISION)

    @abstractmethod
    def accept(self, v: "Visitor") -> Any:
        """
        Accept a visitor.

        :param v: Visitor object.
        """
        pass

    def __str__(self) -> str:
        """
        String representation of the product.

        :return: Product description.
        """
        return f"'{self.name}' by '{self.producer}'"


class Book(Product):
    """
    Represents a book product.

    :param author: Author of the book.
    """

    author = SimpleTextField()

    def __init__(self, price: float, name: str, producer: str, author: str):
        super().__init__(price, name, producer)
        self.author = author

    def accept(self, v: "Visitor") -> Any:
        return v.visit_book(self)

    def __str__(self) -> str:
        return f"Book {super().__str__()}"


class PhoneStand(Product):
    """
    Represents a phone stand product.

    :param material: Material of the stand.
    """

    material = SimpleTextField()

    def __init__(self, price: float, name: str, producer: str, material: str):
        super().__init__(price, name, producer)
        self.material = material

    def accept(self, v: "Visitor") -> Any:
        return v.visit_phone_stand(self)

    def __str__(self) -> str:
        return f"Phone Stand {super().__str__()}"


class USBFlashDrive(Product):
    """
    Represents a USB flash drive.

    :param capacity_gb: Storage capacity in GB.
    """

    def __init__(self, price: float, name: str, producer: str, capacity_gb: int):
        super().__init__(price, name, producer)
        self.capacity_gb = capacity_gb

    @property
    def capacity_gb(self) -> int:
        """
        Get the capacity of the USB flash drive.

        :return: Capacity in GB.
        """
        return self.__capacity_gb

    @capacity_gb.setter
    def capacity_gb(self, capacity_gb: int):
        """
        Set and validate the capacity.

        :param capacity_gb: Capacity in GB.
        :raises TypeError: If capacity_gb not an integer.
        :raises ValueError: If capacity_gb not a positive number.
        """
        if not isinstance(capacity_gb, int):
            raise TypeError(
                "Parameter 'capacity_gb' must be an instance of int"
            )
        if capacity_gb <= 0:
            raise ValueError(
                "Parameter 'capacity_gb' must be positive number"
            )
        self.__capacity_gb = capacity_gb

    def accept(self, v: "Visitor") -> Any:
        return v.visit_usb_flash_drive(self)

    def __str__(self) -> str:
        return f"USB Flash Drive {super().__str__()}"


class Visitor(ABC):
    """
    Abstract visitor interface with visit methods
    for all product types.
    """

    @abstractmethod
    def visit_book(self, book: Book) -> Any:
        pass

    @abstractmethod
    def visit_phone_stand(self, stand: PhoneStand) -> Any:
        pass

    @abstractmethod
    def visit_usb_flash_drive(self, drive: USBFlashDrive) -> Any:
        pass


class DiscountVisitor(Visitor):
    """
    Visitor that applies discounts to various product types
    based on rules.
    """

    def visit_book(self, book: Book) -> float:
        """
        Apply discount rules to books.

        :param book: Book instance.
        :return: Discounted price.
        """
        discount = 10
        if book.producer.lower() == "pengein":
            discount += 5
        elif book.producer.lower() == "o'relly":
            discount += 10
        return round(book.price * ((100 - discount) / 100), PRECISION)

    def visit_phone_stand(self, stand: PhoneStand) -> float:
        """
        Apply discount rules to phone stands.

        :param stand: PhoneStand instance.
        :return: Discounted price.
        """
        discount = 5
        if stand.producer.lower() == "baseus":
            discount += 5
        elif stand.producer.lower() == "ugreen":
            discount += 3
        return round(stand.price * ((100 - discount) / 100), PRECISION)

    def visit_usb_flash_drive(self, drive: USBFlashDrive) -> float:
        """
        Apply discount rules to USB flash drives.

        :param drive: USBFlashDrive instance.
        :return: Discounted price.
        """
        discount = 0
        if (drive.price > 30 and
            drive.producer.lower() in ("sandisk", "kingston")):
            discount += 5
        return round(drive.price * ((100 - discount) / 100), PRECISION)


def main():
    """
    Main function to create products,
    apply DiscountVisitor, and print results.
    """

    book1 = Book(
        price=100.0,
        name="Clean Code",
        producer="Pengein",
        author="Robert Martin"
    )
    book2 = Book(
        price=120.0,
        name="Fluent Python",
        producer="O'Relly",
        author="Luciano Ramalho"
    )
    book3 = Book(
        price=80.0,
        name="Python Basics",
        producer="Manning",
        author="J. Doe"
    )

    stand1 = PhoneStand(
        price=25.0,
        name="Mini Stand",
        producer="Baseus",
        material="Plastic"
    )
    stand2 = PhoneStand(
        price=30.0,
        name="Desk Stand",
        producer="Ugreen",
        material="Aluminum"
    )

    drive1 = USBFlashDrive(
        price=40.0,
        name="Speedy 64GB",
        producer="SanDisk",
        capacity_gb=64
    )
    drive2 = USBFlashDrive(
        price=25.0,
        name="Tiny 32GB",
        producer="Kingston",
        capacity_gb=32
    )
    drive3 = USBFlashDrive(
        price=20.0,
        name="Flex16",
        producer="Transcend",
        capacity_gb=16
    )

    products = [book1, book2, book3, stand1, stand2, drive1, drive2, drive3]

    visitor = DiscountVisitor()

    print(f"{' Discounted Prices ':=^88}")
    print(f"| {'Name':^45} | {'Price, USD':^12} "
          f"| {'Discounted Price, USD':^21} |")
    for product in products:
        print(f"| {str(product):<45} | {product.price:>12.2f} "
              f"| {product.accept(visitor):>21.2f} |")


# Run main() only when script is executed directly
if __name__ == "__main__":
    main()
