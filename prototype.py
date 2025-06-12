from abc import ABC, abstractmethod
import copy

class Prototype(ABC):
    """
    Abstract base class that defines the Prototype interface.
    """

    @abstractmethod
    def clone(self):
        """
        Creates a deep copy of the object.

        :return: A deep copy of the object.
        :rtype: Prototype
        """


class SimpleTextField:
    """
    Descriptor class for validating non-empty string fields.
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
            raise ValueError(f"'{self.name}' can not be empty.")
        setattr(instance, self.attr_name, value)


class Document(Prototype):
    """
    Concrete implementation of the Prototype that represents a document.

    Attributes:
        title (str): Title of the document.
        content (str): Body text of the document.
        author (str): Author of the document.
    """
    title = SimpleTextField()
    content = SimpleTextField()
    author = SimpleTextField()

    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author

    def clone(self) -> "Document":
        return copy.deepcopy(self)
    
    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nContent: {self.content}"

# Test Document   
def main():
    """
    Demonstrates the Prototype pattern by cloning a document object.
    """
    # Create document template
    template = Document("Report Template", "Content goes here...", "Admin")

    # Create copy with new author
    user_doc1 = template.clone()
    user_doc1.author = "Alice"

    # Create copy with new title and content
    user_doc2 = template.clone()
    user_doc2.title = "Final Report"
    user_doc2.content = "New content"

    # Output all documents
    print("Original template:")
    print(template)

    print("\nCloned Document 1:")
    print(user_doc1)

    print("\nCloned Document 2:")
    print(user_doc2)

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()