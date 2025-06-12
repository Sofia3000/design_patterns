from abc import ABC, abstractmethod
import string

class Logger(ABC):
    """Abstract base class defining the logger interface."""
    @abstractmethod
    def log(self, data: str) -> None:
        """
        Logs the provided string data.

        :param data: The message to be logged.
        """

class ConsoleLogger(Logger):
    def log(self, data: str) -> None:
        """Log message to the console (standard output)."""
        print(data, end='')

class FileLogger(Logger):
    def log(self, data: str) -> None:
        """Log message to a file named 'report.txt'. Overwrites file each time."""
        with open('report.txt', 'w') as fhand:
            fhand.write(data)

class TextAnalyzer(ABC):
    """
    Abstract base class for text analyzers that process input text by counting
    character frequencies (excluding whitespace) and logging the analysis results.

    Subclasses must implement create_logger() to provide a specific Logger
    for outputting the analysis report.
    """
    @abstractmethod
    def create_logger(self) -> Logger:
        """Return logger object"""

    def analyze_text(self, text: str) -> None:
        """
        Analyze the input text: validate it, count characters excluding whitespace,
        prepare a frequency report, and log the result using the Logger.

        :param text: The text to analyze.
        :raises TypeError: If text is not a string.
        :raises ValueError: If text is empty or contains only whitespace.
        """
        # Check type
        if not isinstance(text, str):
            raise TypeError('Text must be a string')
        
        # Check value
        if not text.strip():
            raise ValueError('Text can not be empty')
        
        # Convert text to lowercase
        text = text.lower()
        # Delete all whitespaces
        text = text.translate(str.maketrans('', '', string.whitespace))
        # Calculate char frequency
        symbols = dict()
        for c in text:
            symbols[c] = symbols.get(c, 0) + 1
        # Sort symbols by frequency
        char_frequency = list(symbols.items())
        char_frequency.sort(key=lambda item: item[1], reverse=True)
        
        # Log report
        print('Text was analyzed successfully')
        logger = self.create_logger()
        report = "Report\n"
        report += f"Text consists of {len(text)} non-space character(s)\n"
        report += "Char Frequency\n"
        for char, frequency in char_frequency:
            report += f"'{char}': {frequency}\n"
        logger.log(report)

class TerminalTextAnalyzer(TextAnalyzer):
    """
    Text analyzer that logs analysis reports to the terminal (standard output)
    using a ConsoleLogger.
    """
    def create_logger(self):
        return ConsoleLogger()
    
class PersistentTextAnalyzer (TextAnalyzer):
    """
    Text analyzer that logs analysis reports to a file ('report.txt')
    using a FileLogger. Each report overwrites the previous content.
    """
    def create_logger(self):
        return FileLogger()

def main():
    """
    Demonstrates usage of TerminalTextAnalyzer and PersistentTextAnalyzer.
    """
    terminal_analyzer = TerminalTextAnalyzer()
    persistent_analyzer = PersistentTextAnalyzer ()

    print("TerminalTextAnalyzer")
    terminal_analyzer.analyze_text("Hello, Console!")

    print("\nPersistentTextAnalyzer")
    persistent_analyzer.analyze_text("Hello, File!")

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()