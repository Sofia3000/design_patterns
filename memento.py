from abc import ABC
from typing import List
import copy


class Memento(ABC):
    """
    Abstract base class for saving state (Memento).
    """


class ContactBookMemento(Memento):
    """
    Concrete Memento class that stores the state of contacts list.
    """

    def __init__(self, contacts: List["Contact"]):
        """
        Initialize Memento with a list of contacts.

        :param contacts: List of contacts to save.
        :raises TypeError: If contacts is not a list of Contacts.
        """
        if not isinstance(contacts, list):
            raise TypeError("Parameter 'contacts' must be an instance of list")
        if not all(isinstance(c, Contact) for c in contacts):
            raise TypeError("Contacts must be a list of Contact")
        self._contacts = copy.deepcopy(contacts)

    def get_state(self) -> List["Contact"]:
        """
        Returns the saved state of contacts.
        """
        return self._contacts


class Contact:
    """
    Represents a simple contact with name and phone number.
    """
    _number_length: int = 10

    def __init__(self, name: str, number: str):
        """
        Initialize a contact with name and number.

        :param name: Contact's name.
        :param number: Contact's phone number.
        """
        self.name = name
        self.number = number

    @property
    def name(self) -> str:
        """
        Gets the contact's name.

        :return: Name as a string.
        """
        return self.__name

    @name.setter
    def name(self, value: str):
        """
        Sets the contact's name.

        :param value: Name for the contact.
        :raises TypeError: If value is not a string.
        :raises ValueError: If value is empty or whitespace only.
        """
        if not isinstance(value, str):
            raise TypeError("Parameter 'name' must be a string")
        if not value.strip():
            raise ValueError("Parameter 'name' could not be empty")
        self.__name = value

    @property
    def number(self) -> str:
        """
        Gets the contact's phone number.

        :return: Phone number as a string.
        """
        return self.__number

    @number.setter
    def number(self, value: str):
        """
        Sets the contact's phone number.

        :param value: Phone number.
        :raises TypeError: If value is not a string.
        :raises ValueError: If value is empty, wrong length, or contains non-digit characters.
        """
        if not isinstance(value, str):
            raise TypeError("Parameter 'number' must be a string")
        if not value.strip():
            raise ValueError("Parameter 'number' could not be empty")
        if len(value) != self._number_length or not value.isdigit():
            raise ValueError(f"Bad phone number: '{value}'")
        self.__number = value

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the contact.

        :return: Formatted contact string.
        """
        return f"Name: {self.name}. Phone number: {self.number}"


class ContactBook:
    """
    Collection of contacts that supports adding, removing,
    saving, and restoring state.
    """

    def __init__(self):
        """
        Initializes an empty contact book.
        """
        self._contacts: List[Contact] = []

    def add_contact(self, contact: Contact):
        """
        Adds a contact to the book.

        :param contact: Contact object to add.
        :raises TypeError: If contact is not a Contact instance.
        """
        if not isinstance(contact, Contact):
            raise TypeError("Parameter 'contact' must be an instance of Contact")
        self._contacts.append(contact)

    def remove_contact(self, index: int):
        """
        Removes a contact by index.

        :param index: Index of contact to remove.
        :raises TypeError: If index is not an integer.
        :raises IndexError: If index is out of range.
        """
        if not isinstance(index, int):
            raise TypeError("Index must be an integer number")
        if not (0 <= index < len(self._contacts)):
            raise IndexError("Index out of range")
        self._contacts.pop(index)

    def show_contacts(self):
        """
        Prints all contacts to the console.
        If empty, notifies that the book is empty.
        """
        if not self._contacts:
            print("Contact book is empty.")
            return

        print("All contacts:")
        for i, contact in enumerate(self._contacts):
            print(f"{i+1}. {contact}")

    def save(self) -> Memento:
        """
        Creates a Memento with the current state of contacts.

        :return: ContactBookMemento object.
        """
        return ContactBookMemento(self._contacts)

    def restore(self, memento: ContactBookMemento):
        """
        Restores contacts state from a Memento.

        :param memento: ContactBookMemento to restore from.
        :raises TypeError: If memento is not ContactBookMemento.
        """
        if not isinstance(memento, ContactBookMemento):
            raise TypeError(
                "Parameter 'memento' must be an instance of ContactBookMemento"
            )
        self._contacts = copy.deepcopy(memento.get_state())

    def __len__(self) -> int:
        """
        Returns the number of contacts in the book.

        :return: Integer count of contacts.
        """
        return len(self._contacts)


class History:
    """
    Maintains history of ContactBook changes and supports undo.
    """

    def __init__(self, book: ContactBook):
        """
        Initializes History with reference to a ContactBook.

        :param book: ContactBook instance.
        :raises TypeError: If book is not ContactBook.
        """
        if not isinstance(book, ContactBook):
            raise TypeError(
                "Parameter 'book' must be an instance of ContactBook"
            )
        self._book = book
        self._snapshots: List[Memento] = []

    def backup(self):
        """
        Saves the current state of ContactBook to the snapshots stack.
        """
        self._snapshots.append(self._book.save())

    def undo(self) -> bool:
        """
        Restores the last saved state of ContactBook.

        :return: True if undo succeeded, False if no snapshots available.
        """
        if self._snapshots:
            self._book.restore(self._snapshots.pop())
            return True
        return False


def main():
    """
    Entry point with interactive menu for Contact Book.

    Supported commands:
    - a: Add a new contact
    - d: Delete existing contact
    - s: Show all contacts
    - u: Undo last change
    - q: Quit the program
    """
    book = ContactBook()
    history = History(book)
    print("Welcome to Contact Book.")
    while True:
        input("Press Enter to continue. ")
        print("\n--- MENU ---")
        print(f"a - Add a new contact")
        print(f"d - Delete existing contact")
        print(f"s - Show all contacts")
        print(f"u - Undo last change")
        print("q - Quit")

        command = input("Choose an action: ").strip().lower()
        match (command):
            case 'a':
                name = input("Enter name: ").strip()
                number = input("Enter phone number: ").strip()
                if not name or not number:
                    print("Name and phone number could not be empty")
                    continue
                try:
                    contact = Contact(name, number)
                except ValueError as e:
                    print(e)
                    continue
                history.backup()
                book.add_contact(contact)
                print("Contact was added successfully")
            case 'd':
                index_txt = input(
                    "Enter the number of the contact to delete: "
                ).strip()
                try:
                    index = int(index_txt) - 1
                except:
                    print("Error: You must enter a valid number")
                    continue
                if not (0 <= index < len(book)):
                    print("Error: Invalid number")
                    continue
                history.backup()
                book.remove_contact(index)
                print("Contact was deleted successfully")
            case 's':
                book.show_contacts()
            case 'u':
                if history.undo():
                    print("Contact book rollback done")
                else:
                    print("No previous changes to undo")
            case 'q':
                print("Exiting the Contact Book")
                break
            case _:
                print(
                    "Invalid input. Please choose 'a', 'd', 's', 'u', or 'q'."
                )


# Run main() only when script is executed directly
if __name__ == "__main__":
    main()
