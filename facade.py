from PIL import Image
from PIL import UnidentifiedImageError
from typing import Optional

class ImageEditor:
    """
    Facade class that simplifies common image operations using the Pillow library.
    
    Provides an easy-to-use interface for resizing, rotating, and converting images to grayscale.
    Handles validation and exceptions internally to reduce boilerplate for the user.
    """
    @staticmethod
    def _check_str(name: str, value):
        """
        Validate that the given data is a non-empty string.

        :param name: Name of the parameter (used for error messages).
        :param value: The string to validate.
        :raises TypeError: If the value is not a string.
        :raises ValueError: If the string is empty or whitespace.
        """
        if not isinstance(name, str) or not name.strip():
            name = "variable"

        if not isinstance(value, str):
            raise TypeError(f"Parameter '{name}' must be a string.")
        if not value.strip():
            raise ValueError(f"Parameter '{name}' can not be empty.")

    @staticmethod
    def _check_int(name: str, value):
        """
        Validate that the given value is a positive integer.

        :param name: Name of the parameter (used for error messages).
        :param value: The integer to validate.
        :raises TypeError: If the value is not an integer.
        :raises ValueError: If the value is less than 1.
        """
        if not isinstance(name, str) or not name.strip():
            name = "variable"

        if not isinstance(value, int):
            raise TypeError(f"Parameter '{name}' must be an integer number.")
        if value < 1:
            raise ValueError(f"Parameter '{name}' must have positive value.")
    
    @classmethod
    def _open(cls, source: str) -> Optional[Image.Image]:
        """
        Open an image from the given source file path.

        :param source: Path to the image file.
        :return: Image object if successful, None otherwise.
        """
        cls._check_str("source", source)
        try:
            return Image.open(source)
        except FileNotFoundError:
            print(f"The file {source} can not be found.")
        except UnidentifiedImageError:
            print(f"The file {source} can not be opened and identified.")
    
    @classmethod
    def _save(cls, img: Image.Image, destination: str):
        """
        Save an image to the specified destination path.

        :param img: An instance of PIL.Image.Image.
        :param destination: Path to save the image.
        :raises TypeError: If img is not a valid image.
        """
        if not isinstance(img, Image.Image):
            raise TypeError(
                "Parameter 'img' must be an instance of PIL.Image.Image."
            )
        cls._check_str("destination", destination)
        try:
            img.save(destination)
        except ValueError:
            print(f"Wrong file format in {destination}.")
        except OSError:
            print(f"The file {destination} could not be written.")
    
    @classmethod
    def resize_image(cls, width: int, height: int, source: str, destination: str):
        """
        Resize an image to the specified width and height.

        :param width: Target width.
        :param height: Target height.
        :param source: Path to the source image.
        :param destination: Path to save the resized image.
        """
        cls._check_int("width", width)
        cls._check_int("height", height)
        img = cls._open(source)
        if not img:
            return
        cls._save(img.resize((width, height)), destination)  
        
    @classmethod
    def rotate_image(
        cls, angle: int, source: str, destination: str
    ):
        """
        Rotate an image by the given angle.

        :param angle: Angle in degrees.
        :param source: Path to the source image.
        :param destination: Path to save the rotated image.
        """
        cls._check_int("angle", angle)        
        img = cls._open(source)
        if not img:
            return
        cls._save(img.rotate(angle), destination)

    @classmethod
    def image_to_grayscale(cls, source: str, destination: str):
        """
        Convert an image to grayscale.

        :param source: Path to the source image.
        :param destination: Path to save the grayscale image.
        """
        img = cls._open(source)
        if not img:
            return
        cls._save(img.convert("L"), destination)  


def main():
    """
    Demonstrates the usage of the ImageEditor facade 
    to perform common image operations:
    resizing, rotating, and converting images to grayscale.
    """
    ImageEditor.resize_image(50, 50, "sample.jpg", "resized.jpg")
    ImageEditor.rotate_image(90, "sample.jpg", "rotated.jpg")
    ImageEditor.image_to_grayscale("sample.jpg", "grayscale.jpg")
    
# Run main() only when script is executed directly
if __name__ == "__main__":
    main()