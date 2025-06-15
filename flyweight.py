from turtle import Turtle, Screen
from typing import Dict, Tuple
import random
from matplotlib.colors import CSS4_COLORS


class Figure:
    """
    Represents a drawable figure (circle, square, or triangle) with a specific color.

    This class encapsulates the drawing logic for a figure using the turtle graphics library.
    """

    _shapes = {"circle", "square", "triangle"}
    # Hidden turtle used only for validating color names
    _test_turtle = Turtle()
    _test_turtle.hideturtle()
    _test_turtle.penup()

    def __init__(self, shape: str, color: str):
        """
        Initializes a Figure with a given shape and color.

        :param shape: The shape of the figure ('circle', 'square', or 'triangle').
        :param color: The fill color of the figure.
        :raises TypeError: If shape or color is not a string.
        :raises ValueError: If shape is not supported or color is invalid.
        """
        if not isinstance(shape, str):
            raise TypeError("Parameter 'shape' must be a string.")
        if shape not in self._shapes:
            raise ValueError(f"Bad shape name: '{shape}'.")
        if not isinstance(color, str):
            raise TypeError("Parameter 'color' must be a string.")
        if not self._is_color_supported(color):
            raise ValueError(f"Bad color name: '{color}'.")
        self.__shape = shape
        self.__color = color

    @classmethod
    def _is_color_supported(cls, color: str) -> bool:
        """
        Checks whether the given color is supported by turtle.

        :param color: Color string to validate.
        :return: True if color is supported, False otherwise.
        """
        try:
            cls._test_turtle.color(color)
            return True
        except:
            return False

    def draw(self, pen: Turtle, x: float, y: float):
        """
        Draws the figure at the specified coordinates using the given Turtle pen.

        :param pen: An instance of Turtle used for drawing.
        :param x: X-coordinate of the drawing position.
        :param y: Y-coordinate of the drawing position.
        :raises TypeError: If pen is not a Turtle or coordinates are not numbers.
        """
        if not isinstance(pen, Turtle):
            raise TypeError("Parameter 'turtle' must be an instance of turtle.Turtle.")
        if not isinstance(x, (float, int)) or not isinstance(y, (float, int)):
            raise TypeError("Parameters 'x' and 'y' must be float numbers.")

        pen.shape(self.__shape)
        pen.goto((x, y))
        pen.shapesize()  # Use default size
        pen.color('', self.__color)  # Set fill color only
        pen.stamp()  # Stamp the current shape at the turtle's location


class FigureFactory:
    """
    Flyweight factory for creating and reusing Figure instances with specific shape and color.
    """

    _figures: Dict[Tuple[str, str], Figure] = {}

    @classmethod
    def get_figure(cls, shape: str, color: str) -> Figure:
        """
        Returns a shared instance of Figure with the given shape and color.

        :param shape: Shape of the figure.
        :param color: Color of the figure.
        :return: A Figure instance.
        :raises TypeError: If parameters are not strings.
        :raises ValueError: If parameters are empty.
        """
        if not isinstance(shape, str):
            raise TypeError("Parameter 'shape' must be a string.")
        if not shape.strip():
            raise ValueError("Parameter 'shape' can not be empty.")
        if not isinstance(color, str):
            raise TypeError("Parameter 'color' must be a string.")
        if not color.strip():
            raise ValueError("Parameter 'color' can not be empty.")

        if (shape, color) not in cls._figures:
            cls._figures[(shape, color)] = Figure(shape, color)
        return cls._figures[(shape, color)]

    @classmethod
    def figure_count(cls) -> int:
        """
        Returns the number of unique Figure instances created.

        :return: The number of figures in the internal cache.
        """
        return len(cls._figures)


def main():
    """
    Main function to draw multiple random figures on the screen using turtle graphics.
    Demonstrates the Flyweight pattern by reusing Figure instances.
    """
    count = 300
    # Use the first 20 named CSS4 colors
    colors = tuple(CSS4_COLORS.keys())[:20]
    shapes = ("circle", "square", "triangle")

    screen = Screen()
    pen = Turtle()
    pen.penup()  # Prevent drawing lines when moving
    pen.hideturtle() # Hide turtle

    for _ in range(count):
        color = random.choice(colors)
        shape = random.choice(shapes)
        figure = FigureFactory.get_figure(shape, color)
        figure.draw(
            pen,
            random.randint(-count, count),
            random.randint(-count, count)
        )

    print(f"{count} random figures were painted.")
    print(f"{FigureFactory.figure_count()} unique Figure instance(s) were used.")

    screen.mainloop()


# Run main() only when script is executed directly
if __name__ == "__main__":
    main()
