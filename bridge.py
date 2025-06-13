from abc import ABC, abstractmethod
from typing import List
import matplotlib.pyplot as plt

class Style(ABC):
    """Interface representing a chart style."""
    @abstractmethod
    def get_color(self) -> str:
        """Return the main color used for chart elements."""

    @abstractmethod
    def get_linewidth(self) -> float:
        """Return the line width for chart elements."""

    @abstractmethod
    def get_alpha(self) -> float:
        """Return the alpha (transparency) value for chart elements."""

    @abstractmethod
    def get_fontsize(self) -> int:
        """Return the font size used in chart text."""


class SimpleStyle(Style):
    """Concrete Style implementation with simple styling."""

    def get_color(self) -> str:
        return 'black'

    def get_linewidth(self) -> float:
        return 0.5

    def get_alpha(self) -> float:
        return 0.4
    
    def get_fontsize(self) -> int:
        return 12
    

class BrightStyle(Style):
    """Concrete Style implementation with bright styling."""

    def get_color(self) -> str:
        return 'blue'

    def get_linewidth(self) -> float:
        return 5

    def get_alpha(self) -> float:
        return 0.7
    
    def get_fontsize(self) -> int:
        return 16


class Chart(ABC):
    """Abstract base class representing a chart."""

    def __init__(self, style: Style):
        """
        Initializes the chart with a style.

        :param style: Style instance to apply to the chart.
        :raises TypeError: If style is not an instance of Style.
        """
        if not isinstance(style, Style):
            raise TypeError("Parameter 'style' must be an instance of Style")
        self._style = style

    @abstractmethod
    def build(self, labels: List[str], values: List[int | float]) -> None:
        """
        Builds and displays the chart.

        :param labels: List of labels on X-axis.
        :param values: List of values on Y-axis.
        """
    
    @staticmethod
    def _check_data(labels: str, values: List[int | float]) -> None:
        """
        Validates the input data.

        :param labels: List of label strings.
        :param values: List of numeric values.
        :raises TypeError: If labels or values are not lists or contain invalid types.
        :raises ValueError: If labels and values have different lengths.
        """
        # Check data type
        if not isinstance(labels, list) or not isinstance(values, list):
            raise TypeError("'labels' and 'values' must be instances of list")
        # Compare sizes
        if len(labels) != len(values):
            raise ValueError("'labels' and 'values' must have equal sizes")
        # Check elements' types
        for el in labels:
            if not isinstance(el, str):
                raise TypeError("all labels must be strings")
        for el in values:
            if not isinstance(el, (int, float)):
                raise TypeError("all values must be numbers")


class BarChart(Chart):
    """
    Concrete chart class for bar charts.
    """    
    def build(self, labels: List[str], values: List[int | float]) -> None:
        super()._check_data(labels, values)
        try:
            plt.bar(
                labels,
                values,
                color=self._style.get_color(),
                linewidth=self._style.get_linewidth(),
                alpha=self._style.get_alpha(),
            )
            fontsize = self._style.get_fontsize()
            plt.title('Bar Chart', fontsize=fontsize + 2)
            plt.xlabel('Labels', fontsize=fontsize)
            plt.ylabel('Values', fontsize=fontsize)
            plt.show()
        except (ValueError, TypeError, KeyError) as e:
            print(f"Chart rendering failed: {e}")
        except Exception as e:
            print(e)


class ScatterChart(Chart):  
    """
    Concrete chart class for scatter charts.
    """  
    def build(self, labels: List[str], values: List[int | float]) -> None:
        super()._check_data(labels, values)
        try:
            plt.scatter(
                labels,
                values,
                c=self._style.get_color(),
                linewidth=self._style.get_linewidth(),
                alpha=self._style.get_alpha(),
            )
            fontsize = self._style.get_fontsize()
            plt.title('Scatter Chart', fontsize=fontsize + 2)
            plt.xlabel('Labels', fontsize=fontsize)
            plt.ylabel('Values', fontsize=fontsize)
            plt.show()
        except (ValueError, TypeError, KeyError) as e:
            print(f"Chart rendering failed: {e}")
        except Exception as e:
            print(e)


def main():
    """
    Demonstrates usage of different chart types with different styles.
    """
    # Example data
    labels = ['A', 'B', 'C', 'D']
    values = [30, 15, 45, 10]
    # Create different styles
    simple_style = SimpleStyle()
    bright_style = BrightStyle()
    # Build charts with different styles
    charts = [BarChart(simple_style), BarChart(bright_style),
              ScatterChart(simple_style), ScatterChart(bright_style)]
    for chart in charts:
        chart.build(labels, values)

# Run main() only when script is executed directly
if __name__ == "__main__":
    main()