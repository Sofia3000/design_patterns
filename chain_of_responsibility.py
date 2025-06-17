from abc import ABC, abstractmethod
from typing import Optional
import os
import json
import pandas as pd
import xml.etree.ElementTree as ET


class Handler(ABC):
    """
    Interface for all handlers in the chain.
    """

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        """
        Handle the given request or pass it to the next handler.

        :param request: The request to handle.
        :return: Optional response string.
        """
        pass


class FileHandler(Handler):
    """
    Base class for file handlers implementing chain of responsibility.
    """

    def __init__(self):
        self._next_handler = None

    def set_next(self, handler: Handler):
        """
        Set the next handler in the chain.

        :param handler: The next handler.
        :raises TypeError: If the handler is not an instance of Handler.
        """
        if not isinstance(handler, Handler):
            raise TypeError("Parameter 'handler' must be an instance of Handler")
        self._next_handler = handler

    def _check_file_path(self, file_path: str):
        """
        Validate the file path.

        :param file_path: Path to the file.
        :raises TypeError: If file_path is not a string.
        :raises ValueError: If file_path is empty or whitespace.
        :raises FileNotFoundError: If the file does not exist or is not a file.
        """
        if not isinstance(file_path, str):
            raise TypeError("Parameter 'file_path' must be a string")
        if not file_path.strip():
            raise ValueError("Parameter 'file_path' could not be empty")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"File '{file_path}' was not found or it is not a file."
            )

    def handle(self, file_path: str) -> Optional[str]:
        """
        Pass the request to the next handler if available.

        :param file_path: Path to the file.
        :return: Response from next handler or None.
        """
        if self._next_handler:
            return self._next_handler.handle(file_path)
        return None


class JSONHandler(FileHandler):
    """
    Handler for JSON files.
    """

    def handle(self, file_path: str) -> Optional[str]:
        """
        Process JSON file if extension matches, else pass to next handler.

        :param file_path: Path to the JSON file.
        :return: Info string or None.
        """
        self._check_file_path(file_path)
        if file_path.lower().endswith(".json"):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if not data:
                        return f"File {file_path} is empty."
                    elif isinstance(data, dict):
                        return (
                            f"File {file_path} is a dictionary with keys: " +
                            ", ".join(data.keys()) + "."
                        )
                    elif isinstance(data, list):
                        return f"File {file_path} is a list with {len(data)} element(s)."
                    else:
                        return f"File {file_path} contains an instance of {type(data).__name__}."
            except PermissionError:
                print(f"[Error] No permission to read the file {file_path}.")
            except json.JSONDecodeError:
                print(f"[Error] JSON file {file_path} is not properly formatted.")
            except Exception as e:
                print(f"An error occurred while reading {file_path}: {e}")
        else:
            return super().handle(file_path)


class CSVHandler(FileHandler):
    """
    Handler for CSV files.
    """

    def handle(self, file_path: str) -> Optional[str]:
        """
        Process CSV file if extension matches, else pass to next handler.

        :param file_path: Path to the CSV file.
        :return: Info string or None.
        """
        self._check_file_path(file_path)
        if file_path.lower().endswith(".csv"):
            try:
                df = pd.read_csv(file_path, header=None)
                if df.empty:
                    return f"File {file_path} is empty."
                col_count = len(df.columns)
                row_count = len(df)            
                return (
                    f"File {file_path} contains {row_count} row(s)" +
                    f" and {col_count} column(s)."
                )
            except PermissionError:
                print(f"[Error] No permission to read the file {file_path}")
            except pd.errors.EmptyDataError:
                print(f"[Error] File {file_path} is empty or invalid.")
            except pd.errors.ParserError:
                print(f"[Error] file {file_path} is not properly formatted.")
            except Exception as e:
                print(f"An error occurred while reading {file_path}: {e}")
        else:
            return super().handle(file_path)


class XMLHandler(FileHandler):
    """
    Handler for XML files.
    """

    def handle(self, file_path: str) -> Optional[str]:
        """
        Process XML file if extension matches, else pass to next handler.

        :param file_path: Path to the XML file.
        :return: Info string or None.
        """
        self._check_file_path(file_path)
        if file_path.lower().endswith(".xml"):
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                return (
                    f"Root tag for {file_path}: '{root.tag}'. "
                    f"Number of direct child elements: {len(root)}."
                )
            except PermissionError:
                print(f"[Error] No permission to read the file {file_path}.")
            except ET.ParseError:
                print(f"[Error] Failed to parse XML file {file_path}.")
            except Exception as e:
                print(f"An error occurred while reading {file_path}: {e}")
        else:
            return super().handle(file_path)


def main():
    """
    Entry point demonstrating the Chain of Responsibility pattern with file handlers.
    """
    json_handler = JSONHandler()
    csv_handler = CSVHandler()
    xml_handler = XMLHandler()

    # Setup chain JSON -> CSV -> XML
    json_handler.set_next(csv_handler)
    csv_handler.set_next(xml_handler)

    file_path = input("Enter the path to your file: ").strip()
    if not file_path.strip():
        print("[Error] No file path provided.")
        return

    try:
        result = json_handler.handle(file_path)
        if result:
            print(result)
        else:
            print(f"No handler could process the file {file_path}.")
    except (TypeError, ValueError, FileNotFoundError) as e:
        print(f"{e}")


if __name__ == "__main__":
    main()
