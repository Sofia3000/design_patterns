from abc import ABC, abstractmethod
from typing import Any, Optional
import requests
import time
from bs4 import BeautifulSoup
import pprint


class Component:
    """
    Base class for components interacting through a mediator.

    Contains the mediator property to hold a reference to the mediator instance.
    """

    def __init__(self):
        self.__mediator = None

    @property
    def mediator(self) -> Optional["Mediator"]:
        """
        Gets the current mediator of the component.

        :return: The mediator instance.
        :rtype: Mediator | None
        """
        return self.__mediator

    @mediator.setter
    def mediator(self, value: "Mediator") -> None:
        """
        Sets the mediator for the component.

        :param value: An instance of a Mediator.
        :raises TypeError: If value is not an instance of Mediator.
        """
        if not isinstance(value, Mediator):
            raise TypeError(
                "Attribute 'mediator' must be an instance of Mediator"
            )
        self.__mediator = value


class Mediator(ABC):
    """
    Abstract Mediator class.

    Defines the interface for communication between components.
    """

    @abstractmethod
    def notify(self, component: Component, data: Any):
        """
        Receives notifications from components.

        :param component: The component sending the notification.
        :param data: Data sent in the notification.
        """


class HTMLFetcher(Component):
    """
    Component responsible for loading HTML content from a URL.
    """

    def load(self, url: str) -> None:
        """
        Loads the HTML content from the specified URL and notifies the mediator.

        :param url: The URL of the page to load.
        :raises TypeError: If url is not a string.
        :raises ValueError: If url is an empty string.
        """
        if not isinstance(url, str):
            raise TypeError("Parameter 'url' must be a string")
        url = url.strip()
        if not url:
            raise ValueError("Parameter 'url' could not be empty")
        print(f"Connecting to '{url}'...")
        try:
            content = requests.get(url).content
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        time.sleep(1.5)
        print(f"Successfully connected to '{url}'")
        time.sleep(1.5)
        if self.mediator:
            self.mediator.notify(self, content)


class HTMLParser(Component):
    """
    Component responsible for parsing HTML content.
    """

    def parse(self, content: bytes | str):
        """
        Parses the HTML content to extract the page title and links,
        then notifies the mediator with the parsed data.

        :param content: HTML content as bytes or string.
        :raises TypeError: If content is not bytes or string.
        :raises ValueError: If content is empty.
        """
        if not isinstance(content, (bytes, str)):
            raise TypeError(
                "Parameter 'content' must be an instance of bytes or str"
            )
        if not content:
            raise ValueError("Parameter 'content' could not be empty")
        print(f"Parsing data...")
        data = {}
        soup = BeautifulSoup(content, "html.parser")
        title = soup.find("title")
        data["title"] = title.text if title else "Without title"
        data["links"] = []
        for link in soup.find_all("a"):
            href = link.get("href", "")
            if href and href.startswith("http"):
                data["links"].append(href)
        time.sleep(1.5)
        print("Data was successfully parsed")
        time.sleep(1.5)
        if self.mediator:
            self.mediator.notify(self, data)


class WebMediator(Mediator):
    """
    Mediator coordinating interaction between HTMLFetcher and HTMLParser.
    """

    def __init__(self, fetcher: HTMLFetcher, parser: HTMLParser):
        """
        Initializes the mediator with fetcher and parser components.

        :param fetcher: An instance of HTMLFetcher.
        :param parser: An instance of HTMLParser.
        :raises TypeError: If arguments are not of expected types.
        """
        if not isinstance(fetcher, HTMLFetcher):
            raise TypeError(
                "Parameter 'fetcher' must be an instance of HTMLFetcher"
            )
        if not isinstance(parser, HTMLParser):
            raise TypeError(
                "Parameter 'parser' must be an instance of HTMLParser"
            )
        self.__fetcher = fetcher
        self.__parser = parser
        fetcher.mediator = self
        parser.mediator = self

    def notify(self, component: Component, data: Any):
        """
        Handles notifications from components and coordinates next actions.

        :param component: The component sending the notification.
        :param data: Data received from the component.
        """
        match component:
            case self.__fetcher:
                print("Mediator delivers the fetcher's output to the parser")
                time.sleep(1.5)
                self.__parser.parse(data)
            case self.__parser:
                print("Mediator got data from parser")
                time.sleep(1.5)
                if not data:
                    print("Parser returned empty result")
                else:
                    print("Result of parsing:")
                    pprint.pp(data)
            case _:
                print("Notify was called by unknown component")

    def __str__(self):
        """
        Returns a string representation of the mediator.
        """
        return (f"Mediator between {self.__fetcher.__class__.__name__} and " +
                f"{self.__parser.__class__.__name__}")


def main():
    """
    Entry point of the program.

    Initializes components and mediator,
    accepts a URL from the user, and starts the load and parse process.
    """
    fetcher = HTMLFetcher()
    parser = HTMLParser()
    mediator = WebMediator(fetcher, parser)
    print(f"{mediator} was successfully created")
    # Get URL from user input
    url = input("Enter url for parsing: ").strip()
    # Use default if empty
    if not url:
        url = "https://python.org"
    fetcher.load(url)


# Run main() only when script is executed directly
if __name__ == "__main__":
    main()
