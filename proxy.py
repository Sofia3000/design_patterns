from abc import ABC, abstractmethod

# Available user roles
ACCESS_LEVELS = (
    "employee",
    "manager",
    "security",
    "admin"
)

# Access rules for documents by confidentiality level
DOCUMENT_ACCESS_RULES = {
    "general":        {"employee", "manager", "security", "admin"},
    "internal-only":  {"manager", "security", "admin"},
    "sensitive":      {"security", "admin"},
    "classified":     {"admin"}
}


class User:
    """
    Represents a user in the system with a role and a name.
    """

    def __init__(self, name: str, role: str):
        """
        Initialize a user with name and role.

        :param name: User's name (non-empty string)
        :param role: User's role from ACCESS_LEVELS
        :raises TypeError: if types are invalid
        :raises ValueError: if values are invalid
        """
        self.name = name
        if not isinstance(role, str):
            raise TypeError("Parameter 'role' must be a string")
        if role not in ACCESS_LEVELS:
            raise ValueError(f"Invalid role: {role}")
        self.__role = role

    @property
    def name(self) -> str:
        """Return user's name"""
        return self.__name

    @name.setter
    def name(self, value: str):
        """Set and validate user's name"""
        if not isinstance(value, str):
            raise TypeError("Parameter 'name' must be a string")
        if not value.strip():
            raise ValueError("Parameter 'name' could be empty")
        self.__name = value

    @property
    def role(self) -> str:
        """Return user's role"""
        return self.__role
    
    def __str__(self) -> str:
        return f"{self.role} {self.name.capitalize()}"


class AbstractDocument(ABC):
    """
    Abstract interface for any readable document.
    """

    @abstractmethod
    def read(self) -> str:
        """
        Return the content of the document.
        """


class Document(AbstractDocument):
    """
    Real document that contains protected information.
    """

    def __init__(self, name: str, content: str, level: str):
        """
        Initialize document with title, content, and access level.

        :param name: Title of the document.
        :param content: Text of the document.
        :param level: Access level required to view.
        :raises TypeError: if arguments are not valid strings
        :raises ValueError: if level is not allowed
        """
        if not all(isinstance(p, str) for p in (name, content, level)):
            raise TypeError("Parameters 'name', 'content', and 'level' must be strings")
        if not all(p.strip() for p in (name, content, level)):
            raise ValueError("Parameters 'name', 'content', and 'level' could not be empty")
        if level not in DOCUMENT_ACCESS_RULES:
            raise ValueError(f"Invalid document access level: {level}")

        self.__name = name
        self.__content = content
        self.__level = level

    @property
    def level(self) -> str:
        """
        Return access level of the document.
        """
        return self.__level

    def read(self) -> str:
        """
        Return full document content.
        """
        return f"{self.__name}\n{self.__content}"


class DocumentProxy(AbstractDocument):
    """
    Proxy class that controls access to the document based on user role.
    """

    def __init__(self, document: AbstractDocument, role: str):
        """
        Initialize proxy with a real document and a user.

        :param document: Real document to be accessed.
        :param role: User requesting access.
        :raises TypeError: if document or role are of wrong types
        """
        if not isinstance(document, AbstractDocument):
            raise TypeError("Parameter 'document' must be AbstractDocument")
        if not isinstance(role, str):
            raise TypeError("Parameter 'role' must be a string")
        if role not in ACCESS_LEVELS:
            raise ValueError(f"Invalid role: {role}")
        self.__document = document
        self.__role = role

    def read(self) -> str:
        """
        Attempt to read document content. Performs access check.

        :return: Content if access is allowed
        :raises PermissionError: if access is denied
        """
        if not self.__check_access():
            raise PermissionError("Access denied.")

        return self.__document.read()

    def __check_access(self) -> bool:
        """
        Check whether the user's role is in the list of allowed roles.

        :return: True if access is granted, else False
        """
        return self.__role in DOCUMENT_ACCESS_RULES[self.__document.level]


def main():
    """
    Demonstrates the use of DocumentProxy with different users and documents.
    """
    documents = [
        Document("Internal Report", "This contains quarterly internal data", "internal-only"),
        Document("Classified Report", "Top secret strategies", "classified")
    ]

    users = [
        User("David", "manager"),
        User("Ann", "admin")
    ]

    print("=== Test Document Proxy ===")
    for user in users:
        for doc in documents:
            print(f"\n{user} tries to read {doc.level} document")
            try:
                print(
                    "Document content:\n" + 
                    DocumentProxy(doc, user.role).read()
                )
            except PermissionError as e:
                print(e)


if __name__ == "__main__":
    main()
