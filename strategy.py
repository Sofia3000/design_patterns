from abc import ABC, abstractmethod
from typing import List, Optional
import os
import pprint


class SearchStrategy(ABC):
    """
    Abstract base class for search strategies used by FileSearcher.
    Defines the interface and helper method
    for accessing directory content.
    """

    def _get_folder_content(self, folder: str) -> Optional[List[str]]:
        """
        Safely retrieve the content of a given folder.

        :param folder: Absolute or relative path to the directory.
        :return: List of item names in the folder, or None if an error occurred.
        """
        try:
            return os.listdir(folder)
        except PermissionError:
            print(f"Error: Permission denied to access '{folder}'.")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return

    @abstractmethod
    def search(self, folder: str, query: str) -> List[str]:
        """
        Perform a search in the specified folder based on a query.

        :param folder: Folder to search in.
        :param query: Search term.
        :return: List of matching file names.
        """


class FileSearcher:
    """
    Context class for managing file search operations using different strategies.

    Uses the Strategy pattern to delegate the actual search logic.
    """

    def __init__(self, strategy: SearchStrategy):
        """
        Initialize the FileSearcher with a specific search strategy.

        :param strategy: Initial search strategy.
        """
        self.strategy = strategy

    @property
    def strategy(self) -> SearchStrategy:
        """
        Gets the current search strategy.
        """
        return self.__strategy

    @strategy.setter
    def strategy(self, strategy: SearchStrategy):
        """
        Sets the current search strategy.

        :param strategy: New SearchStrategy to use.
        :raises TypeError: If the strategy is not a SearchStrategy instance.
        """
        if not isinstance(strategy, SearchStrategy):
            raise TypeError(
                "Parameter 'strategy' must be an instance of SearchStrategy"
            )
        self.__strategy = strategy

    def search(self, folder: str, query: str) -> List[str]:
        """
        Perform a search using the current strategy.

        :param folder: Folder to search in.
        :param query: Search term.
        :return: List of matching file names.
        :raises TypeError, ValueError: For invalid input.
        """
        if not isinstance(folder, str):
            raise TypeError("Parameter 'folder' must be a string")
        if not folder.strip():
            raise ValueError("Parameter 'folder' must not be empty")
        if not os.path.isdir(folder):
            raise ValueError(f"Invalid folder path: {folder}")
        if not isinstance(query, str):
            raise TypeError("Parameter 'query' must be a string")
        if not query.strip():
            raise ValueError("Parameter 'query' must not be empty")
        return self.strategy.search(folder, query)


class NameSearchStrategy(SearchStrategy):
    """
    Concrete search strategy for finding files
    that contain a query in their name.
    """

    def search(self, folder: str, query: str) -> List[str]:
        """
        Search for files with names that contain the query substring.

        :param folder: Folder to search in.
        :param query: Substring to search for in filenames.
        :return: List of matching filenames.
        """
        query = query.lower()
        content = self._get_folder_content(folder)
        result = []
        if content:
            for item in content:
                name = item
                full_path = os.path.join(folder, item)
                if os.path.isfile(full_path):
                    name = os.path.splitext(item)[0].lower()
                if query in name:
                    result.append(item)

        return result


class ExtensionSearchStrategy(SearchStrategy):
    """
    Concrete search strategy for finding files
    by their extension.
    """

    def search(self, folder: str, query: str) -> List[str]:
        """
        Search for files with a specific extension.

        :param folder: Folder to search in.
        :param query: File extension to search for (without dot).
        :return: List of matching filenames.
        """
        query = query.lower()
        content = self._get_folder_content(folder)
        result = []
        if content:
            for item in content:
                full_path = os.path.join(folder, item)
                if not os.path.isfile(full_path):
                    continue
                ext = os.path.splitext(item)[1][1:].lower()
                if query == ext:
                    result.append(item)

        return result


class ContentSearchStrategy(SearchStrategy):
    """
    Concrete search strategy for finding files
    that contain a query in their content.
    """

    def search(self, folder: str, query: str) -> List[str]:
        """
        Search for files containing the query string in their content.

        :param folder: Folder to search in.
        :param query: Substring to search for inside files.
        :return: List of matching filenames.
        """
        query = query.lower()
        content = self._get_folder_content(folder)
        result = []
        if content:
            for item in content:
                full_path = os.path.join(folder, item)
                if not os.path.isfile(full_path):
                    continue
                try:
                    with open(full_path, 'r') as fhand:
                        for line in fhand:
                            if query in line.lower():
                                result.append(item)
                                break
                except:
                    continue

        return result


def main():
    """
    Demonstrate usage of FileSearcher with different search strategies.
    """
    directory = os.getcwd()
    name = "factory"
    extension = "py"
    text = "import os"

    searcher = FileSearcher(NameSearchStrategy())
    results = searcher.search(directory, name)
    if results:
        print(f"All items with '{name}' in name:")
        pprint.pp(results)
    else:
        print(f"There are no items with '{name}' in name")

    searcher.strategy = ExtensionSearchStrategy()
    results = searcher.search(directory, extension)
    if results:
        print(f"\nAll files with extension '.{extension}':")
        pprint.pp(results)
    else:
        print(f"\nThere are no files with extension '.{extension}'")

    searcher.strategy = ContentSearchStrategy()
    results = searcher.search(directory, text)
    if results:
        print(f"\nAll files that contain '{text}':")
        pprint.pp(results)
    else:
        print(f"\nNo files contain '{text}'")


# Run main() only when script is executed directly
if __name__ == "__main__":
    main()
