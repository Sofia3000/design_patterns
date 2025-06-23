from abc import ABC, abstractmethod
from typing import List, Any, Optional
from io import TextIOWrapper


class TableWriter(ABC):
    """
    Abstract base class for writing tables to files.

    Defines a template method `write_table` for writing a table,
    including validating input and writing header, content, and footer.
    """

    def __init__(self):
        self.__fhand = None
        self.__data = None

    @property
    def fhand(self) -> Optional[TextIOWrapper]:
        """
        Returns the current file handle being written to.
        """
        return self.__fhand

    @property
    def data(self) -> Optional[List[List[Any]]]:
        """
        Returns the current data to write as a list of lists.
        """
        return self.__data

    def write_table(self, filename: str, data: List[List[Any]]):
        """
        Template method that writes a table to the specified file.

        Validates the filename and data, opens the file, and calls
        methods to write header, content, and footer.

        :param filename: The target file name.
        :param data: Table data as a list of lists.
        """
        self._validate_filename(filename)
        self._validate_data(data)
        try:
            with open(filename, 'w') as fhand:
                self.__fhand = fhand
                self.__data = data
                self._write_header()
                self._write_content()
                self._write_footer()
        except OSError as e:
            print(f"OSError: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            self.__fhand = None
            self.__data = None

    def _validate_filename(self, filename: str):
        """
        Validates the filename parameter, including type, emptiness,
        and correct file extension.

        :param filename: File name to validate.
        :raises TypeError, ValueError: If validation fails.
        """
        if not isinstance(filename, str):
            raise TypeError("Parameter 'filename' must be a string")
        if not filename.strip():
            raise ValueError("Parameter 'filename' must not be empty")
        if not filename.lower().endswith(self.expected_extension):
            raise ValueError(
                "Invalid file extension. Only files with "
                f"'{self.expected_extension}' extension are supported."
            )

    @property
    @abstractmethod
    def expected_extension(self) -> str:
        """
        Returns the expected file extension
        for the writer, e.g. '.html'.

        Must be implemented by subclasses.
        """


    def _validate_data(self, data: List[List[Any]]):
        """
        Validates the data parameter, checking type, emptiness,
        uniform row length, and that the first row contains strings.

        :param data: Table data to validate.
        :raises TypeError, ValueError: If validation fails.
        """
        if not isinstance(data, list):
            raise TypeError("Parameter 'data' must be an instance of list")
        if not data:
            raise ValueError("Parameter 'data' must not be empty")

        length_set = set()
        for item in data:
            if not isinstance(item, list):
                raise TypeError("Parameter 'data' must be list of lists")
            if not item:
                raise ValueError("Lists in data must not be empty")
            length_set.add(len(item))

        if len(length_set) != 1:
            raise ValueError("All lists in 'data' must have equal lengths")

        for el in data[0]:
            if not isinstance(el, str):
                raise TypeError(
                    "All elements in first sublist in 'data' must be strings"
                )

    def _write_header(self):
        """
        Writes the header of the table.

        Can be overridden by subclasses.
        """

    @abstractmethod
    def _write_content(self):
        """
        Writes the main content of the table.

        Must be implemented by subclasses.
        """

    def _write_footer(self):
        """
        Writes the footer of the table.

        Can be overridden by subclasses.
        """


class HTMLTableWriter(TableWriter):
    """
    Concrete TableWriter that writes HTML tables.
    """

    @property
    def expected_extension(self) -> str:
        """
        Returns the file extension '.html'.
        """
        return ".html"

    def _write_header(self):
        """
        Writes the opening HTML tags and the start of the table.
        """
        self.fhand.write("<html>\n<title>Table</title>\n<body>\n<table>\n")

    def _write_content(self):
        """
        Writes the table content with headers in <th> and rows in <td>.
        """
        self.fhand.write("<thead>\n<tr>\n")
        for col in self.data[0]:
            self.fhand.write(f"<th>{col}</th>\n")
        self.fhand.write("</tr>\n</thead>\n")
        self.fhand.write("<tbody>\n")
        for row in self.data[1:]:
            self.fhand.write("<tr>\n")
            for col in row:
                self.fhand.write(f"<td>{col}</td>\n")
            self.fhand.write("</tr>\n")
        self.fhand.write("</tbody>\n")

    def _write_footer(self):
        """
        Writes the closing table and HTML tags.
        """
        self.fhand.write("</table></body></html>")


class XMLTableWriter(TableWriter):
    """
    Concrete TableWriter that writes XML tables.
    """

    @property
    def expected_extension(self) -> str:
        """
        Returns the file extension '.xml'.
        """
        return ".xml"

    def _write_header(self):
        """
        Writes the XML declaration and opening <table> tag.
        """
        self.fhand.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<table>\n")

    def _write_content(self):
        """
        Writes each row as an XML <row> element with child elements for columns.
        """
        col_count = len(self.data[0])
        for row in self.data[1:]:
            self.fhand.write("<row>\n")
            for i in range(col_count):
                self.fhand.write(
                    f"<{self.data[0][i]}>{row[i]}</{self.data[0][i]}>\n"
                )
            self.fhand.write("</row>\n")

    def _write_footer(self):
        """
        Writes the closing </table> tag.
        """
        self.fhand.write("</table>")


class CSVTableWriter(TableWriter):
    """
    Concrete TableWriter that writes CSV tables.
    """

    @property
    def expected_extension(self) -> str:
        """
        Returns the file extension '.csv'.
        """
        return ".csv"

    def _write_content(self):
        """
        Writes each row as a comma-separated line.
        """
        for row in self.data:
            self.fhand.write(f"{','.join(map(str, row))}\n")


def main():
    """
    Example usage of the TableWriter classes.
    Writes sample data to HTML, XML, and CSV files.
    """
    data = [
        ["Name", "Age", "City"],
        ["Alice", 30, "London"],
        ["Bob", 25, "Berlin"],
        ["Charlie", 35, "Paris"]
    ]

    html_writer = HTMLTableWriter()
    xml_writer = XMLTableWriter()
    csv_writer = CSVTableWriter()

    print("Writing data to the files...")

    html_writer.write_table("table.html", data)
    xml_writer.write_table("table.xml", data)
    csv_writer.write_table("table.csv", data)

    print("Data was successfully written.")


# Run main() only when script is executed directly
if __name__ == "__main__":
    main()
