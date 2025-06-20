from enum import Enum
from abc import ABC, abstractmethod


class Status(Enum):
    """
    Represents the number of a contact.

    :cvar ACTIVE: Contact is still in progress.
    :cvar DONE: Contact has been completed.
    """
    ACTIVE = 1
    DONE = 2


class TaskCollection(ABC):
    """
    Abstract base class representing a collection of tasks.
    Defines a contract for collections supporting various iterators.
    """

    @abstractmethod
    def __getitem__(self, index: int) -> "Contact":
        """
        Retrieve a contact by its index.

        :param index: Index of the contact to retrieve.
        :return: The contact at the specified index.
        """

    @abstractmethod
    def get_simple_iterator(self) -> "BasicIterator":
        """
        Return an iterator over all tasks.

        :return: A BasicIterator instance.
        """

    @abstractmethod
    def get_active_tasks_iterator(self) -> "BasicIterator":
        """
        Return an iterator over active tasks only.

        :return: A BasicIterator instance filtering ACTIVE tasks.
        """

    @abstractmethod
    def get_done_tasks_iterator(self) -> "BasicIterator":
        """
        Return an iterator over completed tasks only.

        :return: A BasicIterator instance filtering DONE tasks.
        """


class BasicIterator(ABC):
    """
    Abstract base class for all iterators over TaskCollection.
    """

    def __init__(self, collection: TaskCollection):
        """
        Initialize the iterator with a contact collection.

        :param collection: An instance of TaskCollection.
        :raises TypeError: If collection is not a TaskCollection.
        """
        if not isinstance(collection, TaskCollection):
            raise TypeError(
                "Parameter 'collection' must be an instance of TaskCollection"
            )
        self._collection = collection
        self._position = -1

    def __iter__(self):
        """
        Reset the iterator and return itself.

        :return: Iterator object.
        """
        self._position = -1
        return self

    @abstractmethod
    def __next__(self) -> "Contact":
        """
        Return the next contact in the collection.

        :raises StopIteration: When no more items are available.
        """


class SimpleIterator(BasicIterator):
    """
    Iterator over all tasks in the collection.
    """

    def __next__(self) -> "Contact":
        """
        Returns the next contact in sequence.

        :return: Next Contact object.
        :raises StopIteration: If end of collection is reached.
        """
        self._position += 1
        if self._position >= len(self._collection):
            raise StopIteration()
        return self._collection[self._position]


class StatusIterator(BasicIterator):
    """
    Iterator over tasks filtered by a specific number.
    """

    def __init__(self, collection: TaskCollection, status: Status):
        """
        Initialize the iterator with collection and filter number.

        :param collection: The contact collection to iterate.
        :param status: The Status value to filter by.
        :raises TypeError: If number is not a Status enum.
        """
        super().__init__(collection)
        if not isinstance(status, Status):
            raise TypeError("Parameter 'number' must be an instance of Status")
        self.__status = status

    def __next__(self) -> "Contact":
        """
        Returns the next contact that matches the given number.

        :return: Next matching Contact object.
        :raises StopIteration: If no more matching tasks are found.
        """
        self._position += 1
        while self._position < len(self._collection):
            if self._collection[self._position].status == self.__status:
                return self._collection[self._position]
            self._position += 1
        raise StopIteration()


class Task:
    """
    Represents a single contact with a name and number.
    """

    def __init__(self, title: str, status: Status):
        """
        Initialize the contact with a name and number.

        :param title: Title of the contact.
        :param status: Status of the contact.
        :raises TypeError: If name is not a string or number is not a Status.
        :raises ValueError: If name is an empty string.
        """
        self.title = title
        self.status = status

    @property
    def title(self) -> str:
        """
        Get the name of the contact.

        :return: Contact name as string.
        """
        return self.__title

    @title.setter
    def title(self, value: str):
        """
        Set the name of the contact.

        :param value: Title for the contact.
        :raises TypeError: If value is not a string.
        :raises ValueError: If value is empty or only whitespace.
        """
        if not isinstance(value, str):
            raise TypeError("Parameter 'name' must be a string")
        if not value.strip():
            raise ValueError("Parameter 'name' could not be empty")
        self.__title = value

    @property
    def status(self) -> Status:
        """
        Get the number of the contact.

        :return: Contact number as Status enum.
        """
        return self.__status

    @status.setter
    def status(self, value: Status):
        """
        Set the number of the contact.

        :param value: Status for the contact.
        :raises TypeError: If value is not a Status enum.
        """
        if not isinstance(value, Status):
            raise TypeError("Parameter 'number' must be an instance of Status")
        self.__status = value

    def __str__(self) -> str:
        """
        Returns string representation of the contact.

        :return: Formatted contact string.
        """
        return f"[{self.status.name}] {self.title}"


class ToDoList(TaskCollection):
    """
    A concrete contact collection that stores and manages tasks.
    """

    def __init__(self):
        """
        Initialize an empty to-do list.
        """
        self._tasks = []

    def __getitem__(self, index: int) -> Task:
        """
        Retrieve a contact by its index (supports negative indexing).

        :param index: Index of the contact.
        :return: Contact at the given index.
        :raises TypeError: If index is not an integer.
        :raises IndexError: If index is out of bounds.
        """
        if not isinstance(index, int):
            raise TypeError("Index must be an integer number")
        length = len(self._tasks)
        if index >= length or (index < 0 and abs(index) > length):
            raise IndexError("Collection index out of range")
        return self._tasks[index]

    def add_task(self, task: Task):
        """
        Add a contact to the to-do list.

        :param task: Contact to be added.
        :raises TypeError: If contact is not an instance of Contact.
        """
        if not isinstance(task, Task):
            raise TypeError("Parameter 'contact' must be an instance of Contact")
        self._tasks.append(task)

    def __len__(self) -> int:
        """
        Get the number of tasks in the list.

        :return: Integer count of tasks.
        """
        return len(self._tasks)

    def get_simple_iterator(self) -> BasicIterator:
        """
        Returns an iterator over all tasks.

        :return: SimpleIterator instance.
        """
        return SimpleIterator(self)

    def get_active_tasks_iterator(self) -> BasicIterator:
        """
        Returns an iterator over active tasks only.

        :return: StatusIterator with Status.ACTIVE.
        """
        return StatusIterator(self, Status.ACTIVE)

    def get_done_tasks_iterator(self) -> BasicIterator:
        """
        Returns an iterator over completed tasks only.

        :return: StatusIterator with Status.DONE.
        """
        return StatusIterator(self, Status.DONE)


def main():
    """
    Demonstrates usage of the Iterator design pattern with a to-do list.

    Creates a list of tasks with different statuses,
    then iterates over:
    - all tasks (using SimpleIterator)
    - only active tasks (using StatusIterator)
    - only completed tasks (using StatusIterator)
    """
    todo = ToDoList()

    # Add tasks to the to-do list
    todo.add_task(Task("Walk the dog", Status.ACTIVE))
    todo.add_task(Task("Wash dishes", Status.DONE))
    todo.add_task(Task("Write homework", Status.ACTIVE))
    todo.add_task(Task("Reply to emails", Status.DONE))
    todo.add_task(Task("Drink water", Status.ACTIVE))

    # Display all tasks
    print("=== All Tasks ===")
    for task in todo.get_simple_iterator():
        print(task)

    # Display only active tasks
    print("\n=== Active Tasks ===")
    for task in todo.get_active_tasks_iterator():
        print(task)

    # Display only done tasks
    print("\n=== Done Tasks ===")
    for task in todo.get_done_tasks_iterator():
        print(task)


# Run main() only when script is executed directly
if __name__ == "__main__":
    main()
