from enum import Enum
from abc import ABC, abstractmethod


class Status(Enum):
    """
    Represents the status of a task.

    :cvar ACTIVE: Task is still in progress.
    :cvar DONE: Task has been completed.
    """
    ACTIVE = 1
    DONE = 2


class TaskCollection(ABC):
    """
    Abstract base class representing a collection of tasks.
    Defines a contract for collections supporting various iterators.
    """

    @abstractmethod
    def __getitem__(self, index: int) -> "Task":
        """
        Retrieve a task by its index.

        :param index: Index of the task to retrieve.
        :return: The task at the specified index.
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
        Initialize the iterator with a task collection.

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
    def __next__(self) -> "Task":
        """
        Return the next task in the collection.

        :raises StopIteration: When no more items are available.
        """


class SimpleIterator(BasicIterator):
    """
    Iterator over all tasks in the collection.
    """

    def __next__(self) -> "Task":
        """
        Returns the next task in sequence.

        :return: Next Task object.
        :raises StopIteration: If end of collection is reached.
        """
        self._position += 1
        if self._position >= len(self._collection):
            raise StopIteration()
        return self._collection[self._position]


class StatusIterator(BasicIterator):
    """
    Iterator over tasks filtered by a specific status.
    """

    def __init__(self, collection: TaskCollection, status: Status):
        """
        Initialize the iterator with collection and filter status.

        :param collection: The task collection to iterate.
        :param status: The Status value to filter by.
        :raises TypeError: If status is not a Status enum.
        """
        super().__init__(collection)
        if not isinstance(status, Status):
            raise TypeError("Parameter 'status' must be an instance of Status")
        self.__status = status

    def __next__(self) -> "Task":
        """
        Returns the next task that matches the given status.

        :return: Next matching Task object.
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
    Represents a single task with a title and status.
    """

    def __init__(self, title: str, status: Status):
        """
        Initialize the task with a title and status.

        :param title: Title of the task.
        :param status: Status of the task.
        :raises TypeError: If title is not a string or status is not a Status.
        :raises ValueError: If title is an empty string.
        """
        self.title = title
        self.status = status

    @property
    def title(self) -> str:
        """
        Get the title of the task.

        :return: Task title as string.
        """
        return self.__title

    @title.setter
    def title(self, value: str):
        """
        Set the title of the task.

        :param value: Title for the task.
        :raises TypeError: If value is not a string.
        :raises ValueError: If value is empty or only whitespace.
        """
        if not isinstance(value, str):
            raise TypeError("Parameter 'title' must be a string")
        if not value.strip():
            raise ValueError("Parameter 'title' could not be empty")
        self.__title = value

    @property
    def status(self) -> Status:
        """
        Get the status of the task.

        :return: Task status as Status enum.
        """
        return self.__status

    @status.setter
    def status(self, value: Status):
        """
        Set the status of the task.

        :param value: Status for the task.
        :raises TypeError: If value is not a Status enum.
        """
        if not isinstance(value, Status):
            raise TypeError("Parameter 'status' must be an instance of Status")
        self.__status = value

    def __str__(self) -> str:
        """
        Returns string representation of the task.

        :return: Formatted task string.
        """
        return f"[{self.status.name}] {self.title}"


class ToDoList(TaskCollection):
    """
    A concrete task collection that stores and manages tasks.
    """

    def __init__(self):
        """
        Initialize an empty to-do list.
        """
        self._tasks = []

    def __getitem__(self, index: int) -> Task:
        """
        Retrieve a task by its index (supports negative indexing).

        :param index: Index of the task.
        :return: Task at the given index.
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
        Add a task to the to-do list.

        :param task: Task to be added.
        :raises TypeError: If task is not an instance of Task.
        """
        if not isinstance(task, Task):
            raise TypeError("Parameter 'task' must be an instance of Task")
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
