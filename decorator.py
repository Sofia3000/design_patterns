from abc import ABC, abstractmethod

class Validator(ABC):
    """
    Abstract base class for validators.
    """
    @abstractmethod
    def is_valid(self, data: str) -> bool:
        """
        Check if the input data is valid.

        :param data: The string to validate.
        :return: True if valid, False otherwise.
        """


class PasswordValidator(Validator):
    """
    Basic validator that checks whether a string is non-empty and not just whitespace.
    """
    def is_valid(self, data: str) -> bool:
        """
        Validate that the input is a non-empty string.

        :param data: Password string to validate.
        :return: True if non-empty and not only whitespace, False otherwise.
        :raises TypeError: If data is not a string.
        """
        if not isinstance(data, str):
            raise TypeError("Data must be a string")
        return bool(data.strip())


class ValidatorDecorator(Validator):
    """
    Base class for all validator decorators.
    """
    def __init__(self, validator: Validator):
        """
        Initialize the decorator with a base validator.

        :param validator: An instance of a Validator.
        :raises TypeError: If validator is not a Validator instance.
        """
        if not isinstance(validator, Validator):
            raise TypeError(
                "Parameter 'validator' must be an instance of Validator"
            )
        self._validator = validator
    
    def is_valid(self, data: str) -> bool:
        """
        Pass validation to the wrapped validator.

        :param data: The string to validate.
        :return: Result of the wrapped validator.
        :raises TypeError: If data is not a string.
        """
        if not isinstance(data, str):
            raise TypeError("Data must be a string")
        return self._validator.is_valid(data)


class ValidateLengthDecorator(ValidatorDecorator):
    """
    Decorator that checks if a string meets a minimum length requirement.
    """
    def __init__(self, validator: Validator):
        """
        Initialize with a minimum length (default: 8).

        :param validator: A base validator to wrap.
        """
        super().__init__(validator)
        self.min_length = 8

    @property
    def min_length(self):
        return self.__min_length
    
    @min_length.setter
    def min_length(self, length):
        """
        Set the minimum length for the password.

        :param length: Minimum number of characters.
        :raises TypeError: If length is not an integer.
        :raises ValueError: If length is less than 1.
        """
        if not isinstance(length, int):
            raise TypeError("Length must be an integer number")
        if length < 1:
            raise ValueError("Length must be positive number")
        self.__min_length = length

    def is_valid(self, data: str) -> bool:
        """
        Check if the string is valid according to the base validator
        and has at least the minimum required number of characters.

        :param data: The password string to validate.
        :return: True if the string is valid, False otherwise.
        """
        return super().is_valid(data) and len(data) >= self.min_length 
    
class ValidateLettersDecorator(ValidatorDecorator):
    """
    Decorator that ensures the string contains at least one letter.
    """
    def is_valid(self, data: str) -> bool:
        """
        Check if the string is valid according to the base validator
        and contains at least one letter.

        :param data: The password string to validate.
        :return: True if the string is valid, False otherwise.
        """
        return super().is_valid(data) and any(c.isalpha() for c in data)


class ValidateDigitsDecorator(ValidatorDecorator):
    """
    Decorator that ensures the string contains at least one digit.
    """
    def is_valid(self, data: str) -> bool:
        """
        Check if the string is valid according to the base validator
        and contains at least one digit.

        :param data: The password string to validate.
        :return: True if the string is valid, False otherwise.
        """
        return super().is_valid(data) and any(c.isdecimal() for c in data)


def validate_password(password: str, validator: Validator):
    """
    Run a validator on the given password and print the result.

    :param password: The password string to validate.
    :param validator: The validator to use.
    :raises TypeError: If password is not a string or validator is invalid.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    if not isinstance(validator, Validator):
        raise TypeError("Parameter 'validator' must be an instance of Validator")
    print(f"Password '{password}'", end=' ')
    if validator.is_valid(password):
        print("is valid.")
    else:
        print("is not valid.")

def main():
    """
    Demonstrates the Decorator pattern with password validation.
    """
    password_list = [
        "",
        "small12",
        "onlyletters",
        "1234567890",
        "proper1234"
    ]

    simple_validator = PasswordValidator()
    length_validator = ValidateLengthDecorator(simple_validator)
    length_letter_validator = ValidateLettersDecorator(length_validator)
    complex_validator = ValidateDigitsDecorator(length_letter_validator)
    
    validators = [
        simple_validator,
        length_validator,
        length_letter_validator,
        complex_validator
    ]

    for password in password_list:
        for validator in validators:
            validate_password(password, validator)
        print('-'*30)
    
# Run main() only when script is executed directly
if __name__ == "__main__":
    main()