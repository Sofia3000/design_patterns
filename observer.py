import datetime as dt
import time


class News:
    """
    Represents a news item containing
    a title, content, and author information.
    """

    def __init__(self, title: str, content: str, author: str):
        """
        Initialize a news item with title, content, and author.

        :param title: Title of the news.
        :param content: Content/body of the news.
        :param author: Name of the author who wrote the news.
        :raises TypeError: If any of the parameters are not strings.
        :raises ValueError: If any of the parameters are empty strings.
        """
        if not all(isinstance(p, str) for p in (title, content, author)):
            raise TypeError(
                "Parameters 'title', 'content' and 'author' must be strings"
            )
        if not all(p.strip() for p in (title, content, author)):
            raise ValueError(
                "Parameters 'title', 'content' and 'author' must not be empty"
            )

        self.__title = title
        self.__content = content
        self.__author = author

    @property
    def title(self) -> str:
        """
        Get the title of the news.

        :return: The title as a string.
        """
        return self.__title

    @property
    def content(self) -> str:
        """
        Get the content of the news.

        :return: The content as a string.
        """
        return self.__content

    @property
    def author(self) -> str:
        """
        Get the author of the news.

        :return: The author's name as a string.
        """
        return self.__author

    def __str__(self):
        """
        Return a formatted string representation of the news.

        :return: Formatted string with title, content, and author.
        """
        return (f"{self.__title.upper()}\n{self.__content}\n"
                f"Written by {self.__author}")


class Observer:
    """
    Base class for observers that react to published news.
    """

    def update(self, news: News):
        """
        Receive an update with a News object.

        :param news: News instance with the latest data.
        :raises TypeError: If the input is not a News instance.
        """
        if not isinstance(news, News):
            raise TypeError(
                "Parameter 'news' must be an instance of News"
            )
        print(f"\n{self.__class__.__name__} got news.")


class NewsPublisher:
    """
    Publisher class that manages news broadcasting
    to all subscribed observers.
    """

    def __init__(self):
        """
        Initialize the news publisher with
        an empty list of subscribers.
        """
        self._subscribers = []

    def subscribe(self, observer: Observer):
        """
        Add an observer to the subscriber list.

        :param observer: An instance of Observer.
        :raises TypeError: If the object is not an Observer.
        """
        if not isinstance(observer, Observer):
            raise TypeError(
                "Parameter 'observer' must be an instance of Observer"
            )
        if observer not in self._subscribers:
            self._subscribers.append(observer)

    def unsubscribe(self, observer: Observer):
        """
        Remove an observer from the subscriber list.

        :param observer: An instance of Observer.
        :raises TypeError: If the object is not an Observer.
        """
        if not isinstance(observer, Observer):
            raise TypeError(
                "Parameter 'observer' must be an instance of Observer"
            )
        if observer in self._subscribers:
            self._subscribers.remove(observer)

    def notify(self, news: News):
        """
        Notify all subscribed observers with a new news item.

        :param news: The News instance to send.
        :raises TypeError: If the input is not a News instance.
        """
        if not isinstance(news, News):
            raise TypeError(
                "Parameter 'news' must be an instance of News"
            )

        for subscriber in self._subscribers:
            subscriber.update(news)
            time.sleep(1.5)

    def publish_news(self, news: News):
        """
        Publish a new news item and notify all observers.

        :param news: The News instance to publish.
        :raises TypeError: If the input is not a News instance.
        """
        if not isinstance(news, News):
            raise TypeError(
                "Parameter 'news' must be an instance of News"
            )
        print(f"\nPublisher add news:\n{news}")
        time.sleep(1.5)
        self.notify(news)


class NewsLogger(Observer):
    """
    Observer that logs received news to a uniquely named text file.
    """

    def __init__(self):
        """
        Initialize the logger and create
        a unique filename based on the current timestamp.
        """
        timestamp = str(dt.datetime.now().timestamp()).replace('.', '')
        self.__filename = f"news{timestamp}.txt"

    def update(self, news: News):
        """
        Handle the news update by writing it to a file.

        :param news: The News instance to write.
        """
        super().update(news)
        try:
            with open(self.__filename, 'a') as fhand:
                fhand.write(f"{news}\n\n")
        except Exception as e:
            print(f"Error: {e}")
            return
        print(f"{self.__class__.__name__} save news to the {self.__filename}")


class AuthorWatcher(Observer):
    """
    Observer that counts and reports how many times
    each author has published news.
    """

    def __init__(self):
        """
        Initialize the author watcher with an empty tracking dictionary.
        """
        self.__authors = {}

    def update(self, news: News):
        """
        Handle the news update by updating the count for the news author.

        :param news: The News instance received.
        """
        super().update(news)
        self.__authors[news.author] = self.__authors.get(news.author, 0) + 1
        print(f"{self.__class__.__name__} reports: "
              f"It was news №{self.__authors[news.author]} for {news.author}"
        )


def main():
    """
    Simulate news publishing and observer notification workflow.
    """
    publisher = NewsPublisher()
    news_logger = NewsLogger()
    author_watcher = AuthorWatcher()

    publisher.subscribe(news_logger)
    publisher.subscribe(author_watcher)
    print("NewsLogger and AuthorWatcher were subscribed")
    print("===Testing===")

    news_list = [
        News(
            "AI Breakthrough",
            "New AI model surpasses GPT-4.",
            "Alice"
        ),
        News(
            "Quantum Computing",
            "Researchers achieve stable 1000-qubit operation.",
            "Bob"
        ),
        News(
            "SpaceX Launch",
            "Falcon 9 successfully launches 22 satellites.",
            "Alice"
        ),
        News(
            "Cyberattack Reported",
            "Major tech firm hit by ransomware attack.",
            "Eve"
        )
    ]

    for news in news_list:
        publisher.publish_news(news)

    time.sleep(1.5)
    publisher.unsubscribe(news_logger)
    print("\nNewsLogger were unsubscribed")
    time.sleep(1.5)
    publisher.publish_news(
        News("AI Regulation", "EU passes new AI safety regulations.", "Bob")
    )


# Run main() only when script is executed directly
if __name__ == "__main__":
    main()
