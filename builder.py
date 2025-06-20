from abc import ABC, abstractmethod
from functools import wraps
from typing import Optional, Any

class Report:
    """
    Represents a structured report consisting of a name, content, and footer.
    Stores parts of a report identified by keys and allows combining them
    into a complete textual representation. Only predefined part names
    ('name', 'content', 'footer') are allowed.
    """
    # Allowed part names
    _part_names = ('name', 'content', 'footer')
    
    def __init__(self) -> None:
        self._parts = {}

    def add(self, key: str, value: str) -> None:
        """
        Adds a report part with the specified key and content.

        :param key: The name of the part (must be 'name', 'content', or 'footer').
        :param value: The textual content for the specified part.
        :raises TypeError: If key or value is not a string.
        :raises ValueError: If key is not one of the allowed part names.
        """
        # Check types
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError('Key and Value must be strings')
        
        # Check key value
        key = key.strip().lower()
        if key not in self._part_names:
            raise ValueError(f'Wrong part name "{key}"')
        
        self._parts[key] = value

    def __str__(self) -> str:
        """
        Return the full report as a string by combining all parts in order.
        Only non-empty parts are included.
        """
        return '\n'.join(self._parts.get(key, '') for key in self._part_names if self._parts.get(key, ''))


def validate_text(func):
    """
    Decorator that trims and validates non-empty text before passing it to the decorated method.
    """
    @wraps(func)
    def wrapper(self, text: str) -> Optional[Any]:
        # Delete whitespaces
        text = text.strip()
        # Call func if text is not empty
        if text:
            return func(self, text)
    return wrapper

class ReportBuilder(ABC):
    """Abstract builder interface for constructing report parts."""
    
    @abstractmethod
    def add_title(self, text: str) -> None:
        """
        Adds a name to the report.

        :param text: The name text.
        """
    
    @abstractmethod
    def add_content(self, text: str) -> None:
        """
        Adds content to the report.

        :param text: The content text.
        """

    @abstractmethod
    def add_footer(self, text: str) -> None:
        """
        Adds footer to the report.

        :param text: The footer text.
        """

    @abstractmethod
    def get_result(self) -> Report:
        """
        Returns the final built report.

        :return: The constructed report.
        """


class PlainTextReportBuilder(ReportBuilder):
    """Builder for constructing report with plain text."""
    def __init__(self):
        self._report = Report()

    @validate_text
    def add_title(self, text: str) -> None:
        self._report.add('name', text)
    
    @validate_text
    def add_content(self, text: str) -> None:
        self._report.add('content', text)

    @validate_text
    def add_footer(self, text: str) -> None:
        self._report.add('footer', text)

    def get_result(self) -> Report:
        """
        Returns the constructed plain-text report and resets internal state.

        :return: The constructed report.
        """
        report = self._report
        # Reset builder state to allow reuse
        self._report = Report()
        return report


class MarkdownReportBuilder(ReportBuilder):
    """Builder for constructing report with markdown text."""
    def __init__(self):
        self._report = Report()

    @validate_text
    def add_title(self, text: str) -> None:
        self._report.add('name', '# '+text)

    @validate_text
    def add_content(self, text: str) -> None:
        self._report.add('content', text + '\n')

    @validate_text
    def add_footer(self, text: str) -> None:
        self._report.add('footer', '---\n' + text)

    def get_result(self) -> Report:
        """
        Returns the constructed markdown-formatted report and resets internal state.

        :return: The constructed report.
        """
        report = self._report
        # Reset builder state to allow reuse
        self._report = Report()
        return report

class Director:
    """Constructs a report by delegating part addition to the builder."""
    def __init__(self, builder: ReportBuilder):
        # Check builder's type
        if not isinstance(builder, ReportBuilder):
            raise TypeError('Builder must be instance of ReportBuilder')   
        self._builder = builder
    
    def construct_report(self, title: str, content: str, footer: str) -> None:
        """
        Constructs a full report by sequentially adding its parts.

        :param title: Title text.
        :param content: Content text.
        :param footer: Footer text.
        """
        self._builder.add_title(title)
        self._builder.add_content(content)
        self._builder.add_footer(footer)


def main():
    """
    Demonstrates the use of the builder pattern with plain and markdown builders.
    """
    # Test with PlainTextReportBuilder
    print("Testing PlainTextReportBuilder:")
    plain_builder = PlainTextReportBuilder()
    director = Director(plain_builder)

    # Construct the report using the director
    director.construct_report(
        title="Monthly Sales",
        content="Sales increased by 20%.",
        footer="Report generated on 2025-06-04"
    )
    # Get the built report and print it
    simple_report = plain_builder.get_result()
    print(simple_report)
    print("-" * 40)

    # Test with MarkDownReportBuilder
    print("Testing MarkDownReportBuilder:")
    markdown_builder = MarkdownReportBuilder()
    director = Director(markdown_builder)

    # Construct the report using the director
    director.construct_report(
        title="Monthly Sales",
        content="Sales increased by 20%.",
        footer="Report generated on 2025-06-04"
    )
    # Get the built report and print it
    markdown_report = markdown_builder.get_result()
    print(markdown_report)

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()